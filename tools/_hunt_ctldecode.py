#!/usr/bin/env python3
"""HUNT ANGLE: wrong control-field decode.

ctl = (~lane2)&0xFF.  Current decode:
    b7=ZERO  b6=PROTECT(ignored)  b5,b4=RA(pick)  b3=b3(DAB src/DMEM-wr)  b2=XFER  b1,b0=WA

The RA assignment (b5<<1|b4) was historically chosen by 'looks coherent' yet the resulting
linear map GROWS (+1128 ppm). This script re-decodes the control byte under many plausible
alternative field maps and measures the float-exact recirculation eigenvalue (lambda) for each.

We keep offset/coeff fixed (those are separate lanes, schematic-confirmed) and vary only the
interpretation of the 6 used ctl bits {b7..b0} (b6 left as PROTECT/ignored in the base map,
but also swept).

For each variant: compute float lambda (ppm) AND an integer impulse-response sanity check
(peak / late_ratio / blown) so we can flag decoders that DECAY *and* are structurally coherent.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B
import aru_datapath as A

DMASK = A.DMASK


def load_ctl_prog(power_up_id=0x01):
    """Like A.load_microcode but keep the raw ctl byte + offset + coeff."""
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
        prog.append(dict(s=s, offset=offset, coeff=coeff, ctl=ctl))
    return prog


def bit(ctl, i):
    return (ctl >> i) & 1


# A "decode" is a dict of callables on the raw ctl byte:
#   pick(ctl)->0..3 (RA), wa(ctl)->0..3, zero(ctl)->0/1, b3(ctl)->0/1, xfer(ctl)->0/1


def lam_decode(prog, dec, nsamp=20000, K=128, seed=1e4):
    """Float-exact linear-map eigenvalue under an arbitrary field decode.
    Mirrors exp_lambda_clean.lambda_trajectory's datapath exactly, but the field
    selectors come from `dec`. Returns converged lambda (median of last 60 windows)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    pick = dec['pick']; wa = dec['wa']; zero = dec['zero']; b3f = dec['b3']; xfer = dec['xfer']
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            ctl = st['ctl']
            addr = (pos - st['offset']) & DMASK
            dab = RES if b3f(ctl) else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[pick(ctl)]; R[wa(ctl)] = dab
            if zero(ctl): ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if xfer(ctl): RES = ACC/8.0
            if b3f(ctl): DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-60:]);
    return tail[len(tail)//2] if tail else float('nan')


def impulse_sanity(prog, dec, nsamp=4000, imp=20000):
    """Integer (saturating) impulse response -> peak, early/late energy, blown?
    Uses the same datapath as aru_datapath.run but with the arbitrary decode.
    Returns dict(peak, early, late, late_ratio, blown)."""
    R = [0, 0, 0, 0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1); pos = 0
    out = []
    pick = dec['pick']; wa = dec['wa']; zero = dec['zero']; b3f = dec['b3']; xfer = dec['xfer']
    for n in range(nsamp):
        pos = (pos+1) & DMASK; esum = 0
        for st in prog:
            ctl = st['ctl']
            addr = (pos - st['offset']) & DMASK
            dab = RES if b3f(ctl) else DM[addr]
            if n == 0 and st is prog[0]: dab += imp
            mag = abs(st['coeff']); Cs = -(mag >> 1) if st['coeff'] < 0 else (mag >> 1)
            x = R[pick(ctl)]; R[wa(ctl)] = dab
            if zero(ctl): ACC = 0
            ACC = A.sat20(ACC + (((x << 3)*Cs) >> 6))
            if xfer(ctl): RES = A.sat16(ACC >> 3)
            if b3f(ctl): DM[addr] = RES
            if xfer(ctl): esum += abs(RES)
        out.append(esum)
    peak = max(out) or 1
    early = sum(out[:200])/200
    late = sum(out[2000:2200])/200
    blown = any(o >= 32767 for o in out[-50:])
    return dict(peak=peak, early=round(early), late=round(late),
                late_ratio=round(late/(early or 1), 4), blown=blown)


# ---- base decode (the committed/current one) ----
BASE = dict(
    pick=lambda c: (bit(c, 5) << 1) | bit(c, 4),
    wa=lambda c: c & 3,
    zero=lambda c: bit(c, 7),
    b3=lambda c: bit(c, 3),
    xfer=lambda c: bit(c, 2),
)


def mk_pick(hi, lo):
    return lambda c: (bit(c, hi) << 1) | bit(c, lo)


def main():
    prog = load_ctl_prog(0x01)
    print(f"CONCERT active steps: {len(prog)}")

    variants = []

    # ---------- (0) baseline ----------
    variants.append(("BASE pick=(b5,b4) wa=(b1,b0) Z=b7 b3=b3 X=b2", BASE))

    # ---------- (1) RA/pick = every ordered pair from {b5,b4,b3} and {b1,b0} ----------
    # keep wa/zero/b3/xfer at base, only change pick.
    pick_bits = [5, 4, 3, 1, 0]
    for hi in pick_bits:
        for lo in pick_bits:
            if hi == lo: continue
            if (hi, lo) == (5, 4):  # that's base, skip dup
                continue
            d = dict(BASE); d['pick'] = mk_pick(hi, lo)
            variants.append((f"pick=(b{hi},b{lo})  [Z=b7 b3=b3 X=b2 wa=b1b0]", d))

    # ---------- (2) swap which bit is XFER vs b3 vs ZERO ----------
    # The three "single-bit" control roles {ZERO, b3, XFER} permuted over bits {7,3,2}
    import itertools
    roles_bits = [7, 3, 2]
    for perm in itertools.permutations(roles_bits):
        zb, b3b, xb = perm
        if (zb, b3b, xb) == (7, 3, 2):  # base
            continue
        d = dict(BASE)
        d['zero'] = (lambda bb: (lambda c: bit(c, bb)))(zb)
        d['b3'] = (lambda bb: (lambda c: bit(c, bb)))(b3b)
        d['xfer'] = (lambda bb: (lambda c: bit(c, bb)))(xb)
        variants.append((f"Z=b{zb} b3=b{b3b} X=b{xb}  [pick=b5b4 wa=b1b0]", d))

    # ---------- (2b) also swap ZERO/b3/XFER over bits {7,6,3,2} (include PROTECT bit6) ----------
    for perm in itertools.permutations([7, 6, 3, 2], 3):
        zb, b3b, xb = perm
        if (zb, b3b, xb) in [(7, 3, 2)]:
            continue
        # only add ones that USE bit6 (others covered above) to keep table compact
        if 6 not in perm:
            continue
        d = dict(BASE)
        d['zero'] = (lambda bb: (lambda c: bit(c, bb)))(zb)
        d['b3'] = (lambda bb: (lambda c: bit(c, bb)))(b3b)
        d['xfer'] = (lambda bb: (lambda c: bit(c, bb)))(xb)
        variants.append((f"Z=b{zb} b3=b{b3b} X=b{xb} (uses b6) [pick=b5b4 wa=b1b0]", d))

    # ---------- (3) WA = other bit pairs ----------
    wa_pairs = [(3, 2), (1, 0), (5, 4), (7, 6), (2, 1), (4, 3), (6, 5)]
    for hi, lo in wa_pairs:
        if (hi, lo) == (1, 0):  # base
            continue
        d = dict(BASE); d['wa'] = mk_pick(hi, lo)
        variants.append((f"wa=(b{hi},b{lo})  [pick=b5b4 Z=b7 b3=b3 X=b2]", d))

    # ---------- (4) a few JOINT plausible re-decodes ----------
    # The control byte read MSB->LSB could group differently. Try a couple of fully
    # coherent alternative field orders that keep all 6 roles present & disjoint.
    joint = [
        # pick low, wa high (mirror)
        ("pick=(b1,b0) wa=(b5,b4) Z=b7 b3=b3 X=b2",
         dict(pick=mk_pick(1, 0), wa=mk_pick(5, 4),
              zero=lambda c: bit(c, 7), b3=lambda c: bit(c, 3), xfer=lambda c: bit(c, 2))),
        # b3 and XFER swapped, pick=(b5,b4)
        ("pick=(b5,b4) wa=(b1,b0) Z=b7 b3=b2 X=b3",
         dict(pick=mk_pick(5, 4), wa=mk_pick(1, 0),
              zero=lambda c: bit(c, 7), b3=lambda c: bit(c, 2), xfer=lambda c: bit(c, 3))),
        # ZERO=b2, XFER=b7 (swap ends), pick=(b5,b4)
        ("pick=(b5,b4) wa=(b1,b0) Z=b2 b3=b3 X=b7",
         dict(pick=mk_pick(5, 4), wa=mk_pick(1, 0),
              zero=lambda c: bit(c, 2), b3=lambda c: bit(c, 3), xfer=lambda c: bit(c, 7))),
        # pick=(b4,b3), wa=(b1,b0) (RA shifted down one)
        ("pick=(b4,b3) wa=(b1,b0) Z=b7 b3sel=b5 X=b2",
         dict(pick=mk_pick(4, 3), wa=mk_pick(1, 0),
              zero=lambda c: bit(c, 7), b3=lambda c: bit(c, 5), xfer=lambda c: bit(c, 2))),
        # pick=(b3,b2), everything shifted (a fully different framing)
        ("pick=(b3,b2) wa=(b1,b0) Z=b7 b3sel=b5 X=b4",
         dict(pick=mk_pick(3, 2), wa=mk_pick(1, 0),
              zero=lambda c: bit(c, 7), b3=lambda c: bit(c, 5), xfer=lambda c: bit(c, 4))),
    ]
    for name, d in joint:
        variants.append((name + "  [JOINT]", d))

    # ---------- run all ----------
    print(f"\n{'variant':<58} {'lambda':>12} {'ppm':>9}  {'verdict':<6} "
          f"{'peak':>9} {'late/early':>10} blown")
    print("-"*120)
    results = []
    for name, dec in variants:
        try:
            lam = lam_decode(prog, dec)
        except Exception as e:
            print(f"{name:<58} ERROR: {e}")
            continue
        ppm = (lam-1)*1e6
        verdict = "GROW" if lam > 1 else "DECAY"
        s = impulse_sanity(prog, dec)
        results.append((name, lam, ppm, verdict, s))
        print(f"{name:<58} {lam:>12.7f} {ppm:>+9.1f}  {verdict:<6} "
              f"{s['peak']:>9} {s['late_ratio']:>10.4f} {s['blown']}")

    # ---------- flag decay-and-coherent candidates ----------
    print("\n=== FLAGGED: lambda<1 (DECAY) AND structurally coherent ===")
    any_flag = False
    for name, lam, ppm, verdict, s in results:
        if lam < 1.0:
            # coherence: nonzero late energy or a real peak; not totally dead, not blown
            coherent = (s['peak'] > 1) and (not s['blown'])
            dead = (s['peak'] <= 1)
            tag = "COHERENT" if (coherent and 0 < s['late_ratio'] < 5) else \
                  ("DEAD" if dead else "DECAY-but-check")
            print(f"  {name}: lambda={lam:.7f} ({ppm:+.1f} ppm)  peak={s['peak']} "
                  f"late/early={s['late_ratio']}  -> {tag}")
            any_flag = True
    if not any_flag:
        print("  (none: every variant grows or is degenerate)")


if __name__ == '__main__':
    main()
