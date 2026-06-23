#!/usr/bin/env python3
"""Instrument the ACTUAL recirculation delays. Track every DMEM write (addr->sample)
and, on each DMEM read, report the real delay = current_sample - last_write_sample,
and which step wrote it. Reveals the true loop structure (resolving the circular-buffer
addressing), the short-delay crossover filters, and the ~9-sample unstable-mode loop.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK = A.DMASK


def main():
    prog = A.load_microcode(0x01); pick = lambda st: (st['b5'] << 1) | st['b4']
    R=[0,0,0,0]; ACC=0; RES=0; DM=[0]*(DMASK+1); pos=0
    last_write = {}            # addr -> (sample, step)
    read_delays = {}           # read_step -> {writer_step: [delays]}
    N=3000
    for n in range(N):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            if st['b3']:
                dab=RES
            else:
                dab=DM[addr]
                # record the recirculation delay for this read
                if addr in last_write and n>200:   # skip warmup
                    ws,wstep=last_write[addr]
                    d=n-ws
                    read_delays.setdefault(st['s'],{}).setdefault(wstep,[]).append(d)
            if n==0 and st is prog[0]: dab+=20000
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[pick(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0
            ACC=A.sat20(ACC+(((x<<3)*Cs)>>6))
            if st['XFER']: RES=A.sat16(ACC>>3)
            if st['b3']:
                DM[addr]=RES
                last_write[addr]=(n,st['s'])

    bystep={p['s']:p for p in prog}
    # Report the dominant (most frequent) writer and delay for each read step.
    print("Recirculation delays (read step <- writer step : delay samples):")
    print("Focus: SHORT loops (delay <= 20) = HF/crossover filters & the unstable mode\n")
    shorts=[]
    for rs in sorted(read_delays):
        for wstep, ds in read_delays[rs].items():
            md=min(ds)   # the stable (mode) delay
            if md<=20:
                shorts.append((md, wstep, rs))
    shorts.sort()
    for d,ws,rs in shorts:
        rp=bystep[rs]; wp=bystep[ws]
        rmag=abs(rp['coeff']); rCs=-(rmag>>1) if rp['coeff']<0 else (rmag>>1)
        print(f"  delay={d:>3}  write s{ws}(off {wp['offset']}) -> read s{rs}(off {rp['offset']}, "
              f"Cs={rCs}, {'LOW' if rs in (43,95) else 'XOV' if rs in (45,46,97,98) else ''})")
    # Also: the crossover/LOW read steps' delays explicitly
    print("\nLOW/XOV read steps and their measured delays:")
    for rs in (43,95,45,46,97,98):
        if rs in read_delays:
            allds=sorted({min(v) for v in read_delays[rs].values()})
            print(f"  s{rs}: min-delays seen = {allds[:8]}")
        else:
            print(f"  s{rs}: (no DMEM read recorded -- likely b3=1 write-only)")


if __name__ == '__main__':
    main()
