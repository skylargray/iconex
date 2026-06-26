#!/usr/bin/env python3
"""Track E.2-BUILD: the COMPLETE per-microword CONCERT program, every field firmware-derived
from the LIVE mem[0x4000] image (the authoritative hardware microword the ARU/T&C executes).

KEY CORRECTIONS over aru_datapath2.py (the WA=0/RA=0 surrogate that went over-unity):
  * WA / RA / XFER / ZERO / device / CSIGN / coeff come from the live 0x4000 lanes 2,3 (owner field
    map; decode_image already does this and agrees 128/128 with the baked recbase+0x2A9 control
    table -- Track E2b). NO hard-coded WA=0/RA=0.
  * The DELAY OFFSET is decoded RAW (l0 | l1<<8), NOT inverted. decode_image uses ~(l0|l1<<8),
    which is the source of the Session-11/Track-E "30000-sample garbage". RAW matches tap_map
    88/110 (102/110 by the verifier). This is the load-bearing E2a/E2b correction.
  * MI4 (the sub-decoder gate = offset bit4) is taken from the INVERTED lane0 (~l0 bit4), the
    convention under which the device histogram reproduces the validated 8/10/11/3/4/74 split
    (DMEM-READ/WRITE / RD-AD / RDRREG / RD-XREG / HOLD). So lane0 has TWO firmware uses: the RAW
    16-bit delay offset, and the inverted-bit4 MI4 gate. Both are ROM-derived, not fitted.
  * For the 5 structural head steps s0-s4 (lane0 repacked to 0x89) the RAW offset is meaningless;
    they are input-routing steps (audio injection happens at the RD-AD steps anyway).

CARDINAL RULE: every field here is read straight from the live ROM-assembled 0x4000 image. The
only "model" choices are (a) which CSIGN polarity convention the engine uses (tested BOTH ways,
A/B reported) and (b) the coeff scale bridge cmag(6-bit /32)->engine cs (the live lane already
carries a 6-bit /32 coeff, so cs = cmag directly -- no /127 round-trip, no fit).
"""
import sys, os, math
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B
import aru_datapath as D

FS = 34130.0
DMASK = 0xFFFF


def build_live_program(power_up_id=0x01, csign_pos=False):
    """Decode the live 0x4000 image into a complete per-microword program for run_trace.

    csign_pos=False : aru_datapath convention CSIGN=1 -> NEGATIVE coeff (cs = -cmag if csign).
    csign_pos=True  : Track B / POST convention CSIGN=1 -> POSITIVE coeff (cs = +cmag if csign,
                      -cmag if not).  A/B tested below.

    Returns (prog, meta) where prog is the run_trace step list and meta carries per-step provenance.
    """
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = []
    meta = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        # --- lane2 (owner map, used DIRECT) : device / WA / RA / CSIGN ---
        MI16 = l2 & 1
        MI17 = (l2 >> 1) & 1
        WA = (l2 >> 2) & 3
        RA = (l2 >> 4) & 3
        csign = (l2 >> 7) & 1
        # --- lane3 (used COMPLEMENTED) : XFER / ZERO / 6-bit coeff mag ---
        v3 = (~l3) & 0xFF
        xfer = v3 & 1
        zero = (v3 >> 1) & 1
        cmag = (v3 >> 2) & 0x3F
        # --- lane1 (used COMPLEMENTED bits 4,5) : sub-decoder MI12,MI13 ---
        vl1 = (~l1) & 0xFF
        MI12 = (vl1 >> 4) & 1
        MI13 = (vl1 >> 5) & 1
        sub = (MI13 << 1) | MI12
        # --- offset: RAW for delay addressing; MI4 from INVERTED lane0 bit4 (sub-decoder gate) ---
        off_raw = (l0 | (l1 << 8)) & DMASK
        MI4 = ((~l0) & 0xFF >> 4) & 1   # = (~l0 bit4); the DP/sub-gate bit
        MI4 = (((~l0) & 0xFF) >> 4) & 1
        repacked = (l0 == 0x89)
        # coeff scale: live lane carries 6-bit /32 coeff. engine unity = cs/32=1 -> cs=cmag.
        if csign_pos:
            cs = cmag if csign else -cmag       # Track B: CSIGN=1 -> POSITIVE
        else:
            cs = -cmag if csign else cmag       # aru_datapath: CSIGN=1 -> NEGATIVE
        st = dict(s=s, offset=off_raw, MI16=MI16, MI17=MI17, WA=WA, RA=RA, MI4=MI4,
                  XFER=xfer, ZERO=zero, csign=csign, cs=cs, sub=sub)
        prog.append(st)
        meta.append(dict(s=s, off_raw=off_raw, repacked=repacked, cmag=cmag,
                         dev=(MI17, MI16), WA=WA, RA=RA, sub=sub, csign=csign,
                         XFER=xfer, ZERO=zero))
    return prog, meta


def role_of(st):
    if st['MI17'] == 1 and st['MI16'] == 1:
        return 'DMEM_READ'
    if st['MI17'] == 1:
        return 'DMEM_WRITE'
    if st['MI16'] == 1 and st['MI4'] == 1:
        return {1: 'RDRREG', 3: 'RD_AD', 2: 'RD_XREG', 0: 'idle'}[st['sub']]
    return 'HOLD'


def role_histogram(prog):
    return dict(Counter(role_of(st) for st in prog))


def find_audio_in_steps(prog):
    return [i for i, st in enumerate(prog) if role_of(st) == 'RD_AD']


# ---------------------------------------------------------------------------
# Loop-gain analysis: round-trip recirculation gain from the recirc DMEM-WRITE
# back through every DMEM-READ that reads its address, times the section coeffs.
# Purely diagnostic (read off the decoded coeffs), never fed back into the engine.
# ---------------------------------------------------------------------------
def _sd(o):
    """signed delay: offset>32768 => write-ahead (head pointer, negative); else read-behind."""
    return o - 65536 if o > 32768 else o


def recirc_loop_gain(prog):
    """The recirculation is NOT same-address: a DMEM-WRITE stores RES at a write-HEAD pointer
    (signed delay negative, ~ -4097..-12353 = ahead of CPC); a DMEM-READ taps the line at a
    positive delay BEHIND the head. The comb loop length = read_delay - write_delay (samples), and
    the loop GAIN is the read tap's |cs|/32 (the write commits RES at unity). We report, per read
    tap, the nearest plausible write head it pairs with and the loop length + tap gain."""
    reads = [(i, st['offset'], st['cs']) for i, st in enumerate(prog) if role_of(st) == 'DMEM_READ']
    writes = [(i, st['offset']) for i, st in enumerate(prog) if role_of(st) == 'DMEM_WRITE']
    loops = []
    for ri, ro, rcs in reads:
        rd = _sd(ro)
        if rd <= 0:
            continue
        # the dominant write head (most common headdelay = -4097, four writes)
        best = None
        for wi, wo in writes:
            L = rd - _sd(wo)
            if best is None or abs(L) < abs(best[2]):
                best = (wi, wo, L)
        L = best[2]
        loops.append(dict(read_step=ri, read_delay=rd, write_step=best[0],
                          loop_samp=L, loop_ms=round(L / FS * 1000, 1),
                          tap_gain=round(rcs / 32.0, 4)))
    return loops


def rt60(esum, fs=FS):
    if not esum:
        return None, None, 'dead'
    pk = max(range(len(esum)), key=lambda i: esum[i])
    peak = esum[pk]
    if peak == 0:
        return None, None, 'dead'
    tail = esum[pk:]
    W = 64
    sm = []
    acc = 0.0
    for i, v in enumerate(tail):
        acc += v
        if i >= W:
            acc -= tail[i - W]
        sm.append(acc / min(i + 1, W))
    speak = max(sm) or 1
    late_max = max(sm[len(sm)//2:]) if len(sm) > 2 else 0
    if late_max > speak * 1.5:
        return None, None, 'runaway'
    thresh = speak / 1000.0
    for i in range(len(sm)):
        if sm[i] < thresh and all(s < thresh for s in sm[i:i+200]):
            return i, i / fs, 'decayed'
    return None, None, 'marginal_or_long'


def analyze(prog, label='', nsamp=200000, imp=20000):
    esum, _ = D.run_trace(prog, nsamp=nsamp, imp=imp, trace_window=0)
    pk = max(range(len(esum)), key=lambda i: esum[i]) if esum else 0
    peak = esum[pk] or 1
    early = sum(esum[pk:pk+200]) / 200
    mid = sum(esum[nsamp//4:nsamp//4+200]) / 200
    late = sum(esum[nsamp-2000:nsamp-1800]) / 200
    rt, rts, verdict = rt60(esum)
    if verdict == 'runaway' or (late > early * 1.2 and mid > early):
        closure = 'runaway'
    elif verdict == 'decayed':
        closure = 'stable_subunity'
    elif peak <= imp * 1.5 and late < early * 1e-3:
        closure = 'dead'
    elif late > early * 0.5:
        closure = 'marginal'
    else:
        closure = 'marginal'
    print(f"--- {label} ---")
    print(f"  peak={peak:.0f} @samp{pk}  early={early:.1f} mid={mid:.1f} late={late:.1f}")
    print(f"  late/early={late/(early or 1):.3e} mid/early={mid/(early or 1):.3e}")
    print(f"  RT60: {rt} samp ({rts:.3f}s)" if rt else f"  RT60: n/a ({verdict})")
    print(f"  -> closure = {closure}")
    return dict(label=label, peak=peak, pk=pk, early=early, mid=mid, late=late,
                rt60_samp=rt, rt60_s=rts, verdict=verdict, closure=closure, esum=esum)


if __name__ == '__main__':
    print("=== live 0x4000 CONCERT program (RAW offset, lane2/3 owner decode) ===")
    for pos in (False, True):
        conv = 'CSIGN=1->POS (Track B)' if pos else 'CSIGN=1->NEG (aru_datapath)'
        prog, meta = build_live_program(csign_pos=pos)
        print(f"\n##### convention: {conv}  ({len(prog)} microwords) #####")
        print("  roles:", role_histogram(prog))
        ain = find_audio_in_steps(prog)
        print(f"  RD-AD audio-in steps: {ain[:8]}{'...' if len(ain)>8 else ''} (n={len(ain)})")
        loops = recirc_loop_gain(prog)
        print("  recirc comb loops (read_step, loop_ms, tap_gain):")
        for lp in sorted(loops, key=lambda x: x['loop_ms']):
            print(f"    read s{lp['read_step']:3d} delay={lp['read_delay']:6d} "
                  f"loop={lp['loop_samp']:6d} samp ({lp['loop_ms']:6.1f} ms) tap_gain={lp['tap_gain']:+.3f}")
        analyze(prog, label=conv)
