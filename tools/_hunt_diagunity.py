#!/usr/bin/env python3
"""Ground-truth gain via the ZERO DELAY / .5 S DELAY diagnostic WCS images.

Builds the two minimal diagnostic programs DIRECTLY from the decoded byte table in
tech ref section 12 (no firmware boot needed), decodes them with the SAME logic as
aru_datapath.load_microcode, runs an impulse through aru_datapath.run, and measures:
  (a) ZERO DELAY  -> passthrough gain (output/input), should be EXACTLY unity if no scaling bug.
  (b) .5 S DELAY  -> impulse reappears ~17065 samples later at full amplitude (gain ~1).

ANY deviation of the passthrough/delay-line gain from unity is the CONCERT over-unity smoking gun.
Exact unity points AWAY from a global datapath scaling bug.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK

# ---------------------------------------------------------------------------
# Build the 512-byte WCS image directly from tech ref section 12 byte table.
# Each step s occupies bytes img[s*4 .. s*4+3] = (l0, l1, l2, l3).
# Table rows give l0 l1 l2 l3 for steps 74-77 (RIGHT) and 124-127 (LEFT).
# Plus step 29 patch: 0x4074=0xF7, 0x4076=0xFE  (l0=0xF7, l2=0xFE; l1,l3 stay 0xFF).
# ZERO DELAY = identical to MAX except step 76 offset->0xBFFE, step 126 offset->0xFFFE
#   (i.e. low14 of those WA=3 output steps changes; offset=~(l1<<8|l0)).
# ---------------------------------------------------------------------------

# MAX (.5 s DELAY) decoded byte rows: step -> (l0,l1,l2,l3)
MAX_ROWS = {
    74:  (0x7f, 0xe9, 0xfe, 0xff),
    75:  (0x00, 0x40, 0xfd, 0xfe),
    76:  (0xff, 0x7f, 0xfc, 0x7c),
    77:  (0xff, 0xcf, 0xfe, 0x7d),
    124: (0x7f, 0xe6, 0xfe, 0xff),
    125: (0x00, 0x00, 0xfd, 0xfe),
    126: (0xff, 0x3f, 0xfc, 0x7c),
    127: (0xff, 0xcf, 0xfe, 0x7d),
}
# step 29 patch bytes
PATCH29 = {0x74: 0xF7, 0x76: 0xFE}   # absolute byte addresses within 0x4000.. region


def build_image(zero_delay=False):
    """Return a 512-byte bytearray for the diagnostic WCS, default 0xFF (all NOP)."""
    img = bytearray([0xFF] * 512)
    rows = dict(MAX_ROWS)
    if zero_delay:
        # ZERO DELAY: step 76 offset 0x8000 -> 0xBFFE ; step 126 offset 0xC000 -> 0xFFFE.
        # offset = ~(l1<<8 | l0) & 0xFFFF  =>  l1<<8|l0 = ~offset & 0xFFFF.
        # MAX step76: l0=0xff,l1=0x7f -> raw=0x7fff -> offset=0x8000. Want offset=0xBFFE.
        #   raw = ~0xBFFE & 0xFFFF = 0x4001 -> l0=0x01, l1=0x40.
        # MAX step126: l0=0xff,l1=0x3f -> raw=0x3fff -> offset=0xC000. Want offset=0xFFFE.
        #   raw = ~0xFFFE & 0xFFFF = 0x0001 -> l0=0x01, l1=0x00.
        l0a, l1a, l2a, l3a = rows[76]
        rows[76] = (0x01, 0x40, l2a, l3a)
        l0b, l1b, l2b, l3b = rows[126]
        rows[126] = (0x01, 0x00, l2b, l3b)
    for s, (l0, l1, l2, l3) in rows.items():
        img[s*4 + 0] = l0
        img[s*4 + 1] = l1
        img[s*4 + 2] = l2
        img[s*4 + 3] = l3
    # step 29 patch (byte addresses relative to 0x4000)
    for boff, val in PATCH29.items():
        img[boff] = val
    return img


def decode(img):
    """Decode the 512-byte image with the SAME logic as aru_datapath.load_microcode."""
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
        prog.append(dict(s=s, offset=offset, coeff=coeff,
                         ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1, XFER=(ctl >> 2) & 1,
                         WA=ctl & 3, b5=(ctl >> 5) & 1, b4=(ctl >> 4) & 1))
    return prog


PICK = lambda st: (st['b5'] << 1) | st['b4']


def dump(prog, name):
    print(f"\n=== decoded program: {name} ({len(prog)} active steps) ===")
    print(" s  | offset  b15 b14 low14 | WA b5 b4 b3 ZERO XFER | coeff   C=mag>>1/64")
    for st in prog:
        off = st['offset']
        C = (abs(st['coeff']) >> 1) / 64.0
        Cs = -C if st['coeff'] < 0 else C
        print(f"{st['s']:3d} | 0x{off:04X}  {(off>>15)&1}   {(off>>14)&1}  0x{off&0x3FFF:04X} "
              f"| {st['WA']}  {st['b5']}  {st['b4']}  {st['b3']}   {st['ZERO']}    {st['XFER']}  "
              f"| {st['coeff']:+4d}   {Cs:+.5f}")


# ---------------------------------------------------------------------------
# Custom impulse runner that records the FPC-output (WA=3) signal directly,
# so we can read true passthrough/delay gain (not the energy-sum probe in run()).
# Mirrors aru_datapath.run datapath bit-for-bit.
# ---------------------------------------------------------------------------
def run_capture(prog, ra_pick, nsamp, imp, mode='int'):
    """Run an impulse; capture the value DRIVEN onto each FPC output (WA=3, bit15) step
    each sample. Returns dict: out_per_step[s] = list over samples of the RES driven out,
    plus the captured input sample fed onto each FPC-input read step.
    mode='int' -> exact aru_datapath integer datapath; mode='float' -> exact float."""
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    if mode == 'int':
        DM = [0] * (DMASK + 1)
    else:
        DM = [0.0] * (DMASK + 1)
        R = [0.0, 0.0, 0.0, 0.0]; ACC = 0.0; RES = 0.0
    pos = 0
    in_step = A.fpc_input_step(prog)
    out_steps = [st['s'] for st in prog if st['WA'] == 3 and (st['offset'] & 0x8000)]
    out_log = {s: [] for s in out_steps}
    in_log = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        in_this = None
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            if in_step is not None and st['s'] == in_step:
                dab = imp if n == 0 else 0
                in_this = dab
            else:
                dab = RES if st['b3'] else DM[addr]
            mag = abs(st['coeff'])
            csign = st['coeff'] < 0
            Cs = -(mag >> 1) if csign else (mag >> 1)
            ra = ra_pick(st)
            x = R[ra]
            R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0 if mode == 'int' else 0.0
            if mode == 'int':
                operand = x << 3
                prod = (operand * Cs) >> 6
                ACC = A.sat20(ACC + prod)
                if st['XFER']:
                    RES = A.sat16(ACC >> 3)
            else:
                ACC = ACC + x * 8.0 * Cs / 64.0
                if st['XFER']:
                    RES = ACC / 8.0
            if st['b3']:
                DM[addr] = RES
            if st['WA'] == 3 and (st['offset'] & 0x8000):
                # value driven to the FPC output for this step = current RES on the DAB
                out_log[st['s']].append(RES)
        if in_this is not None:
            in_log.append(in_this)
    return out_log, in_log, in_step, out_steps


def analyze_zero_delay(mode='int'):
    img = build_image(zero_delay=True)
    prog = decode(img)
    dump(prog, f"ZERO DELAY ({mode})")
    imp = 20000
    nsamp = 200
    out_log, in_log, in_step, out_steps = run_capture(prog, PICK, nsamp, imp, mode=mode)
    print(f"\n  in_step (FPC input read) = {in_step}; FPC output steps (WA=3,bit15) = {out_steps}")
    print(f"  injected impulse amplitude = {imp}")
    for s in out_steps:
        seq = out_log[s]
        # find first nonzero output sample and its value
        nz = [(i, v) for i, v in enumerate(seq) if abs(v) > 1e-12]
        if nz:
            i0, v0 = nz[0]
            print(f"  output step {s}: first nonzero at sample {i0}, value={v0!r}, "
                  f"gain={v0/imp:+.8f}")
            # show first few output samples
            print(f"    out[{s}][0:6] = {[round(x,6) if mode=='float' else x for x in seq[:6]]}")
        else:
            print(f"  output step {s}: ALL ZERO over {nsamp} samples")
    return prog, out_log, in_log, out_steps, imp


def analyze_half_sec(mode='int'):
    img = build_image(zero_delay=False)
    prog = decode(img)
    dump(prog, f".5 S DELAY ({mode})")
    imp = 20000
    nsamp = 40000
    out_log, in_log, in_step, out_steps = run_capture(prog, PICK, nsamp, imp, mode=mode)
    print(f"\n  in_step (FPC input read) = {in_step}; FPC output steps (WA=3,bit15) = {out_steps}")
    print(f"  injected impulse amplitude = {imp}; target delay ~17065 samples (0.5s @ 34130 Hz)")
    for s in out_steps:
        seq = out_log[s]
        nz = [(i, v) for i, v in enumerate(seq) if abs(v) > (imp * 0.01)]
        if nz:
            # report the largest-magnitude output after sample 100 (the delayed impulse)
            late = [(i, v) for i, v in nz if i > 100]
            if late:
                i_peak, v_peak = max(late, key=lambda t: abs(t[1]))
                print(f"  output step {s}: delayed impulse peak at sample {i_peak} "
                      f"(={i_peak/34130.0*1000:.2f} ms), value={v_peak!r}, gain={v_peak/imp:+.8f}")
            else:
                print(f"  output step {s}: nonzero outputs only early: {nz[:5]}")
        else:
            print(f"  output step {s}: no significant output > 1% over {nsamp} samples")
    return prog, out_log, in_log, out_steps, imp


if __name__ == '__main__':
    print("#" * 78)
    print("# ZERO DELAY diagnostic -> expect UNITY passthrough (output == input)")
    print("#" * 78)
    analyze_zero_delay(mode='int')
    analyze_zero_delay(mode='float')

    print("\n" + "#" * 78)
    print("# .5 S DELAY diagnostic -> expect impulse delayed ~17065 samples at full amplitude")
    print("#" * 78)
    analyze_half_sec(mode='int')
    analyze_half_sec(mode='float')
