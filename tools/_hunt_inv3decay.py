#!/usr/bin/env python3
"""Pin inv_l3 by DECAY PHYSICS + microcode plausibility (no WR DA/ output decode needed).

For each clean program, under inv_l2=False/read_bit=1 and BOTH inv_l3:
  (1) microcode stats: #steps, #zero-coeff (pure-delay move) steps, #XFER, #ZERO, #RD-AD,
      #RDRREG, #DMEM-read, #DMEM-write -- a real reverb microprogram has many pure-delay
      move steps and a sane XFER/ZERO structure.
  (2) closed-loop decay: inject an impulse at the RD-AD (audio-in) step, run the float
      acc_latch datapath with NO renorm, track total tank-state energy per output sample,
      fit the late-time log-energy slope -> per-sample lambda -> RT60 @ 34130 Hz.

A correct decode gives a clean, gently-decaying tank (RT60 ~ seconds, single slope), not a
flat sustain (RT60 = inf), a fast collapse, or growth.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _hunt_rawcache as RC
import _hunt_rebuild2 as R2
MASK = 0xFFFF
FS = 34130.0


def stats(prog):
    z = sum(1 for st in prog if st['Cs'] == 0)
    xf = sum(1 for st in prog if st['XFER'])
    zr = sum(1 for st in prog if st['ZERO'])
    rdad = sum(1 for st in prog if st['MI17'] == 0 and st['MI16'] == 1 and st['sub'] == 3)
    rdr = sum(1 for st in prog if st['MI17'] == 0 and st['MI16'] == 1 and st['sub'] == 1)
    rd = sum(1 for st in prog if st['MI17'] == 1 and st['MI16'] == 1)
    wr = sum(1 for st in prog if st['MI17'] == 1 and st['MI16'] == 0)
    return dict(n=len(prog), zcoeff=z, xfer=xf, zero=zr, rdad=rdad, rdr=rdr, rd=rd, wr=wr)


def decay(prog, nsamp=120000, warmup=4000, read_bit=1, imp=1.0):
    """Float acc_latch closed loop. Impulse at the first RD-AD step. Returns
    (rt60_s, lam_per_sample, clean_r2, peakidx). Tank energy sampled per output sample."""
    R = [0.0]*4
    ACC = 0.0; RES = 0.0; ACCc = 0.0
    DM = [0.0]*(MASK+1); nz = set(); pos = 0
    adsteps = [i for i, st in enumerate(prog)
               if st['MI17'] == 0 and st['MI16'] == 1 and st['sub'] == 3]
    inj = adsteps[0] if adsteps else None
    E = []
    for n in range(nsamp):
        pos = (pos+1) & MASK
        for i, st in enumerate(prog):
            addr = (pos - st['offset']) & MASK
            is_dram = st['MI17'] == 1
            is_read = is_dram and (st['MI16'] == read_bit)
            is_write = is_dram and not is_read
            is_sub = (st['MI17'] == 0) and (st['MI16'] == 1)
            if is_read:
                dab = DM[addr]
            elif is_sub and st['sub'] == 1:
                dab = RES
            elif is_sub and st['sub'] == 3:
                dab = (imp if (n == 0 and i == inj) else 0.0)
            elif is_write:
                dab = RES
            else:
                dab = 0.0
            x = R[st['RA']]; R[st['WA']] = dab
            if st['ZERO']:
                ACC = 0.0
            ACC += x * 8.0 * st['Cs'] / 64.0
            if st['XFER']:
                RES = ACCc / 8.0
            if is_write:
                DM[addr] = RES; nz.add(addr)
            ACCc = ACC
        e = ACC*ACC + RES*RES + ACCc*ACCc + sum(v*v for v in R) + sum(DM[i]*DM[i] for i in nz)
        E.append(e)
    # late-time slope fit on 0.5*log(E)
    ys = []
    xs = []
    for n in range(warmup, nsamp):
        if E[n] > 0:
            xs.append(n); ys.append(0.5*math.log(E[n]))
    if len(xs) < 100:
        return (float('nan'), float('nan'), 0.0, 0)
    m = len(xs)
    mx = sum(xs)/m; my = sum(ys)/m
    sxx = sum((x-mx)**2 for x in xs); sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    slope = sxy/sxx if sxx else 0.0           # d(ln amp)/d sample = ln(lambda)
    # r^2
    sse = sum((y - (my + slope*(x-mx)))**2 for x, y in zip(xs, ys))
    syy = sum((y-my)**2 for y in ys)
    r2 = 1 - sse/syy if syy else 0.0
    lam = math.exp(slope)
    # RT60: amplitude drops 60 dB -> factor 1000. n60 = ln(1000)/(-slope). seconds = n60/FS
    rt60 = (math.log(1000.0)/(-slope))/FS if slope < 0 else float('inf')
    peak = max(range(nsamp), key=lambda i: E[i])
    return (rt60, lam, r2, peak)


def main():
    cache = RC.load()
    clean = [p for p in sorted(cache) if cache[p]['clean']]
    NS = int(os.environ.get('NS', '120000'))
    only = os.environ.get('ONLY')
    if only:
        clean = [int(only, 16)]
    print(f"inv_l3 pin via decay physics + microcode stats (inv_l2=False, read_bit=1)\n")
    for inv_l3 in (True, False):
        print(f"========== inv_l3 = {inv_l3} ==========")
        print(f"{'pid':>4} {'n':>3} {'zc':>3} {'xf':>3} {'zr':>3} {'adIn':>4} {'rdr':>3} "
              f"{'rd':>3} {'wr':>3} | {'RT60(s)':>9} {'lam-1(ppm)':>11} {'r2':>6} {'peak':>7}")
        for p in clean:
            prog = R2.decode(cache[p]['steps'], inv_l2=False, inv_l3=inv_l3)
            s = stats(prog)
            rt60, lam, r2, peak = decay(prog, nsamp=NS)
            ppm = (lam-1)*1e6 if not math.isnan(lam) else float('nan')
            rts = f"{rt60:9.2f}" if rt60 != float('inf') else "      inf"
            print(f"{('%#x' % p):>4} {s['n']:>3} {s['zcoeff']:>3} {s['xfer']:>3} {s['zero']:>3} "
                  f"{s['rdad']:>4} {s['rdr']:>3} {s['rd']:>3} {s['wr']:>3} | "
                  f"{rts} {ppm:>11.2f} {r2:>6.3f} {peak:>7}")
        print()


if __name__ == '__main__':
    main()
