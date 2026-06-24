#!/usr/bin/env python3
"""ANGLE: FPC-vs-DMEM device select. Ground-truth audit.

Question: when a CONCERT step has offset bit15 set (FPC select per tech-ref 12 /
SM 3.8), does the lambda model ALSO perform the DMEM read/write the hardware does
NOT? Enumerate the bit15-set steps, classify them (FPC input read / output write /
neither), and report whether each writes DMEM in the float lambda model.

Read-only. Does not modify any committed file.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

prog = A.load_microcode(0x01)
print(f"CONCERT active steps: {len(prog)}\n")

DMASK = A.DMASK

# Per tech-ref 12 fingerprints:
#   FPC select  = offset & 0x8000
#   channel     = offset & 0x4000
#   input read  = bit15 set, WA!=3, low14 == 0x3FFF  (RD AD/)
#   output write= bit15 set, WA==3                    (WR DA/)
b15 = [p for p in prog if p['offset'] & 0x8000]
print(f"steps with offset bit15 set (would route to FPC, NOT DMEM): {len(b15)}")
print(f"{'s':>4} {'offset':>7} {'b15':>3} {'b14':>3} {'low14':>6} {'WA':>2} {'b3':>2} "
      f"{'XFER':>4} {'ZERO':>4} {'coeff':>5}  class / model-DMEM-action")
print('-'*100)
for p in b15:
    off = p['offset']
    low14 = off & 0x3FFF
    is_in  = (p['WA'] != 3) and (low14 == 0x3FFF)
    is_out = (p['WA'] == 3)
    if is_in:   cls = "FPC INPUT read (RD AD/)"
    elif is_out:cls = "FPC OUTPUT write (WR DA/)"
    else:       cls = "bit15 set but neither in/out pattern"
    # what the lambda model (exp_lambda_clean) does at this step:
    #   dab = RES if b3 else DM[addr];  if b3: DM[addr]=RES
    # i.e. it ALWAYS treats it as DMEM. It NEVER branches on bit15.
    model = ("WRITES DMEM[addr]=RES (b3=1)" if p['b3']
             else "reads DM[addr] (b3=0); no DMEM write")
    print(f"{p['s']:>4} {off:>#7x} {(off>>15)&1:>3} {(off>>14)&1:>3} {low14:>#6x} "
          f"{p['WA']:>2} {p['b3']:>2} {p['XFER']:>4} {p['ZERO']:>4} {p['coeff']:>5}  "
          f"{cls} | {model}")

print()
# Does ANY bit15-set step write DMEM in the lambda model? (these are the spurious accesses)
spurious = [p for p in b15 if p['b3']]
print(f"bit15-set steps that WRITE DMEM in the model (spurious vs hardware): "
      f"{len(spurious)}  -> steps {[p['s'] for p in spurious]}")
reads = [p for p in b15 if not p['b3']]
print(f"bit15-set steps that READ DMEM in the model (spurious vs hardware): "
      f"{len(reads)}  -> steps {[p['s'] for p in reads]}")

# Also: the FPC input read step per the engine model (aru_datapath.fpc_input_step)
ins = A.fpc_input_step(prog)
print(f"\naru_datapath.fpc_input_step() identifies input-read step s = {ins} "
      f"(this is the ONLY FPC step the engine model special-cases; output writes are NOT)")

# Sanity: confirm none of the bit15 steps are the eigenvalue-dominant closers the
# brief flagged (step 69 etc.). Show their lambda-support relevance: print their addr
# at pos=0 so we can see they map into the bit15-address region of DM.
print("\nbit15-set step addresses (pos arbitrary): these are the DM[] cells the model")
print("touches that the HARDWARE would route to the FPC instead:")
for pos in (0,):
    for p in b15:
        addr = (pos - p['offset']) & DMASK
        print(f"  s={p['s']:>3}  offset={p['offset']:#06x} -> DM addr {addr:#06x} "
              f"(bit15 of addr = {(addr>>15)&1})  b3={p['b3']}")
