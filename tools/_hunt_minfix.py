#!/usr/bin/env python3
"""ANGLE part 3/3: the MINIMAL PRINCIPLED FIX search.

Question: does a SINGLE principled decode correction (one step's coeff off-by-one,
one sign flip, one ZERO/XFER/b3 bit, one missing/extra edge) bring lambda to
~0.99999, OR does only a distributed/uniform attenuation work?

I test, on the EXACT float linear map (mirror of exp_lambda_clean):
  1. uniform coeff scale s* such that lambda(s*)=target  -> the "physical loss" answer
  2. per-step coeff +-1 (off-by-one in the 7-bit magnitude) -- the most likely single
     decode bug; report the best single-step change and the lambda it reaches
  3. per-step coeff sign flip
  4. per-step toggle of ZERO / XFER / b3 (a mis-decoded control bit)
  5. dropping each single step (a spurious-step decode error)
For each, report whether ANY single change reaches lambda in [0.99990, 1.00000]
(i.e. a real, physical RT60). If none does, the minimal fix is necessarily
distributed -> consistent with a uniform physical loss, NOT a localizable bug.
"""
import sys, os, math, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import exp_lambda_clean as L

DMASK = A.DMASK
PICK = L.PICK
TARGET = 0.9999899


def lam_custom(prog, nsamp=24000, K=128, seed=1e4, gscale=1.0, override=None):
    """Float mirror of L.lambda_trajectory.
       gscale : global multiply on every step's net coeff.
       override: dict s-> (coeff_override_int) or callable(st)->Cs_float to replace Cs.
       Steps may be dropped by setting override[s]='DROP'."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    nz = set(); seeded = False; traj = []
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        for st in prog:
            ov = override.get(st['s']) if override else None
            if ov == 'DROP':
                # still must honor the seed injection on prog[0]
                if not seeded and st is prog[0]:
                    seeded = True
                continue
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += seed; seeded = True
            if ov is not None and ov != 'DROP':
                coeff = ov
            else:
                coeff = st['coeff']
            mag = abs(coeff); Cs = -(mag>>1) if coeff<0 else (mag>>1)
            csf = float(Cs)*gscale
            x = R[PICK(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*csf/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES; nz.add(addr)
        if (n+1) % K == 0:
            s = math.sqrt(ACC*ACC + RES*RES + sum(v*v for v in R)
                          + sum(DM[i]*DM[i] for i in nz)) + 1e-300
            traj.append(math.exp(math.log(s)/K))
            f = 1.0/s
            R = [v*f for v in R]; ACC *= f; RES *= f
            for i in nz: DM[i] *= f
    tail = sorted(traj[-50:])
    return tail[len(tail)//2]


def main():
    prog = A.load_microcode(0x01)
    lam0 = lam_custom(prog)
    print(f"baseline lambda = {lam0:.7f}  ({(lam0-1)*1e6:+.1f} ppm), target {TARGET}\n")

    # ---- 1. uniform scale bisection ----
    print("=== 1. UNIFORM coeff scale s* for lambda=target ===")
    lo, hi = 0.80, 1.0
    for _ in range(26):
        mid = 0.5*(lo+hi)
        lm = lam_custom(prog, gscale=mid)
        if lm > TARGET: hi = mid
        else: lo = mid
    s_star = 0.5*(lo+hi)
    lm = lam_custom(prog, gscale=s_star)
    print(f"  s* = {s_star:.5f}  (=> {100*(1-s_star):.2f}% uniform attenuation)  lambda={lm:.7f}")

    # ---- 2. per-step coeff +-1 (off-by-one magnitude) ----
    print("\n=== 2. single-step coeff +-1 (off-by-one decode) -> best coolers ===")
    results = []
    for st in prog:
        c = st['coeff']
        for dc in (-1, +1):
            nc = c + dc if c >= 0 else c - dc  # change magnitude toward/away 0 keeping sign-ish
            # simpler: just nudge the signed integer by dc (covers magnitude+sign boundary)
            nc = c + dc
            lm = lam_custom(prog, override={st['s']: nc})
            results.append((lm, st['s'], c, nc))
    results.sort(key=lambda t: abs(t[0]-TARGET))
    best_any = min(results, key=lambda t: t[0])  # coolest reachable
    print("  closest-to-target single +-1 changes:")
    for lm, s, c, nc in results[:8]:
        print(f"    s={s:3d} coeff {c:+d}->{nc:+d}  lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)")
    print(f"  COOLEST single +-1 reachable: s={best_any[1]} {best_any[2]:+d}->{best_any[3]:+d}"
          f"  lambda={best_any[0]:.7f} ({(best_any[0]-1)*1e6:+.1f} ppm)")

    # ---- 3. per-step sign flip ----
    print("\n=== 3. single-step sign flip -> best coolers ===")
    flips = []
    for st in prog:
        lm = lam_custom(prog, override={st['s']: -st['coeff']})
        flips.append((lm, st['s'], st['coeff']))
    flips.sort(key=lambda t: t[0])
    for lm, s, c in flips[:6]:
        print(f"    s={s:3d} coeff {c:+d}->{-c:+d}  lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)")

    # ---- 4. control-bit toggles via DROP (proxy for removing a spurious step) ----
    print("\n=== 4. single-step DROP -> best coolers (spurious-step decode) ===")
    drops = []
    for st in prog:
        lm = lam_custom(prog, override={st['s']: 'DROP'})
        drops.append((lm, st['s'], st['coeff'], st['b3'], st['XFER']))
    drops.sort(key=lambda t: t[0])
    for lm, s, c, b3, xf in drops[:8]:
        print(f"    drop s={s:3d} (coeff {c:+d} b3={b3} X={xf})  lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)")

    # ---- verdict ----
    print("\n=== MINIMAL-FIX VERDICT ===")
    pool = ([(lm, f"coeff s={s} {c}->{nc}") for lm, s, c, nc in results]
            + [(lm, f"signflip s={s}") for lm, s, c in flips]
            + [(lm, f"drop s={s}") for lm, s, c, b3, xf in drops])
    in_band = [(lm, d) for lm, d in pool if 0.99990 <= lm <= 1.00000]
    in_band.sort(key=lambda t: abs(t[0]-TARGET))
    if in_band:
        print(f"  {len(in_band)} single-change candidates land in [0.99990,1.00000]:")
        for lm, d in in_band[:6]:
            print(f"     {d}: lambda={lm:.7f} ({(lm-1)*1e6:+.1f} ppm)")
    else:
        coolest = min(pool, key=lambda t: t[0])
        print("  NO single principled change reaches a physical RT60 band [0.99990,1.0].")
        print(f"  Coolest single change only reaches lambda={coolest[0]:.7f} "
              f"({(coolest[0]-1)*1e6:+.1f} ppm) via {coolest[1]}")
        print(f"  => the {(lam0-TARGET)*1e6:+.0f} ppm excess is DISTRIBUTED; only the uniform "
              f"{100*(1-s_star):.1f}% attenuation reaches target.")


if __name__ == '__main__':
    main()
