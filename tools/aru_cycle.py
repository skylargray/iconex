#!/usr/bin/env python3
"""Cycle-accurate (AS0/AS1/AS2) 224XL ARU datapath model -- Phase A of the
signature-analysis endgame (docs/plans/224XL-signature-analysis-plan.md).

Decode + /32 multiply scale are reused verbatim from aru_datapath (frontier,
schematic-confirmed). What this module adds is the manual-exact PIPELINE TIMING
derived from Figs 3.2/3.3/3.4 + the 060-01318 netlist:

  * A microinstruction cycle = MS0..MS8 = AS0(MS0-2) AS1(MS3-5) AS2(MS6-8);
    ARU CK pulses once per AS state (3 ARUCK / cycle).
  * Fig 3.4: a microinstruction's operand (R[RA]) is read in its own cycle but
    the multiply runs in the NEXT cycle; the MAC result completes at AS0 of the
    cycle after that. XFER CK + ZERO/ for microinstruction m fire at AS0 of cycle
    m+1, i.e. one cycle LATE -- microinstruction m's XFER captures the accumulator
    BEFORE m's own product, and ZERO clears it so m's product starts fresh.
  * Fig 3.3: a DMEM write latches DIN = the result register, and "the critical
    timing path for DIN is XFER CK -> result register". So a DMEM write in cycle c
    uses the RES that was loaded by XFER CK at AS0 of cycle c -- i.e. the result
    XFER'd by the PREVIOUS microinstruction. The same held RES feeds RDRREG/.

The previous (aru_datapath.run_trace) model loaded RES *within* the XFER step and
let that same step's DMEM write see the fresh value -- one cycle too early, and
asymmetric between RDRREG (pre-XFER) and DMEM-write (post-XFER). That misalignment
is the dead-tank suspect: the firmware places XFER and the comb write-back on
adjacent steps assuming the hardware's 1-cycle RES latency.

`timing` selects the RES/XFER phase so the hypothesis is testable against oracles:
  'faithful'  : RES loaded at next cycle's AS0 (this module's thesis).
  'legacy'    : RES loaded within the XFER step (== aru_datapath.run_trace).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A

DMASK = A.DMASK
sat16, sat20 = A.sat16, A.sat20
SENT = -(1 << 63)


def _mul(x, cs):
    """One MAC product, frontier /32 scale: (x<<3)*cs >> 5  (net gain cs/32)."""
    return (x << 3) * cs >> 5


def output_steps(prog):
    """FPC D/A output steps: WA=3 pass-through, offset bit15 set, low14 != 0x3FFF
    (the input fingerprint). Mirrors the diagnostic capture that reads the unity
    echo. Returns the list of step numbers in program order."""
    return [st['s'] for st in prog
            if st['WA'] == 3 and (st['offset'] & 0x8000) and (st['offset'] & 0x3FFF) != 0x3FFF]


def input_step(prog):
    """RD-AD audio-in step (sub==3 read, base-invariant low14==0x3FFF fingerprint)."""
    for st in prog:
        if st['sub'] == 3 and st['MI17'] == 0 and st['MI16'] == 1 and (st['offset'] & 0x3FFF) == 0x3FFF:
            return st['s']
    # fall back to the device-decode RD-AD step if no fingerprint match
    for st in prog:
        if st['sub'] == 3 and st['MI17'] == 0 and st['MI16'] == 1:
            return st['s']
    return None


def run3(prog, nsamp=4000, imp=20000, in_seq=None, timing='faithful',
         capture_out=True, node_probe=None, dm_init=None):
    """Run the cycle-accurate ARU over `prog`, one microinstruction per cycle,
    nsamp samples (the 100-step frame is whatever `prog` is; NOP steps are absent).

    Injection: an impulse `imp` at sample 0 on the RD-AD input step, OR an explicit
    per-sample input list `in_seq` (len nsamp) delivered to the input step.

    Returns dict with:
      out[s][n]   : value driven to FPC output step s at sample n (capture_out)
      esum[n]     : sum |RES| over XFER steps at sample n (reverb-energy proxy)
      probe       : if node_probe set, the list it accumulates (see below)
    node_probe(rec): optional callback called once per microinstruction with a dict
      {n,s,arstate-less snapshot} of RES/ACC after this cycle's AS0 update -- used by
      the signature oracle (RES is constant across the 3 ARUCK of a cycle).
    """
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    pend = 0                    # product of the previous microinstruction (1-cycle MAC latency)
    xfer_p = 0; zero_p = 0      # previous microinstruction's deferred XFER/ZERO bits
    DM = [0] * (DMASK + 1) if dm_init is None else list(dm_init)
    pos = 0
    in_s = input_step(prog)
    out_s = set(output_steps(prog)) if capture_out else set()
    out = {s: [] for s in out_s}
    esum_list = []

    legacy = (timing == 'legacy')

    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        if in_seq is not None:
            ain = in_seq[n]
        else:
            ain = imp if n == 0 else 0
        esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            audio_in = ain if st['s'] == in_s else 0

            if not legacy:
                # --- AS0 of this cycle: prior microinstruction's XFER/ZERO fire
                #     (capture ACC BEFORE adding the prior product), then the prior
                #     product completes into the accumulator. ---
                if xfer_p:
                    RES = sat16(ACC >> 3)
                if zero_p:
                    ACC = 0
                ACC = sat20(ACC + pend)
                # cycle body: RES holds the prior microinstruction's XFER result
                dab, is_w = A._dab_source(st, DM, addr, RES, audio_in, A.READ_BIT)
                x = R[st['RA']]
                R[st['WA']] = dab
                if is_w:
                    DM[addr] = RES
                pend = _mul(x, st['cs'])
                xfer_p, zero_p = st['XFER'], st['ZERO']
                res_now = RES
            else:
                # legacy phase (== aru_datapath.run_trace): RES updated within step.
                dab, is_w = A._dab_source(st, DM, addr, RES, audio_in, A.READ_BIT)
                x = R[st['RA']]
                R[st['WA']] = dab
                ACC = sat20(ACC + pend)
                if st['XFER']:
                    RES = sat16(ACC >> 3)
                if st['ZERO']:
                    ACC = 0
                pend = _mul(x, st['cs'])
                if is_w:
                    DM[addr] = RES
                res_now = RES

            if st['XFER']:
                esum += abs(res_now)
            if st['s'] in out_s:
                out[st['s']].append(res_now)
            if node_probe is not None:
                node_probe(dict(n=n, s=st['s'], RES=res_now, ACC=ACC, addr=addr))
        esum_list.append(esum)

    return dict(out=out, esum=esum_list, in_step=in_s, out_steps=sorted(out_s), DM=DM)


# --------------------------------------------------------------------------
# ADD'L MULT (diagnostic 4, EA0-EB3) arithmetic oracle: an isolated multiply
# x * (coeff/32) must give RES = x*coeff/32 with the manual's coefficients.
# --------------------------------------------------------------------------
ADDL_MULT = [("x1", 32, 1.0), ("x1/2", 16, 0.5), ("x-1", -32, -1.0),
             ("x1/4", 8, 0.25), ("x5/4", 40, 1.25)]


def check_addl_mult(x=1000):
    """Single MAC: ZERO, multiply x by cs, XFER -> RES should be round(x*cs/32)."""
    print(f"ADD'L MULT arithmetic check (x={x}):")
    ok = True
    for name, cs, ratio in ADDL_MULT:
        # one isolated op: clear acc, one product, transfer.
        acc = 0
        acc = sat20(acc + _mul(x, cs))
        res = sat16(acc >> 3)
        want = int(x * cs / 32)        # truncating like the integer datapath
        got = res
        good = (got == want)
        ok &= good
        print(f"  {name:5s} cs={cs:+3d}  RES={got:+6d}  expect~{x*ratio:+8.1f} "
              f"(int {want:+6d})  {'OK' if good else 'MISMATCH'}")
    return ok


if __name__ == '__main__':
    print("=" * 70)
    ok = check_addl_mult(1000)
    print("ADD'L MULT:", "PASS" if ok else "FAIL")
    print("=" * 70)
    prog = A.load_microcode(0x01)
    print(f"CONCERT: {len(prog)} steps; in_step={input_step(prog)} "
          f"out_steps={output_steps(prog)}")
    for tm in ('legacy', 'faithful'):
        r = run3(prog, nsamp=4000, imp=20000, timing=tm)
        es = r['esum']
        peak = max(es) or 1
        early = sum(es[:200]) / 200
        late = sum(es[2000:2200]) / 200
        nz_out = {s: sum(1 for v in seq if abs(v) > 1) for s, seq in r['out'].items()}
        print(f"  timing={tm:8s} peak={peak:7d} early={early:8.1f} late={late:8.1f} "
              f"late/early={late/(early or 1):.4f}  out_nonzero={nz_out}")
