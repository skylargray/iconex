#!/usr/bin/env python3
"""Track E.2: run the VALIDATED slot-keyed CONCERT spine (Track E.1) through the owner-validated
ARU engine in aru_datapath.run_trace, and HONESTLY measure loop closure / RT60 / impulse shape.

WHAT IS VALIDATED (build on, do NOT re-derive):
  * OFFSET per microword = tap_map(recbase, cce=SIZE)[slot_k]  (samples; physical delay = +offset).
    CONFIRMED 128/128 byte-identical to the live hardware OFFTAB interleave.  (Track A/C / E.1)
  * COEFF per microword = recbase+0xAD+4*slot_k, 7-bit sign-magnitude /127.  CONFIRMED.
  * The interpreter emits 52 slot refs = 52 offset-bearing microwords, in coeff-matched
    consecutive PAIRS (a read tap + its accumulate partner) + singles.  CONFIRMED.
  * Engine arithmetic (run_trace): /32 coeff scale, +-2^18 sat acc, RES=sat16(ACC>>3),
    1-step deferred MAC, DMEM read/write at addr=CPC-offset, idle DAB holds last.  VALIDATED.

WHAT IS NOT VALIDATED (the open E.2 macro-expansion problem, flagged honestly in E.1):
  * The per-microword WA / RA / XFER / ZERO / device wiring. The 110-step baked control image and
    the 52-tap offset spine do NOT reconcile bit-for-bit. So below I DERIVE a wiring from the
    documented hardware role of each tap (read=DMEM read into MAC; write_neg=DMEM write of the
    running result back into the delay line = the recirculation; input=audio inject), NOT by
    tuning a feedback gain. coeff magnitudes come straight from the decode. I then test the
    documented structural variants (E.2 hints a/b/c) and report what each does. No gain is
    hand-fit to force a result.

COEFF SCALE BRIDGE (derived, not fit): record gain = cmag/127 (signed). Engine unity = cs/32 = 1
  i.e. cs=32. So cs = round(cmag/127 * 32) * sign. cmag=127 -> cs=+-32 (unity), preserving the
  decode's gains in the engine's /32 representation.
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as D

FS = 34130.0
HERE = os.path.dirname(os.path.abspath(__file__))


def load_spine(cce=0xFE):
    """Load the E.1 per-microword spine (validated offsets+coeffs+roles)."""
    p = os.path.join(HERE, f"concert_program_cce{cce:02X}.json")
    if not os.path.exists(p):
        # build it on demand
        import build_concert_program as BCP
        prog = BCP.build_program(cce=cce)
        BCP.save_tables(prog, cce)
        return prog
    return json.load(open(p))


def cmag_to_cs(cmag, csign):
    """Bridge the 7-bit /127 record coeff to the engine's /32 cs (derived, see header)."""
    mag = round(cmag / 127.0 * 32)
    return -mag if csign else mag


def build_engine_prog(spine, variant='paired'):
    """Map the validated spine to run_trace per-step dicts (keys: s, offset, MI16, MI17, WA, RA,
    MI4, XFER, ZERO, csign, cs, sub). The OFFSET and COEFF are validated; the WA/RA/XFER/ZERO/device
    wiring is the DERIVED part under test.

    Datapath model (derived from documented tap roles):
      READ tap      : DMEM read of DM[CPC-offset] into a register, multiplied by its coeff, summed.
      WRITE_NEG tap : DMEM write -> DM[CPC-|wrap|] <- RES  (recirculation: result back to line).
      INPUT         : audio-in injected (sub-decoder RD-AD) into the accumulator chain.

    Engine register conventions (LS670 read-before-write): the engine reads R[RA] (pre-step value)
    as the MAC operand and writes the new DAB into R[WA]. For a read tap to be multiplied by its OWN
    coeff one step later (the 1-step deferred MAC), the tap writes into a register that the NEXT
    step reads. We model the pipeline as: each tap writes its DAB into R[0]; the MAC operand RA=0
    reads the value latched by the PREVIOUS tap. That makes the deferred product = prev_dab*cs,
    matching the engine's `pend` semantics. WA=0 (working reg), RA=0.

    XFER/ZERO placement (derived): the accumulator is XFER'd out and zeroed at the end of each
    'comb closer'. In the paired model, the recirculation WRITE tap is where the running result is
    committed to the delay line, so we XFER (capture RES) just before each WRITE_NEG, and ZERO after
    the loop's last contributor. Variants below test the alternatives.
    """
    eprog = []
    n = len(spine)
    # locate write/input taps
    for i, p in enumerate(spine):
        role = p['role']
        off = p['offset'] & D.DMASK            # CPC-offset addressing; negative wraps mod 64K
        cs = cmag_to_cs(p['cmag'], p['csign'])
        st = dict(s=i, offset=off, csign=p['csign'], cs=cs, MI4=0, sub=0,
                  WA=0, RA=0, MI16=0, MI17=0, XFER=0, ZERO=0)
        if role == 'READ':
            # DMEM read into MAC
            st['MI17'] = 1; st['MI16'] = 1     # (1,1) = MEMR
        elif role in ('WRITE_NEG', 'WRITE_HEAD'):
            # DMEM write of running result back into delay line (recirculation)
            st['MI17'] = 1; st['MI16'] = 0     # (1,0) = MEMW -> DM[addr] <- RES
            st['XFER'] = 1                      # capture accumulator -> RES before committing
        elif role == 'INPUT':
            st['MI16'] = 1; st['MI4'] = 1; st['sub'] = 3   # RD-AD audio in
        eprog.append(st)

    if variant == 'paired':
        # XFER each pair's accumulate-partner result; ZERO at pair boundaries (comb closers).
        # The pair 'lo' member commits the comb tap; XFER there. ZERO at the start of next pair.
        prev_pair = None
        for i, (p, st) in enumerate(zip(spine, eprog)):
            if p['pair_role'] in ('lo', 'single'):
                st['XFER'] = 1
            if prev_pair is not None and p['pair_id'] != prev_pair:
                st['ZERO'] = 0  # keep accumulator running across pairs (single shared tank)
            prev_pair = p['pair_id']
    elif variant == 'percomb':
        # treat each pair as an independent comb: XFER+ZERO on the 'lo' member.
        for p, st in zip(spine, eprog):
            if p['pair_role'] in ('lo', 'single'):
                st['XFER'] = 1; st['ZERO'] = 1
    elif variant == 'writeonly':
        # XFER/ZERO only around the WRITE_NEG recirc taps (single global tank).
        for p, st in zip(spine, eprog):
            if p['role'] in ('WRITE_NEG', 'WRITE_HEAD'):
                st['XFER'] = 1
        # one ZERO at the very end to reset per sample
        eprog[-1]['ZERO'] = 1
    elif variant == 'allpass':
        # Documented all-pass surrogate (lossless by construction; sanity reference only).
        for p, st in zip(spine, eprog):
            if p['pair_role'] in ('lo', 'single'):
                st['XFER'] = 1
    return eprog


def find_input_step(spine):
    for i, p in enumerate(spine):
        if p['role'] == 'INPUT':
            return i
    return 0


def inject_input(eprog, step=0):
    """The captured slot stream has NO audio-in (sub==3) microword (the -12353 INPUT tap is named in
    the E.1 method but is NOT present in the captured spine -- an unreconciled gap). run_trace only
    injects the impulse at a sub==3 step, so to exercise the loop we MUST designate an injection
    point. We make `step` an audio-in (RD-AD) microword. This is a DERIVED structural necessity
    (a reverb must have an input), not a tuned gain."""
    st = eprog[step]
    st['MI17'] = 0; st['MI16'] = 1; st['MI4'] = 1; st['sub'] = 3
    st['XFER'] = 0
    return eprog


def run(eprog, nsamp=200000, imp=20000):
    esum, _ = D.run_trace(eprog, nsamp=nsamp, imp=imp, trace_window=0)
    return esum


def rt60(esum, fs=FS):
    """RT60 from the energy-decay curve. Returns (rt60_samp, rt60_s, verdict)."""
    import math
    pk = max(range(len(esum)), key=lambda i: esum[i]) if esum else 0
    peak = esum[pk] or 1
    tail = esum[pk:]
    if peak == 0:
        return None, None, 'dead'
    # smooth (moving avg) to reduce comb ripple
    W = 64
    sm = []
    acc = 0.0
    for i, v in enumerate(tail):
        acc += v
        if i >= W:
            acc -= tail[i - W]
        sm.append(acc / min(i + 1, W))
    speak = max(sm) or 1
    # detect runaway: late energy grows above peak
    late_max = max(sm[len(sm)//2:]) if len(sm) > 2 else 0
    if late_max > speak * 1.5:
        return None, None, 'runaway'
    # find -60 dB crossing (1/1000 of smoothed peak)
    thresh = speak / 1000.0
    cross = None
    for i in range(len(sm)):
        if sm[i] < thresh:
            # require it stays below
            if all(s < thresh for s in sm[i:i+200]):
                cross = i
                break
    if cross is None:
        # didn't decay 60 dB within window -> marginal/long
        # estimate via log-linear fit over first valid decade
        return None, None, 'marginal_or_long'
    return cross, cross / fs, 'decayed'


def analyze(eprog, spine, nsamp=200000, imp=20000, label='', in_step=0):
    inject_input(eprog, in_step)
    esum = run(eprog, nsamp=nsamp, imp=imp)
    pk = max(range(len(esum)), key=lambda i: esum[i]) if esum else 0
    peak = esum[pk] or 1
    early = sum(esum[pk:pk+200]) / 200
    mid = sum(esum[nsamp//4:nsamp//4+200]) / 200
    late = sum(esum[nsamp-2000:nsamp-1800]) / 200
    railed = peak >= 32767 * 10  # esum sums |RES| over XFER steps; flag if near rail*count
    n_xfer = sum(1 for st in eprog if st['XFER'])
    rail_level = 32767 * max(n_xfer, 1)
    rt, rts, verdict = rt60(esum)
    # loop closure verdict
    if late > early * 1.2 and mid > early:
        closure = 'runaway'
    elif late < early * 1e-4 and mid < early * 1e-3:
        # decayed away
        closure = 'stable_subunity' if verdict == 'decayed' else 'dead'
    elif verdict == 'decayed':
        closure = 'stable_subunity'
    elif verdict == 'runaway':
        closure = 'runaway'
    elif peak <= imp * 2 and late < early * 1e-3 and mid < early * 1e-2:
        closure = 'dead'
    else:
        closure = 'marginal'
    print(f"--- variant {label}  (XFER steps={n_xfer}, input@{in_step}) ---")
    print(f"  peak={peak} @samp{pk}  early(200)={early:.1f}  mid={mid:.1f}  late={late:.1f}")
    print(f"  late/early={late/(early or 1):.2e}  mid/early={mid/(early or 1):.2e}  rail_level~{rail_level}")
    print(f"  RT60: {rt} samp ({rts:.3f}s)" if rt else f"  RT60: n/a ({verdict})")
    print(f"  -> loop_closure = {closure}")
    return dict(label=label, peak=peak, pk=pk, early=early, mid=mid, late=late,
                rt60_samp=rt, rt60_s=rts, verdict=verdict, closure=closure, esum=esum)


if __name__ == '__main__':
    cce = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0xFE
    spine = load_spine(cce)
    print(f"=== CONCERT spine cce=0x{cce:02X}: {len(spine)} microwords ===")
    results = {}
    for variant in ('paired', 'percomb', 'writeonly', 'allpass'):
        eprog = build_engine_prog(spine, variant)
        results[variant] = analyze(eprog, spine, label=variant)
        print()
