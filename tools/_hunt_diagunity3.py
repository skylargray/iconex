#!/usr/bin/env python3
"""Hypothesis test: what datapath semantics make ZERO DELAY = unity passthrough?

The committed aru_datapath model produces ZERO output for the diagnostics (no XFER step
=> RES never loads; no b3 => DAB never carries RES). That model literally cannot pass a
signal, so it cannot be the faithful diagnostic semantics. The manual GROUND TRUTH is:
  zero-delay: output == input  (unity).

We enumerate physically-plausible "what the FPC output step captures" hypotheses and see
which yields gain == 1 for zero-delay (and full-amplitude delayed impulse for .5s). The
gain that the WINNING hypothesis produces is the model's true passthrough gain; ANY
non-unity value would be the CONCERT over-unity scaling bug.

Datapath facts (tech ref 4): MAC runs EVERY ARUCKE edge: AC <- PP = sat20(AC +/- product),
or 0 if ZERO. RES (74F374) = PP[3..18] = ACC>>3, but only latched by XFER CK. DAB carries
RES only when RDRREG/ (b3) asserts; else DAB = DMEM read (or FPC input).

Coeff: C = (|coeff|>>1)/64. Multiplicand operand = x<<3. product = (operand*Cs)>>6.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import importlib.util
spec = importlib.util.spec_from_file_location("_hd", os.path.join(os.path.dirname(__file__), "_hunt_diagunity.py"))
_hd = importlib.util.module_from_spec(spec); spec.loader.exec_module(_hd)

DMASK = A.DMASK


def run_hyp(prog, ra_pick, nsamp, imp, hyp, mode='int'):
    """hyp controls how the FPC output (WA=3, bit15) step captures its output value:
       'res'      : current RES register   (committed model)
       'acc_xfer' : sat16(ACC>>3) at the step regardless of XFER (MAC visible w/o XFER latch)
       'x'        : the register read R[ra] at the step (raw, no multiply)
       'xC'       : R[ra]*C  (single multiply, the step's own coeff)
       'dab'      : the DAB driven into R[WA=3] this cycle
    Returns out_log dict {s: [values per sample]}.
    """
    if mode == 'int':
        R = [0,0,0,0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1)
    else:
        R = [0.0]*4; ACC = 0.0; RES = 0.0; DM = [0.0]*(DMASK+1)
    pos = 0
    in_step = A.fpc_input_step(prog)
    out_steps = [st['s'] for st in prog if st['WA'] == 3 and (st['offset'] & 0x8000)]
    out_log = {s: [] for s in out_steps}
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if in_step is not None and st['s'] == in_step:
                dab = imp if n == 0 else 0
            elif (st['offset'] & 0x8000) and st['WA'] == 3:
                # FPC output step: it is NOT a DMEM read; DAB source is undefined here.
                dab = 0
            else:
                dab = RES if st['b3'] else DM[addr]
            mag = abs(st['coeff']); csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            ra = ra_pick(st); x = R[ra]
            R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0 if mode == 'int' else 0.0
            if mode == 'int':
                ACC = A.sat20(ACC + (((x << 3) * Cs) >> 6))
                if st['XFER']:
                    RES = A.sat16(ACC >> 3)
                acc_xfer_val = A.sat16(ACC >> 3)
                xC_val = A.sat16((((x << 3) * Cs) >> 6) >> 3)
            else:
                ACC = ACC + x*8.0*Cs/64.0
                if st['XFER']:
                    RES = ACC/8.0
                acc_xfer_val = ACC/8.0
                xC_val = (x*8.0*Cs/64.0)/8.0
            if st['b3']:
                DM[addr] = RES
            if (st['offset'] & 0x8000) and st['WA'] == 3:
                if hyp == 'res':       outv = RES
                elif hyp == 'acc_xfer':outv = acc_xfer_val
                elif hyp == 'x':       outv = x
                elif hyp == 'xC':      outv = xC_val
                elif hyp == 'dab':     outv = dab
                else: outv = None
                out_log[st['s']].append(outv)
    return out_log


def summarize(prog, ra_pick, hyp, mode, imp, nsamp, label):
    out_log = run_hyp(prog, ra_pick, nsamp, imp, hyp, mode)
    rows = []
    for s, seq in out_log.items():
        nz = [(i, v) for i, v in enumerate(seq) if abs(v) > 1e-9]
        if not nz:
            rows.append(f"    step{s}: ALL ZERO")
            continue
        i0, v0 = nz[0]
        peak_i, peak_v = max(nz, key=lambda t: abs(t[1]))
        rows.append(f"    step{s}: first nz @n={i0} v={v0!r} gain={v0/imp:+.6f} | "
                    f"peak @n={peak_i} ({peak_i/34130.0*1000:.1f}ms) v={peak_v!r} gain={peak_v/imp:+.6f}")
    print(f"  [{label}] hyp={hyp} mode={mode}:")
    for r in rows: print(r)


if __name__ == '__main__':
    PICKS = {
        'RA=(b5,b4)': lambda st: (st['b5'] << 1) | st['b4'],
        'RA=(b5,b3)': lambda st: (st['b5'] << 1) | st['b3'],
        'RA=(b4,b3)': lambda st: (st['b4'] << 1) | st['b3'],
    }
    img0 = _hd.build_image(zero_delay=True)
    prog0 = _hd.decode(img0)
    imp = 20000
    print("================= ZERO DELAY: scan RA-pick x output-hypothesis =================")
    for pname, pick in PICKS.items():
        print(f"\n### RA pick = {pname}")
        for hyp in ('res', 'acc_xfer', 'x', 'xC', 'dab'):
            summarize(prog0, pick, hyp, 'int', imp, 300, f"ZERO {pname}")
