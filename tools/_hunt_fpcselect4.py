#!/usr/bin/env python3
"""ANGLE pt4: scrutinize the V3 collapse. Is suppressing DMEM at (offset-b15 & WA==3)
a PRINCIPLED hardware fix or an accidental knife-edge overfit?

Concerns:
 (a) The brief says s69 is an ESSENTIAL damping closer whose DMEM write matters
     (zeroing its coeff makes lambda +16102 ppm hotter). out_fp INCLUDES s69. So
     V3 removes s69's DMEM write. Does the collapse depend on s69 specifically, or
     is it the whole out_fp set?
 (b) Is the +0.1 ppm a coincidence of THIS set, or robust? Leave-one-out: which
     single step's DMEM-write suppression carries most of the -1126 ppm?
 (c) Cross-check: the brief says removing only the b3 WRITE-BACK (not the read) is
     the physically meaningful change at an FPC output step (WR DA/ drives FPC, not
     DM). Test suppressing ONLY the b3 write at out_fp (keep reads) vs full route.

Read-only.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']
prog = A.load_microcode(0x01)


def lam(prog, suppress_rw=frozenset(), suppress_write_only=frozenset(),
        nsamp=60000, K=128, seed=1e4):
    R=[0.0]*4; ACC=0.0; RES=0.0; DM=[0.0]*(DMASK+1); pos=0
    nz=set(); seeded=False; traj=[]
    for n in range(nsamp):
        pos=(pos+1)&DMASK
        for st in prog:
            addr=(pos-st['offset'])&DMASK
            s=st['s']
            full=s in suppress_rw
            wonly=s in suppress_write_only
            if full:
                dab=0.0
            else:
                dab=RES if st['b3'] else DM[addr]
            if not seeded and st is prog[0]:
                dab+=seed; seeded=True
            mag=abs(st['coeff']); Cs=-(mag>>1) if st['coeff']<0 else (mag>>1)
            x=R[PICK(st)]; R[st['WA']]=dab
            if st['ZERO']: ACC=0.0
            ACC=ACC+x*8.0*Cs/64.0
            if st['XFER']: RES=ACC/8.0
            if st['b3'] and not full and not wonly:
                DM[addr]=RES; nz.add(addr)
        if (n+1)%K==0:
            ss=math.sqrt(ACC*ACC+RES*RES+sum(v*v for v in R)+sum(DM[i]*DM[i] for i in nz))+1e-300
            traj.append(math.exp(math.log(ss)/K))
            f=1.0/ss; R=[v*f for v in R]; ACC*=f; RES*=f
            for i in nz: DM[i]*=f
    t=sorted(traj[-60:]); return t[len(t)//2]


out_fp = {p['s'] for p in prog if (p['offset']&0x8000) and p['WA']==3}
out_fp_w = {s for s in out_fp if any(p['s']==s and p['b3'] for p in prog)}  # those with b3=1

V0 = lam(prog)
print(f"V0 baseline                              lambda={V0:.7f} ppm={(V0-1)*1e6:+.1f}")

# (c) write-only suppression at out_fp (physically: WR DA/ -> FPC, no DM write,
#     but a non-output read step still reads DM). For WA==3 steps there is no
#     separate read anyway (b3 picks RES not DM), so write-only == full route here.
Vw = lam(prog, suppress_write_only=out_fp_w)
print(f"V3w suppress ONLY b3-write at out_fp(b3) lambda={Vw:.7f} ppm={(Vw-1)*1e6:+.1f}  "
      f"(steps n={len(out_fp_w)})")
Vfull = lam(prog, suppress_rw=out_fp | {76})
print(f"V3  full route out_fp + s76              lambda={Vfull:.7f} ppm={(Vfull-1)*1e6:+.1f}")

# (b) leave-one-out: start from full out_fp_w write-suppression, ADD BACK one step's
# write, see how much ppm returns. The step whose re-added write returns the most ppm
# is the eigenvalue carrier.
print("\nleave-one-out (suppress all out_fp(b3) writes, then RE-ENABLE one step's write):")
rows=[]
for s in sorted(out_fp_w):
    Vs = lam(prog, suppress_write_only=(out_fp_w - {s}))
    rows.append((s, Vs))
rows.sort(key=lambda r: -r[1])
for s,Vs in rows[:12]:
    print(f"   re-enable s{s:<3} write -> lambda={Vs:.7f} ppm={(Vs-1)*1e6:+9.1f}")
print("   ...")
for s,Vs in rows[-4:]:
    print(f"   re-enable s{s:<3} write -> lambda={Vs:.7f} ppm={(Vs-1)*1e6:+9.1f}")

# (a) does removing JUST s69 write account for it?
V69 = lam(prog, suppress_write_only={69})
print(f"\nsuppress ONLY s69 b3-write   lambda={V69:.7f} ppm={(V69-1)*1e6:+.1f}")
# remove s69 from the suppression set -> is collapse gone?
Vno69 = lam(prog, suppress_write_only=(out_fp_w-{69}))
print(f"suppress out_fp(b3) EXCEPT s69 lambda={Vno69:.7f} ppm={(Vno69-1)*1e6:+.1f}")
