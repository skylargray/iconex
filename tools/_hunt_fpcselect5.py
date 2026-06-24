#!/usr/bin/env python3
"""ANGLE pt5: is there a PURE-ADDRESS device-select rule (no WA heuristic) that
reproduces the collapse? The hardware decodes device from the absolute address bus.

Test thresholds on the COMPUTED absolute address: route to FPC (no DM r/w) when
addr >= T for various T (i.e. top of the 64K map is the FPC/IO window). Sweep T and
report lambda + how many step-instances per sample get routed.

Also report the per-sample DMEM-write count the baseline model performs, to size the
"spurious accesses" claim.

Read-only.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK=A.DMASK; PICK=lambda st:(st['b5']<<1)|st['b4']; prog=A.load_microcode(0x01)

def lam(prog, T=None, nsamp=40000, K=128, seed=1e4):
    """If T is not None: any step whose computed addr >= T routes to FPC (no DM)."""
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0
    nz=set(); seeded=False; traj=[]; routed=0
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            is_fpc = (T is not None) and (addr>=T)
            if is_fpc:
                dab=0.0; routed+=1
            else:
                dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab+=seed; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3'] and not is_fpc:
                DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            ss=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(ss)/K))
            f=1.0/ss; R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    t=sorted(traj[-50:]); return t[len(t)//2], routed/nsamp

print("pure computed-address threshold sweep (route addr>=T to FPC):")
print("  the absolute addresses actually used live in two clusters; find the split\n")
for T in (0x8000, 0xC000, 0xE000, 0xF000, 0xF800, 0xFC00, 0xFE00, 0xFF00, 0xFF80, 0xFFC0, 0xFFF0):
    L,r = lam(prog, T)
    print(f"  T={T:#06x}  lambda={L:.7f} ppm={(L-1)*1e6:+9.1f}  routed/sample={r:5.1f}")
L0,_ = lam(prog, None)
print(f"\n  baseline (no routing) lambda={L0:.7f} ppm={(L0-1)*1e6:+.1f}")

# distribution of computed addresses to see the natural FPC window
import collections
hist=collections.Counter()
pos=0
for n in range(2000):
    pos=(pos+1)&DMASK
    for st in prog:
        addr=(pos-st['offset'])&DMASK
        hist[addr>>12]+=1   # by 4K page
tot=sum(hist.values())
print("\n  computed-address distribution by 4K page (page: %of accesses):")
for pg in sorted(hist):
    print(f"    {pg:#x}xxx : {100*hist[pg]/tot:5.2f}%")
