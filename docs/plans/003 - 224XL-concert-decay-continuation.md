# 224XL CONCERT decay — SUPERSEDED

This file's original "final 3×10⁻⁴ continuation brief" framed the problem as a **sub-LSB rounding** fix.
That premise was **refuted** by a full systematic-debugging investigation (2026-06-22/23).

**→ See the consolidated record: [`224XL-concert-decay-investigation.md`](224XL-concert-decay-investigation.md)**

It contains: the executive summary, the verified-faithful reconstruction, every hypothesis tested with its
verdict (incl. the refuted rounding/LFO/closer-ordering/timing/sign/RA/crossover-addressing/arithmetic-idiom
paths), the structural root cause (frequency-dependent band-split decay; the mid-band is under-damped), the
full tool catalog (`tools/exp_*.py`, `tools/echo_*.py`), and the open fork (behavioral hardware check vs a
V7.2-calibrated HF-damping element). Do not re-run the refuted paths.
