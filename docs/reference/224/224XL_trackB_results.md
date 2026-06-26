# Track B Adversarial Verification — Faithful ARU vs. un-suppressed POST

**Tool:** `tools/_trackB_post.py`  **Verifier:** independent re-run + disassembly cross-check.  **Date:** 2026-06-26.

## Verdict: PARTIAL SIGNATURE — two firmware self-tests genuinely pass on a faithful ARU; two named blockers remain.

| Sub-test | Firmware addr | Verdict | Asserted by |
|---|---|---|---|
| ARU LATCH echo (E32) | 0x0A1D–0x0A37 | **PASS (un-suppressed, no shim)** | reached 0x0A37 past both CP C compares, no DIAG |
| Register/"signature" walking pattern (E51-7F) | 0x0C48 | **PASS (un-suppressed, needs bustest shim)** | firmware error-acc `0x3C40==0` at `RET z` (0x0C74) |
| U42 8080 bus-test register (E34) | 0x0A82–0x0B3F, IN(0x04)@0x0B1D | **BLOCKS (un-modeled, non-ARU)** | multibus self-loopback, not datapath |
| Multiplier test (E83) | 0x0942 | **FAIL — 1 LSB** | firmware golden @0x9E5; `JP 0x021D` on mismatch |
| DMEM test (E91-96), normal-op | 0x0B75 / 0x813B | **Not reached** | gated behind A/B above |

## Reproduction
Re-ran the tool. All builder numbers matched exactly: ADD'L MULT 5/5, register-echo 8/8; BOOT 1 (no shim) → first DIAG **E34** caller=0x0B63; BOOT 2 (shim) → latch PASS, register PASS, first DIAG **E83** caller=0x0955, last step `l2=7E l3=A9 cmag=21 in=0x5555 RES=-14336`.

## Cheating check — CLEAN on the two claimed passes
- **DIAG handlers intact.** Disassembly of the loaded image: `0217: LD E,A / LD A,'H'`, `021D: LD E,A / LD A,'E'` — not `C9 RET`. Both boots run `suppress_post=False`; the patch is guarded behind `if suppress_post:` and never fires.
- **Golden bytes are firmware-owned, not hardcoded.** Register golden table @0xCC3 = `..55/..66/..77/..EE` + complements; multiplier golden @0x9E5 = `C7FF 37FF BCCC 4332 3800 C800 4333 BCCD`. The firmware does its own `CP (HL)` / `CP C` compares.
- **Register PASS is firmware-asserted.** `0x0C48` zeroes `0x3C40`, accumulates mismatches via `0x0CB3`, then `LD A,(0x3C40); OR A; RET z`. Verified `0x3C40==0` at the RET.
- **Not a trivial echo.** Tracing all 21 single-steps with register-file state: in the compare phase the input latch is frozen at 0xEEEE/0x1111 while WA=3, but readbacks for RA=0/1/2 return the DISTINCT preloaded 0x5555/6666/7777. The 4×16 regfile must genuinely store/retrieve four separate words — real datapath fidelity, not pass-through.
- **Chain order verified** from POST dispatcher @0x08F0: `0A1D latch → 0C48 register → 0942 multiplier → 0B75 DMEM`. Register test genuinely precedes the multiplier test.

### The one acknowledged crutch
`shim_bustest` feeds `cpu.C` back for `IN(0x03/0x04)` only inside the `0x0A82–0x0B40` window, bypassing the **U42** self-loopback (manual: "U42 forms the bus test register... sample and read its own data bus DATA/"). This is legitimately outside the ARU, but it means the register PASS holds **only with the shim**. With fully faithful ports POST halts at **E34** before completing — so "boots to normal operation, POST fully un-suppressed" is **not achieved**.

## Remaining failures
**(A) E34 / U42 bus-test (0x0B1D `IN A,(0x04)`).** SBC reads the byte it itself drives on DATA/ — a multibus-cycle artifact, not value-representable, not the ARU. Correctly isolated, but un-modeled.

**(B) E83 / multiplier 1-LSB.** Firmware golden for `0x5555 × -21/32` = `0xC7FF` (-14337). Value-level `(x<<3)*cs>>5 = -14336` (0xC800). Exact -14335.78 floors to -14336; the firmware's gate-level modified-Booth serial multiply (independently-truncated shifted partials + CSIGN active-low 74F283 subtract carry) lands one more LSB negative. All 4 records off by +1 LSB, same direction. No value-level floor/bias/shift variant reproduces 0xC7FF while keeping the cmag=32 unity path exact. This corroborates Session 9: the last-LSB / signature fidelity needs the netlist-level multiplier, not a parallel approximation.

## Notable correction flagged
To pass these tests the builder applied a **CSIGN active-low** convention: CSIGN=1 → POSITIVE coeff (register test reads +R[RA]), CSIGN=0 → negate (multiplier -21/32). This is firmware-grounded and load-bearing here, and is the OPPOSITE of the prior audio-path frontier decode in the reference docs — a genuine conflict to reconcile in Track C.

## Bottom line
Track B's exit criterion ("firmware boots to normal operation with no suppressed POST errors") is **not met**. But its fallback clause ("document exactly which sub-test fails and what it implies") is satisfied with high-value, non-circular evidence: a faithful 4×16 regfile + /32 unity datapath + single-step co-emulation **passes two real, un-suppressed firmware self-tests** (LATCH, register walking-pattern @0x0C48), and the only remaining ARU-datapath gap is a precisely characterized irreducible ±1-LSB gate-level serial-multiply truncation. The latch and register tests should graduate from 🟡 toward ✅ for the I/O-model and register-file claims; the multiplier last-LSB and U42 stay 🟡/⚪ pending gate-level multiplier emulation.