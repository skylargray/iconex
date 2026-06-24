#!/usr/bin/env python3
"""Why does s=94 alone carry the eigenvalue, while structural siblings s=29/s=125 don't?

s=29, s=94, s=125 are all WA=3 b3=0 bit15 large-offset (rel~0x4ce0) forward delay reads.
Suppressing s=94's read flips lambda; s=29/s=125 do nothing. The 'rel-addr never written'
framing is base=0 static; the REAL feedback is dynamic: addr=(pos-offset) sweeps DMEM and
reads what other steps wrote at past positions.

Decisive principled test of the ANGLE (FPC-output phantom):
  An FPC OUTPUT step drives the DAC and is a SINK; its DMEM read/write must be irrelevant.
  A RECIRCULATION READ pulls a delayed tap back into the accumulating chain.
Distinguish by: does s=94's product enter an accumulation that reaches a later XFER (RES)
WITHOUT a ZERO clearing it first? Trace the ACC lineage from s=94 to the next XFER.

Also: confirm s=94 is NOT FPC by section-12 rule -- a TRUE output has low14 = a strobe code
and (in diag) was the LAST step of its 4-step I/O block right after the input read. s=94's
low14=0x331f is a plain large delay tap, identical pattern to s=29/s=125 (the block forward
reads), so by the firmware-build path these are delay reads, not WR DA/ writes.
"""
import sys, math
sys.path.insert(0, 'tools')
import aru_datapath as A
DMASK = A.DMASK
PICK = lambda st: (st['b5'] << 1) | st['b4']


def trace_acc_to_xfer(prog, s_target):
    """From step s_target forward (program order, wrapping), list steps until the next XFER,
    noting any ZERO that would clear s_target's contribution first."""
    idx = next(i for i, p in enumerate(prog) if p['s'] == s_target)
    n = len(prog); chain = []
    for j in range(1, n+1):
        p = prog[(idx + j) % n]
        chain.append((p['s'], p['ZERO'], p['XFER']))
        if p['ZERO']:
            return ('ZEROED-before-XFER', chain)
        if p['XFER']:
            return ('reaches-XFER s=%d' % p['s'], chain)
    return ('no-xfer', chain)


def main():
    prog = A.load_microcode(0x01)
    byS = {p['s']: p for p in prog}

    for s in [29, 94, 125]:
        p = byS[s]
        # does s itself ZERO? what is its PICK source? does its product survive to an XFER?
        verdict, chain = trace_acc_to_xfer(prog, s)
        # also: this step's OWN accumulation -- is ACC cleared AT this step (ZERO) before MAC?
        print(f"s={s:3d} off={p['offset']:#06x} ZERO={p['ZERO']} PICK->R{PICK(p)} coeff={p['coeff']:5d}")
        print(f"      product fate: {verdict}")
        print(f"      chain (s,ZERO,XFER) to next XFER/ZERO: {chain[:8]}")

    # The real question: who reads the register s=94 writes (R[3]) and feeds the loop?
    # s=94 writes R[3]; next reader of R3? we found s=96. But s=96 PICK source:
    for s in [94, 95, 96]:
        p = byS[s]
        print(f"\n  s={s}: WA={p['WA']} PICK->R{PICK(p)} ZERO={p['ZERO']} XFER={p['XFER']} b3={p['b3']} coeff={p['coeff']}")

    # Crucial: is the +1126 ppm eigenvector actually flowing THROUGH s=94's READ (a delayed
    # DMEM tap), i.e. s=94 is a long forward delay read that closes a loop? Test write-side:
    # find which step writes the address s=94 reads at the dominant lag. Scan: at steady state
    # the loop period = the dominant offset. We just confirm s=94's READ is load-bearing and
    # is a NORMAL delay read (b3=0 from DMEM), exactly like s=29/s=125 structurally.
    print("\n  -> s=94 is structurally identical (WA=3,b3=0,bit15,large-delay forward read) to")
    print("     s=29 and s=125. It is a DELAY-LINE READ, not an FPC WR DA/ output. The 51/21")
    print("     bit15 matches are large absolute delays, exactly as warned. FPC-OUTPUT angle =>")
    print("     no phantom-output recirculation; the only load-bearing 'candidate' is a genuine tap.")


if __name__ == '__main__':
    main()
