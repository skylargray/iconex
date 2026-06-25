#!/usr/bin/env python3
"""DECODE ARBITER: test decode hypotheses against BOTH gates that a correct 224XL
decode must pass simultaneously:

  GATE A (diagnostic, tech-ref-VERIFIED): build the ZERO-DELAY / .5s-DELAY diagnostic
    images, route FPC I/O by offset bit15 (tech ref section 12), run the integer ARU,
    and require ZERO-DELAY -> ~unity passthrough and MAX-DELAY -> ~unity echo ~17065.
  GATE B (over-unity): power-iterate every clean live program; require all lambda <= 1.

A correct decode passes BOTH. The OLD decode (tech-ref section 3) passes A, fails B;
the FRONTIER decode (rebuild2) passes B -- this tells us whether it also passes A.

Decode variants:
  old   : ctl=~l2; WA=ctl&3, XFER=(ctl>>2)&1, b3=(ctl>>3)&1, RA=(ctl>>4)&3, ZERO=(ctl>>7)&1;
          coeff=+/-(l3&0x7f), Cs=mag>>1 (gain Cs/64). DMEM via b3. No acc_latch.
  front : v2=l2; MI16=b0,MI17=b1, WA=b2:3, RA=b4:5, CSIGN=b7; l3(inv_l3): XFER=b0,ZERO=b1,
          coeff=b2:7 (Cs=+/-that). DMEM via MI16/MI17. acc_latch.
FPC I/O for BOTH: address-decoded by offset bit15 (input: bit15 & low14==0x3FFF; output: bit15 & WA==3).
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_diagunity as DG
import _hunt_rawcache as RC
MASK = 0xFFFF
FS = 34130.0


def sat20(x):
    return 262143 if x > 262143 else (-262144 if x < -262144 else x)


def sat16(x):
    return 32767 if x > 32767 else (-32768 if x < -32768 else x)


def decode_old(steps):
    prog = []
    for (s, l0, l1, l2, l3) in steps:
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & MASK
        mag = l3 & 0x7F
        coeff = -mag if (l3 & 0x80) else mag
        Cs = -(mag >> 1) if (l3 & 0x80) else (mag >> 1)
        prog.append(dict(s=s, offset=offset, WA=ctl & 3, RA=(ctl >> 4) & 3,
                         XFER=(ctl >> 2) & 1, ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1,
                         Cs=Cs, model='old', MI16=0, MI17=0, sub=0))
    return prog


def decode_front(steps, inv_l3, coeff_shift=2, zero_from='l3'):
    """coeff_shift: cmag = (v3>>coeff_shift)&0x3F  (2=frontier l3[2:7]; 1=l3[1:6]=old mag>>1).
    zero_from: 'l3' -> ZERO=v3.b1 (frontier); 'l2b7' -> ZERO=l2.b7, CSIGN from l3.b7 (hybrid)."""
    prog = []
    for (s, l0, l1, l2, l3) in steps:
        vl1 = (~l1) & 0xFF
        v2 = l2 & 0xFF
        v3 = (~l3 & 0xFF) if inv_l3 else (l3 & 0xFF)
        offset = (~(l0 | (l1 << 8))) & MASK
        MI16 = v2 & 1; MI17 = (v2 >> 1) & 1
        WA = (v2 >> 2) & 3; RA = (v2 >> 4) & 3
        MI12 = (vl1 >> 4) & 1; MI13 = (vl1 >> 5) & 1
        xfer = v3 & 1
        cmag = (v3 >> coeff_shift) & 0x3F
        if zero_from == 'l2b7':
            zero = (v2 >> 7) & 1; csign = (v3 >> 7) & 1
        else:
            zero = (v3 >> 1) & 1; csign = (v2 >> 7) & 1
        Cs = -cmag if csign else cmag
        prog.append(dict(s=s, offset=offset, WA=WA, RA=RA, XFER=xfer, ZERO=zero,
                         Cs=Cs, model='front', MI16=MI16, MI17=MI17, sub=(MI13 << 1) | MI12, b3=0))
    return prog


def diag_steps(zero_delay):
    img = DG.build_image(zero_delay=zero_delay)
    return [(s, img[s*4], img[s*4+1], img[s*4+2], img[s*4+3])
            for s in range(128) if not (img[s*4+2] == 0xFF and img[s*4+3] == 0xFF)]


def run_diag(prog, acc_latch, read_bit, nsamp, imp=20000):
    """FPC I/O address-decoded by offset bit15. Returns out_log[s] = list of RES driven
    to each WR-DA output step per sample; and the input step list."""
    R = [0]*4; ACC = 0; RES = 0; ACCprev = 0; DM = [0]*(MASK+1); pos = 0
    # FPC I/O address-decoded by offset bit15 (tech ref 12): input fingerprint = low14==0x3FFF
    # (the ADC strobe); output = WA=3 pass-through with bit15 and low14 != 0x3FFF.
    in_steps = [st['s'] for st in prog if (st['offset'] & 0x8000) and (st['offset'] & 0x3FFF) == 0x3FFF]
    out_steps = [st['s'] for st in prog
                 if (st['offset'] & 0x8000) and st['WA'] == 3 and (st['offset'] & 0x3FFF) != 0x3FFF]
    out_log = {s: [] for s in out_steps}
    for n in range(nsamp):
        pos = (pos + 1) & MASK
        for st in prog:
            off = st['offset']; fpc = bool(off & 0x8000); low14 = off & 0x3FFF
            is_input = fpc and low14 == 0x3FFF
            is_output = fpc and st['WA'] == 3 and low14 != 0x3FFF
            addr = (pos - off) & MASK
            is_dmem_write = False
            if is_input:
                dab = imp if n == 0 else 0
            elif is_output:
                # Hypothesis: the WR-DA output step reads the DMEM delay-tap at its offset's
                # low14 (tech ref 12: low14 "doubles as the delay-tap selector"), drives THAT
                # to the FPC output. Capture both candidates: RES and the DMEM tap.
                tap = DM[addr]
                out_log[st['s']].append((RES, tap))
                dab = RES
            elif fpc:
                dab = 0
            elif st['model'] == 'old':
                if st['b3']:
                    dab = RES; is_dmem_write = True
                else:
                    dab = DM[addr]
            else:  # front DMEM
                is_read = st['MI17'] == 1 and st['MI16'] == read_bit
                is_dmem_write = st['MI17'] == 1 and not is_read
                is_sub = st['MI17'] == 0 and st['MI16'] == 1
                if is_read:
                    dab = DM[addr]
                elif is_sub and st['sub'] == 1:
                    dab = RES
                elif is_dmem_write:
                    dab = RES
                else:
                    dab = 0
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0
            prod = (x << 3) * st['Cs'] >> 6
            ACC = sat20(ACC + prod)
            if st['XFER']:
                RES = sat16((ACCprev if acc_latch else ACC) >> 3)
            if is_dmem_write:
                DM[addr] = RES
            ACCprev = ACC
    return out_log, in_steps, out_steps


def lam(prog, acc_latch, read_bit, nsamp=16000, warmup=4000, rseed=1):
    """Closed-loop float power-iteration lambda for a LIVE program (RD-AD input=0).
    PURE device decode (no offset-bit15 FPC routing -- live offsets are absolute at base 0,
    so a bit15 offset is a large DMEM delay, NOT an FPC access). Matches _hunt_rebuild2.lam."""
    rng = random.Random(rseed)
    R = [rng.uniform(-1, 1) for _ in range(4)]
    ACC = rng.uniform(-1, 1); RES = rng.uniform(-1, 1); ACCp = ACC
    DM = [0.0]*(MASK+1); pos = 0; nz = set(); traj = []; K = 128
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for st in prog:
            off = st['offset']; addr = (pos - off) & MASK
            is_dmem_write = False
            if st['model'] == 'old':
                if st['b3']:
                    dab = RES; is_dmem_write = True
                else:
                    dab = DM[addr]
            else:
                is_read = st['MI17'] == 1 and st['MI16'] == read_bit
                is_dmem_write = st['MI17'] == 1 and not is_read
                is_sub = st['MI17'] == 0 and st['MI16'] == 1
                if is_read: dab = DM[addr]
                elif is_sub and st['sub'] == 1: dab = RES        # RDRREG feedback
                elif is_sub and st['sub'] == 3: dab = 0.0        # RD AD input = 0 (closed loop)
                elif is_dmem_write: dab = RES
                else: dab = 0.0
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']: RES = (ACCp if acc_latch else ACC) / 8.0
            if is_dmem_write: DM[addr] = RES; nz.add(addr)
            ACCp = ACC
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC+RES*RES+ACCp*ACCp+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            if (n+1) > warmup: traj.append(math.exp(math.log(s)/K))
            f = 1.0/s; R = [v*f for v in R]; ACC *= f; RES *= f; ACCp *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2] if tail else float('nan')


def gate_a(name, prog_builder, acc_latch, read_bit):
    """Run ZERO-DELAY (passthrough) and MAX-DELAY (echo) diagnostics."""
    zd = prog_builder(diag_steps(True))
    md = prog_builder(diag_steps(False))
    zlog, zin, zout = run_diag(zd, acc_latch, read_bit, nsamp=400)
    mlog, _, mout = run_diag(md, acc_latch, read_bit, nsamp=40000)
    print(f"  [{name}] in_steps={zin} out_steps={zout}")
    for ci, lbl in ((0, 'RES'), (1, 'TAP')):
        for s in zout:
            seq = [v[ci] for v in zlog[s]]
            nz = [(i, v) for i, v in enumerate(seq) if abs(v) > 1]
            if nz:
                i0, v0 = nz[0]
                ipk = max(range(len(seq)), key=lambda i: abs(seq[i]))
                print(f"    ZD[{lbl}] s{s}: first@{i0} g={v0/20000:+.4f}  peak@{ipk} g={seq[ipk]/20000:+.4f}")
        for s in mout:
            seq = [v[ci] for v in mlog[s]]
            late = [(i, v) for i, v in enumerate(seq) if i > 100 and abs(v) > 200]
            if late:
                ipk, vpk = max(late, key=lambda t: abs(t[1]))
                print(f"    MAX[{lbl}] s{s}: echo peak@{ipk} ({ipk/FS*1000:.1f}ms) g={vpk/20000:+.4f}")


def gate_b(prog_builder, acc_latch, read_bit):
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    hot = []; loss = 0
    for p in clean:
        prog = prog_builder(cache[p]['steps'])
        l = lam(prog, acc_latch, read_bit)
        if abs(l-1) < 5e-4: loss += 1
        elif l > 1: hot.append(f"{p:#x}:{(l-1)*1e6:+.0f}" if abs(l-1) < 2 else f"{p:#x}:{l:.2f}x")
    return loss, len(clean), hot


def main():
    variants = [
        ("OLD       no-acclatch ", lambda steps: decode_old(steps), False, 1),
        ("FRONT l3=F cs2 acclatch", lambda steps: decode_front(steps, False, 2), True, 1),
        ("FRONT l3=F cs1 acclatch", lambda steps: decode_front(steps, False, 1), True, 1),
        ("FRONT l3=T cs1 acclatch", lambda steps: decode_front(steps, True, 1), True, 1),
        ("FRONT l3=F cs1 noacc   ", lambda steps: decode_front(steps, False, 1), False, 1),
        ("HYB l3=F cs1 z=l2b7 acc", lambda steps: decode_front(steps, False, 1, 'l2b7'), True, 1),
        ("HYB l3=T cs1 z=l2b7 acc", lambda steps: decode_front(steps, True, 1, 'l2b7'), True, 1),
    ]
    print("=" * 70)
    print("GATE A: diagnostic passthrough/echo (target ZD g~+1.0, MAX echo ~17065)")
    print("=" * 70)
    for name, b, acc, rb in variants:
        gate_a(name, b, acc, rb)
    if os.environ.get('SKIP_B'):
        return
    print("\n" + "=" * 70)
    print("GATE B: over-unity (all 13 clean programs lambda<=1)")
    print("=" * 70)
    print(f"{'variant':24s} {'#lossless':>9} {'hot':>4}  hot-list")
    for name, b, acc, rb in variants:
        loss, ntot, hot = gate_b(b, acc, rb)
        print(f"{name:24s} {loss:>4}/{ntot:<4} {len(hot):>4}  {' '.join(hot[:6])}")


if __name__ == '__main__':
    main()
