#!/usr/bin/env python3
"""Phantom FPC-output recirculation hunt.

Angle: a real FPC OUTPUT write (drives the DAC) is modeled here either as a harmless
read (b3=0 => dab=DM[addr], no write) or, if mis-decoded, as a DMEM write that another
step reads back -> phantom feedback inflating lambda.

Section 12 (authoritative) FPC OUTPUT fingerprint:
  bit15 set (offset & 0x8000), WA==3 (pass-through), XFER==0, b3(RW)==0, ZERO==0
  i.e. ctl in {0x01,0x02,0x03}; the device is chosen by offset high bits, NOT a microword bit.
FPC INPUT fingerprint: bit15 set, WA==2 (read reg), low14==0x3FFF (base-invariant), XFER==0.

Recirculation closer (MUST NOT suppress): XFER==1 AND b3==1 (computes RES then writes DMEM),
or b3==1 read-back steps that feed the comb/allpass loop.
"""
import sys, os, math
sys.path.insert(0, 'tools')
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def classify(prog):
    fpc_in = []
    fpc_out = []
    for p in prog:
        o = p['offset']
        b15 = (o >> 15) & 1
        low14 = o & 0x3FFF
        if not b15:
            continue
        # INPUT: WA==2, low14==0x3FFF, XFER==0  (base-invariant fingerprint)
        if p['WA'] == 2 and low14 == 0x3FFF and p['XFER'] == 0 and p['b3'] == 0:
            fpc_in.append(p)
        # OUTPUT: WA==3, XFER==0, b3==0, ZERO==0  (pass-through, no DMEM write, no acc clear)
        elif p['WA'] == 3 and p['XFER'] == 0 and p['b3'] == 0 and p['ZERO'] == 0:
            fpc_out.append(p)
    return fpc_in, fpc_out


def dmem_dep_graph(prog):
    """At base pos=0 (confirmed), addr = (-offset)&0xFFFF for every step.
    Build: which (step) WRITES which addr (b3==1), which step READS which addr (b3==0).
    A 'phantom loop' = a write-addr that is also a read-addr of some OTHER step.
    Report bit15-set write addrs specially."""
    # addr is pos-relative; the relative tap = (-offset)&MASK is constant in n.
    writes = {}   # addr -> list of writer step s
    reads = {}    # addr -> list of reader step s
    for p in prog:
        rel = (-p['offset']) & DMASK
        if p['b3']:
            writes.setdefault(rel, []).append(p['s'])
        else:
            reads.setdefault(rel, []).append(p['s'])
    return writes, reads


def lambda_run(prog, suppress_steps=frozenset(), nsamp=60000, K=128, seed=1e4):
    """Float-exact map (identical to exp_lambda_clean) but: any step in suppress_steps
    routes its FPC access to a SINK (no DMEM read, no DMEM write, dab=0). All else faithful.
    Returns converged lambda (median of last 60 windows)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            sup = st['s'] in suppress_steps
            if sup:
                dab = 0.0              # FPC output -> separate sink, not DMEM
            else:
                dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3'] and not sup:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:]); return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    fpc_in, fpc_out = classify(prog)
    print("=== FPC step classification (section-12 fingerprint) ===")
    print("INPUT steps (bit15, WA=2, low14=0x3FFF, XFER=0, b3=0):")
    for p in fpc_in:
        print(f"  s={p['s']:3d} off={p['offset']:#06x} WA={p['WA']} coeff={p['coeff']}")
    print("OUTPUT steps (bit15, WA=3, XFER=0, b3=0, ZERO=0):")
    for p in fpc_out:
        o = p['offset']
        print(f"  s={p['s']:3d} off={o:#06x} b14={(o>>14)&1} low14={o&0x3FFF:#06x} "
              f"WA={p['WA']} coeff={p['coeff']}")
    out_steps = frozenset(p['s'] for p in fpc_out)
    in_steps = frozenset(p['s'] for p in fpc_in)

    print("\n=== DMEM write->read dependency graph (base pos=0) ===")
    writes, reads = dmem_dep_graph(prog)
    # phantom loops: a written rel-addr that some OTHER step reads
    phantom = []
    writeonly = []
    for rel, ws in writes.items():
        rs = reads.get(rel, [])
        readers = [s for s in rs]
        b15 = (rel == ((-(rel ^ 0)) & DMASK))  # placeholder; compute below
        if readers:
            phantom.append((rel, ws, readers))
        else:
            writeonly.append((rel, ws))
    # bit15-set write addresses: those whose ABSOLUTE offset had bit15 set
    print(f"  total distinct write rel-addrs: {len(writes)}")
    print(f"  total distinct read  rel-addrs: {len(reads)}")
    print(f"  write rel-addrs READ BACK by some step (real loops): {len(phantom)}")
    print(f"  write-only rel-addrs (harmless): {len(writeonly)}")
    # Now: of the b15-set writers, are any read back?
    b15writers = [p for p in prog if p['b3'] and ((p['offset']>>15)&1)]
    print(f"\n  b3-writer steps with bit15-set offset: {len(b15writers)}")
    for p in b15writers:
        rel = (-p['offset']) & DMASK
        rs = reads.get(rel, [])
        ws = [w for w in writes.get(rel, []) if w != p['s']]
        tag = "READ-BACK(loop)" if rs else "write-only"
        # is this step itself a closer? XFER+b3 or b3 read-back closer
        print(f"    s={p['s']:3d} off={p['offset']:#06x} XFER={p['XFER']} b3=1 "
              f"rel={rel:#06x} readers={rs} cowriters={ws}  -> {tag}")

    print("\n=== lambda measurements (float-exact, converged median) ===")
    base = lambda_run(prog)
    print(f"  baseline                                 lambda={base:.7f}  ({(base-1)*1e6:+.1f} ppm)")
    if out_steps:
        supp_out = lambda_run(prog, suppress_steps=out_steps)
        print(f"  suppress FPC-OUTPUT steps {sorted(out_steps)}     lambda={supp_out:.7f}  ({(supp_out-1)*1e6:+.1f} ppm)  d={(supp_out-base)*1e6:+.1f} ppm")
    else:
        print("  (no FPC-OUTPUT steps matched the strict fingerprint)")
    supp_in = lambda_run(prog, suppress_steps=in_steps)
    print(f"  suppress FPC-INPUT  steps {sorted(in_steps)}          lambda={supp_in:.7f}  ({(supp_in-1)*1e6:+.1f} ppm)  d={(supp_in-base)*1e6:+.1f} ppm")
    if out_steps or in_steps:
        supp_both = lambda_run(prog, suppress_steps=out_steps | in_steps)
        print(f"  suppress BOTH                            lambda={supp_both:.7f}  ({(supp_both-1)*1e6:+.1f} ppm)  d={(supp_both-base)*1e6:+.1f} ppm")


if __name__ == '__main__':
    main()
