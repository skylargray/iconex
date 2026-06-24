#!/usr/bin/env python3
"""ANGLE pt3: does removing the model's SPURIOUS DMEM accesses at genuine FPC
steps move lambda toward decay?

The hardware decodes device (DMEM vs FPC) from the absolute address / T&C strobe;
DMEM CAS/ falls only on MEMAC. If a step is a true FPC D/A write (WR DA/) or A/D
read (RD AD/), the DMEM is NOT strobed there, so the model's b3 write-back and its
DMEM read at those steps are accesses the hardware does NOT perform.

Test (principled, NOT a hand-tuned subset): take the base-invariant FPC fingerprints
ONLY -- input read (s76) and the diagnostic-confirmed OUTPUT-write pattern -- and at
those steps DO NOT touch DM (route to FPC instead, silent input=0). Measure lambda.

We test a few principled definitions of "genuine FPC step" so the result is not an
artifact of one threshold:
  V0  baseline (current model, every step is DMEM)
  V1  suppress DM at the single input read s76 only
  V2  + suppress DM at COMPUTED-addr-bit15 steps (the real top-of-RAM I/O region)
  V3  + suppress DM at ALL (bit15-offset & WA==3) output-write-fingerprint steps
Reports converged lambda (median tail) for each.

Read-only; reimplements the float datapath locally (does not modify committed code).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
prog = A.load_microcode(0x01)


def lam(prog, fpc_steps, nsamp=60000, K=128, seed=1e4):
    """fpc_steps: set of step indices where the access is FPC, not DMEM (no DM r/w;
    read returns external/0, b3 write suppressed)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            is_fpc = st['s'] in fpc_steps
            if is_fpc:
                dab = 0.0          # FPC: external sample (silent=0) / output write drives FPC, not DM
            else:
                dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3'] and not is_fpc:
                DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s; R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    tail = sorted(traj[-60:]); return tail[len(tail)//2]


# Build the principled step sets
input_read = {76}
# computed-addr-bit15 region (at base 0): the genuine top-of-memory I/O block
addr_b15 = set()
for pos in range(2000):
    p2 = (pos+1) & DMASK
    for p in prog:
        if ((p2 - p['offset']) & DMASK) & 0x8000:
            addr_b15.add(p['s'])
out_fp = {p['s'] for p in prog if (p['offset']&0x8000) and p['WA']==3}

V0 = lam(prog, set())
V1 = lam(prog, input_read)
V2 = lam(prog, input_read | addr_b15)
V3 = lam(prog, input_read | out_fp)
V4 = lam(prog, input_read | addr_b15 | out_fp)

def show(tag, l, base=V0):
    print(f"  {tag:55s} lambda={l:.7f}  ppm={(l-1)*1e6:+8.1f}  "
          f"{'GROW' if l>1 else 'DECAY'}  (d_vs_base={ (l-base)*1e6:+8.1f} ppm)")

print("converged lambda (median of last 60 windows), target 0.9999899:\n")
show("V0 baseline (every step DMEM)", V0)
show("V1 suppress DM at input-read s76 only", V1)
show("V2 + suppress DM at computed-addr-bit15 I/O region", V2)
show("V3 + suppress DM at (offset-b15 & WA==3) output-writes", V3)
show("V4 + both regions", V4)
print(f"\n  addr-b15 region steps : {sorted(addr_b15)}")
print(f"  output-write fp steps : {sorted(out_fp)}  (n={len(out_fp)})")
print(f"  overlap of out_fp with model DMEM-write steps (b3=1): "
      f"{sorted(s for s in out_fp if any(p['s']==s and p['b3'] for p in prog))}")
