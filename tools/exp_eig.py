#!/usr/bin/env python3
"""Clean structural eigenvalue via power iteration + dominant-frequency probe.

run_float (no sat, no quant) is a linear map; iterating it converges to the
dominant eigenvalue. We renormalize periodically to avoid overflow and read the
asymptotic per-sample growth = the true structural lambda. We also capture an
output proxy stream and find its dominant oscillation frequency.
"""
import sys, os, math, cmath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
NATIVE_HZ = 34130.0


def power_iter(prog, pick, nsamp=20000, renorm_every=200):
    """Linear (exact float) datapath with periodic renormalization.
    Returns (lambda, proxy_stream). proxy = last-RES per sample (an AC signal)."""
    R = [0.0]*4; ACC = 0.0; RES = 0.0
    DM = [0.0]*(DMASK+1); pos = 0
    # seed with a small impulse
    log_growth = 0.0; nrm = 1.0
    proxy = []
    seeded = False
    for n in range(nsamp):
        pos = (pos+1) & DMASK
        last_res = RES
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            dab = RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab += 20000.0; seeded = True
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0.0
            ACC = ACC + x*8.0*Cs/64.0
            if st['XFER']: RES = ACC/8.0
            if st['b3']: DM[addr] = RES
            if st['XFER']: last_res = RES
        proxy.append(last_res)
        if (n+1) % renorm_every == 0:
            # measure energy norm of full state and renormalize
            s = abs(ACC)+abs(RES)+sum(abs(v) for v in R)
            # include a sample of DM via current proxy magnitude
            s += sum(abs(p) for p in proxy[-renorm_every:]) + 1e-30
            if s > 0:
                f = 1e6 / s
                R = [v*f for v in R]; ACC*=f; RES*=f
                for i in range(len(DM)):
                    if DM[i] != 0.0: DM[i]*=f
                log_growth += -math.log(f)
    lam = math.exp(log_growth / nsamp)
    return lam, proxy


def dominant_freq(proxy, skip=2000):
    """Crude dominant-frequency estimate via autocorrelation peak (lag>1)."""
    x = proxy[skip:]
    n = len(x)
    if n < 100: return None
    mean = sum(x)/n
    x = [v-mean for v in x]
    # find first strong autocorrelation peak in lag 2..40
    best_lag, best = None, -1e30
    e0 = sum(v*v for v in x) or 1.0
    for lag in range(2, 60):
        s = sum(x[i]*x[i+lag] for i in range(n-lag)) / e0
        if s > best:
            best, best_lag = s, lag
    if best_lag:
        return NATIVE_HZ/best_lag, best_lag, best
    return None


def main():
    prog = A.load_microcode(0x01)
    pick = lambda st: (st['b5']<<1)|st['b4']
    lam, proxy = power_iter(prog, pick, nsamp=20000)
    print(f"structural lambda (power iteration) = {lam:.7f}")
    print(f"  => per-sample growth {(lam-1)*1e6:+.1f} ppm; "
          f"{'GROWS' if lam>1 else 'DECAYS'}")
    df = dominant_freq(proxy)
    if df:
        f, lag, corr = df
        print(f"dominant mode ~ {f:.0f} Hz  (lag {lag} samples, autocorr {corr:.3f})")
    # target
    print(f"target lambda = 0.9999899 ; loop-gain reduction needed "
          f"~ {(lam-0.9999899)/lam*100:.3f}%")


if __name__ == '__main__':
    main()
