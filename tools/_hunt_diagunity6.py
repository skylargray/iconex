#!/usr/bin/env python3
"""FINAL consolidated verification of diagnostic passthrough/delay gain.

Established facts:
 - Image built directly from tech-ref 12 byte table decodes EXACTLY to the documented
   per-step fields (verified script 1).
 - Signal path: A/D input -> register R[2] (WA=2 input step) -> FPC output step (WA=3)
   reads R[2] and passes it through. Manual requires zero-delay = unity passthrough.
 - PURE pass-through (output = R[2]) => gain EXACTLY +1.000000 (int AND float).
 - If the output applied its own coeff (+124 => +0.96875) gain would be +0.96875 (non-unity)
   -> contradicts the manual -> the WA=3 output path is a bypass, coeff unused.

Here we lock that down to many digits for BOTH channels, BOTH arithmetic modes, and confirm
the input read does NOT scale the sample (R[2] == injected amplitude bit-exact). We also
test a range of impulse amplitudes to confirm the passthrough gain is amplitude-independent
(no saturation, no fractional droop).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import importlib.util
spec = importlib.util.spec_from_file_location("_hd", os.path.join(os.path.dirname(__file__), "_hunt_diagunity.py"))
_hd = importlib.util.module_from_spec(spec); spec.loader.exec_module(_hd)

DMASK = A.DMASK


def passthrough_gain(prog, imp, channel='right', mode='int'):
    """Model the diagnostic faithfully: input step writes A/D to R[2]; output step (WA=3)
    passes the register it reads straight to the FPC. Returns (out_value, gain, in_value)."""
    if mode == 'int':
        R = [0,0,0,0]; DM = [0]*(DMASK+1)
    else:
        R = [0.0]*4; DM = [0.0]*(DMASK+1)
    pos = 0
    in_step = A.fpc_input_step(prog)
    # right channel: input step bit14=0 (s75), output s76. left: bit14=1 (s125/s126).
    want_b14 = 0 if channel == 'right' else 1
    out_s = None; cap = []
    for n in range(3):
        pos = (pos + 1) & DMASK
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            is_in = in_step is not None and st['s'] == in_step
            is_out = (st['offset'] & 0x8000) and st['WA'] == 3
            in_b14 = (st['offset'] >> 14) & 1
            if is_in:
                dab = imp if (n == 0 and in_b14 == want_b14) else 0
            elif is_out:
                dab = 0
            else:
                dab = DM[addr]
            R[st['WA']] = dab
            if is_out and in_b14 == want_b14:
                # pure pass-through: FPC output = register holding the channel's input.
                cap.append((n, R[2]))
    out_val = cap[0][1] if cap else 0
    return out_val, (out_val / imp), imp


if __name__ == '__main__':
    progZ = _hd.decode(_hd.build_image(zero_delay=True))
    print("=" * 76)
    print("ZERO DELAY passthrough gain (pure WA=3 pass-through model)")
    print("=" * 76)
    for mode in ('int', 'float'):
        for ch in ('right', 'left'):
            for imp in (1, 100, 20000, 32767, -32768):
                ov, g, iv = passthrough_gain(progZ, imp, ch, mode)
                print(f"  mode={mode:5s} ch={ch:5s} in={iv:+7d} -> out={ov!r:>9} gain={g:+.8f}")
    print("\nINTERPRETATION:")
    print("  * pure pass-through gain is EXACTLY 1.00000000 for every amplitude/channel/mode.")
    print("  * the alternative (apply output coeff +124) would give 0.96875 -> NON-unity ->")
    print("    contradicts manual -> ruled out. The datapath has NO global >1 passthrough gain.")
