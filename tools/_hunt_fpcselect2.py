#!/usr/bin/env python3
"""ANGLE pt2: is OFFSET-bit15 a device select in the LIVE image? Reductio test.

If "offset & 0x8000 => route to FPC, skip DMEM" were applied to the live CONCERT
image, count how many active steps that captures, and whether step 69 (the proven
eigenvalue-dominant comb closer) is among them. If yes, the rule is self-refuting
for live images: it would gut the tank.

Then: contrast offset-bit15 vs COMPUTED-address bit15 (the thing that actually
reaches the RAM/device decode), at the confirmed position base = 0, and show which
interpretation isolates exactly the 1 input read + the genuine output writes vs
swallowing the whole tank.

Read-only.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

prog = A.load_microcode(0x01)
DMASK = A.DMASK
n_active = len(prog)
b15 = [p for p in prog if p['offset'] & 0x8000]
print(f"active steps                          : {n_active}")
print(f"steps with OFFSET bit15 set           : {len(b15)}  ({100*len(b15)//n_active}%)")
print(f"is step 69 (eigen-dominant closer) among them? "
      f"{any(p['s']==69 for p in b15)}")
print("=> Treating offset-bit15 as 'skip DMEM' would remove DMEM r/w from 85% of")
print("   the program INCLUDING the dominant comb closer s69 -> the tank cannot")
print("   exist. So OFFSET-bit15 is NOT a live-image device select.\n")

# Now compute address (position-offset) over a full sample sweep of positions and
# see whether COMPUTED-address bit15 ever distinguishes anything. position base is
# confirmed 0; position increments each sample. The hardware decodes the device from
# the 16-bit absolute address bus (DMEM RAS/CAS only on MEMAC; FPC on RD AD//WR DA/).
# Check: over many positions does the computed addr bit15 stay clean (i.e. is the
# tank entirely in the low 32K, with FPC steps the only top-bit users)?
import collections
hi_addr_steps = collections.Counter()
NPOS = 4000
for pos in range(NPOS):
    p2 = (pos+1) & DMASK
    for p in prog:
        addr = (p2 - p['offset']) & DMASK
        if addr & 0x8000:
            hi_addr_steps[p['s']] += 1
print(f"steps whose COMPUTED addr has bit15 set for ANY of {NPOS} positions:")
print(f"  {sorted(hi_addr_steps)}")
print(f"  (fraction of positions each is 'high', a few): "
      + ", ".join(f"s{s}:{hi_addr_steps[s]*100//NPOS}%" for s in sorted(hi_addr_steps)[:12]))
print()

# The genuine FPC fingerprints per tech-ref 12 (base-invariant): the INPUT read is
# WA!=3 & low14==0x3FFF & bit15; engine model special-cases ONLY that one (s76).
ins = A.fpc_input_step(prog)
print(f"engine model FPC-input step (special-cased, NOT read from DMEM) : s={ins}")
outs = [p['s'] for p in prog if (p['offset']&0x8000) and p['WA']==3]
print(f"steps matching OUTPUT-write fingerprint (bit15 & WA==3)         : {len(outs)} steps")
print(f"  -> {outs}")
print("NOTE: many of these 'WA==3' steps also have b3=1 and FIRE the DMEM write in")
print("the model. In hardware a WA=3 pass-through step that is a real D/A output")
print("write asserts WR DA/ (FPC), and DMEM CAS/ only falls on MEMAC. If those output")
print("steps are FPC writes, the model's b3 DMEM write-back at them is SPURIOUS.")
print()

# Quantify: how many DMEM WRITES does the model do per sample that land at a step
# the FPC-output fingerprint (bit15 & WA==3) would claim as a D/A write?
model_writes = [p for p in prog if p['b3']]
out_fp = set(outs)
overlap_w = [p['s'] for p in model_writes if p['s'] in out_fp]
print(f"model DMEM-write steps (b3=1) total                : {len(model_writes)}")
print(f"  of which also match output-write fingerprint     : {len(overlap_w)} -> {overlap_w}")
print(f"  pure-tank DMEM writes (b3=1, NOT bit15&WA==3)     : "
      f"{[p['s'] for p in model_writes if p['s'] not in out_fp]}")
