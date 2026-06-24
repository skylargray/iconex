#!/usr/bin/env python3
"""Pin the exact microword byte-inversions / DMEM read-write polarity using the DIAGNOSTIC
programs as ground truth: ZERO-DELAY must be a UNITY passthrough; MAX-DELAY a 0.5 s delay,
also unity. The over-unity eigenvalue test is satisfied by several inversion combos; only the
physically-correct one reproduces the diagnostics' known gain/delay.

Signal-path model (corrected decode): the FPC I/O is addressed by offset bit15:
  - input step  = offset bit15 set AND low14==0x3FFF  -> A/D sample drives the DAB (impulse @ n=0)
  - other bit15-set steps = FPC/device (D/A out etc.) -> result reg drives DAB; we capture RES here
  - bit15-clear + dmem_op + read  -> DAB = DMEM[addr]
  - bit15-clear + dmem_op + write -> DMEM[addr] = RES (result reg)
  - else -> DAB = result reg
acc_latch timing (manual-confirmed). Reports the passthrough gain (and delay sample) per inversion config.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_diagunity as D
import _hunt_rebuild as RB
MASK = 0xFFFF


def diag_steps(zero_delay):
    img = D.build_image(zero_delay=zero_delay)
    steps = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        steps.append((s, l0, l1, l2, l3))
    return steps


def run_impulse(prog, read_val, nsamp, imp=20000.0):
    """Returns (out_seq) where out_seq[n] = sum of RES driven onto FPC-output (bit15) steps
    that are NOT the input step. Input impulse injected at the input fingerprint step, n=0."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0; ACCc = 0.0
    DM = [0.0]*(MASK+1); pos = 0
    in_s = None
    for st in prog:
        if (st['offset'] & 0x8000) and (st['offset'] & 0x3FFF) == 0x3FFF:
            in_s = st['s']; break
    out = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        osum = 0.0
        for st in prog:
            off = st['offset']; addr = (pos - off) & MASK
            is_fpc = bool(off & 0x8000)
            is_input = (st['s'] == in_s)
            is_read = (not is_fpc) and st['dmem_op'] and (st['dmem_rw'] == read_val)
            is_write = (not is_fpc) and st['dmem_op'] and not is_read
            if is_input:
                dab = imp if n == 0 else 0.0
            elif is_read:
                dab = DM[addr]
            else:
                dab = RES                                  # result reg drives (FPC-out or default)
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']: RES = ACCc / 8.0                # acc_latch
            if is_write: DM[addr] = RES
            ACCc = ACC
            if is_fpc and not is_input:                    # FPC output device step
                osum += RES
        out.append(osum)
    return out, in_s


def main():
    import itertools
    print("DIAGNOSTIC PIN: passthrough gain (ZERO-DELAY) + delay (MAX-DELAY) per inversion config")
    print("target: ZERO-DELAY gain=+1.000 at sample 0; MAX-DELAY gain~+1.0 at a late sample\n")
    print(f"{'inv2':5s} {'inv3':5s} {'readVal':7s}  {'ZD gain@0':>10s}  {'ZD peak':>16s}   {'MAX peak(late)':>22s}")
    for inv2, inv3, read_val in itertools.product((True, False), (True, False), (0, 1)):
        zd = RB.decode(diag_steps(True), inv2, inv3)
        md = RB.decode(diag_steps(False), inv2, inv3)
        zout, _ = run_impulse(zd, read_val, nsamp=300)
        mout, _ = run_impulse(md, read_val, nsamp=40000)
        g0 = zout[0] / 20000.0
        # ZD: peak over first samples
        zpk_i = max(range(len(zout)), key=lambda i: abs(zout[i]))
        zpk = zout[zpk_i] / 20000.0
        # MAX: peak after sample 100 (the delayed echo)
        late = [(i, v) for i, v in enumerate(mout) if i > 100]
        mpk_i, mpk_v = max(late, key=lambda t: abs(t[1])) if late else (0, 0.0)
        print(f"{str(inv2):5s} {str(inv3):5s} {read_val:7d}  {g0:+10.4f}  "
              f"{zpk:+.4f}@{zpk_i:<4d}     {mpk_v/20000.0:+.4f}@{mpk_i}")
    print("\n  The physically-correct config = ZD gain +1.000 at sample 0 AND MAX a unity echo at ~17065.")


if __name__ == '__main__':
    main()
