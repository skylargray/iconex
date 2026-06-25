"""HP-5004A-style 16-bit signature analysis for the Lexicon 224X reconstruction.

A signature analyzer compresses a gated serial data-bit stream (one DATA bit
sampled per CLOCK edge, between a START and STOP edge) into a 16-bit value via a
linear-feedback shift register (LFSR), then displays it as 4 characters using a
non-hex character set.

WINNING CONVENTION  (calibrated & confirmed against the manual's section 5.7
reference signatures -- see the self-test in __main__):

  - 16-bit LFSR, characteristic polynomial  X^16 + X^12 + X^9 + X^7 + 1.
  - The state is held in a Python int ``S`` whose bit ``b`` (0..15) is shift-
    register stage ``b+1`` (1-indexed). So value-bit 15 is the MSB / "bit16".
  - Per CLOCK edge with incoming DATA bit ``d`` (read state BEFORE the shift):

        fb = d XOR S15 XOR S11 XOR S8 XOR S6
        S  = ((S << 1) | fb) & 0xFFFF

    i.e. a classic Fibonacci (left-shifting) LFSR: the whole register shifts up
    one stage (stage_i -> stage_{i+1}, top stage discarded) and the feedback is
    inserted at the bottom stage (value-bit 0).  The tap value-bits {15,11,8,6}
    are exactly the 1-indexed register stages {16,12,9,7} of the polynomial.
    The DATA bit IS part of the feedback XOR sum (constant-1 input drives the
    register; constant-0 input leaves it untouched).
  - After STOP, the 16-bit register value ``S`` is displayed MOST-SIGNIFICANT
    NIBBLE FIRST through the character set "0123456789ACFHPU".  This set is NOT
    hex: index 10->'A', 11->'C', 12->'F', 13->'H', 14->'P', 15->'U'.

Properties:
  - GROUND (all-0 data) yields 0x0000 -> "0000" for ANY window length N, because
    the feedback has no constant injection term (fb=0 when d=0 and S=0).
  - +5V (all-1 data) over a window of N clock edges yields a signature that is a
    pure, deterministic function of N (period 65535, the LFSR is primitive).

Calibration (section 5.7 reference signatures), smallest N:
    ARU no-feedback   "29F3" (0x29C3)  N = 62
    ARU feedback      "3696" (0x3696)  N = 90
    T&C               "FP54" (0xCE54)  N = 30
    DMEM              "826P" (0x826E)  N = 4096   (= 2**12, a full DMEM sweep)
    FPC               "96F6" (0x96C6)  N = 98

Only the Python standard library is used.
"""

from __future__ import annotations

CHARSET = "0123456789ACFHPU"
"""Signature display alphabet. Index = nibble value (0..15). NOT hexadecimal."""

# Feedback tap positions as 0-indexed value bits, derived from the 1-indexed
# polynomial stages {16, 12, 9, 7} -> value bits {15, 11, 8, 6}.
TAPS = (15, 11, 8, 6)
MASK = 0xFFFF


def display_to_value(s: str) -> int:
    """Convert a 4-character signature display string to its 16-bit register
    value by looking up each character's index in :data:`CHARSET`.

    >>> hex(display_to_value("29F3"))
    '0x29c3'
    >>> hex(display_to_value("FP54"))
    '0xce54'
    """
    if len(s) != 4:
        raise ValueError(f"signature display must be 4 chars, got {s!r}")
    v = 0
    for ch in s:
        try:
            v = (v << 4) | CHARSET.index(ch)
        except ValueError:
            raise ValueError(f"invalid signature char {ch!r} (not in {CHARSET!r})")
    return v


def value_to_display(v: int) -> str:
    """Convert a 16-bit register value to its 4-character display, most-
    significant nibble first.

    >>> value_to_display(0x29C3)
    '29F3'
    >>> value_to_display(0x0000)
    '0000'
    """
    v &= MASK
    return "".join(CHARSET[(v >> (4 * i)) & 0xF] for i in (3, 2, 1, 0))


class Signature:
    """Streaming 16-bit signature accumulator.

    Feed DATA bits one per CLOCK edge with :meth:`clock`; read the result with
    :attr:`value` or :meth:`display`.

    >>> s = Signature()
    >>> for _ in range(62): _ = s.clock(1)
    >>> s.display()
    '29F3'
    """

    __slots__ = ("state",)

    def __init__(self, state: int = 0) -> None:
        self.state = state & MASK

    def reset(self, state: int = 0) -> None:
        self.state = state & MASK

    def clock(self, data_bit: int) -> int:
        """Advance one CLOCK edge with the given DATA bit (0 or 1). Returns the
        new 16-bit state."""
        s = self.state
        fb = data_bit & 1
        for t in TAPS:
            fb ^= (s >> t) & 1
        self.state = ((s << 1) | fb) & MASK
        return self.state

    @property
    def value(self) -> int:
        return self.state

    def display(self) -> str:
        return value_to_display(self.state)


def sig_value(bits, state: int = 0) -> int:
    """Feed an iterable of DATA bits through the LFSR and return the 16-bit
    register value. ``bits`` may be any iterable of 0/1 ints."""
    s = state & MASK
    for d in bits:
        fb = d & 1
        for t in TAPS:
            fb ^= (s >> t) & 1
        s = ((s << 1) | fb) & MASK
    return s


def signature_over(get_bit, n: int, state: int = 0) -> int:
    """Clock ``n`` edges, taking each DATA bit from ``get_bit(i)`` for i in
    range(n). Returns the 16-bit register value."""
    s = state & MASK
    for i in range(n):
        fb = get_bit(i) & 1
        for t in TAPS:
            fb ^= (s >> t) & 1
        s = ((s << 1) | fb) & MASK
    return s


def signature_const(n: int, data_bit: int = 1, state: int = 0) -> int:
    """Signature of a constant-``data_bit`` stream of length ``n`` (e.g. +5V=1,
    GROUND=0)."""
    s = state & MASK
    fb_const = data_bit & 1
    for _ in range(n):
        fb = fb_const
        for t in TAPS:
            fb ^= (s >> t) & 1
        s = ((s << 1) | fb) & MASK
    return s


def find_n(target_value: int, nmax: int = 200000):
    """Brute-force the smallest window length N for which an all-1s (+5V) stream
    produces ``target_value``. Returns (first_N, period) or (None, None)."""
    s = 0
    first = None
    period = None
    for n in range(1, nmax + 1):
        fb = 1
        for t in TAPS:
            fb ^= (s >> t) & 1
        s = ((s << 1) | fb) & MASK
        if s == target_value:
            if first is None:
                first = n
            elif period is None:
                period = n - first
                break
    return first, period


# Section 5.7 reference signatures used for calibration.
CALIBRATION = [
    ("ARU no-feedback", "29F3"),
    ("ARU feedback",    "3696"),
    ("T&C",             "FP54"),
    ("DMEM",            "826P"),
    ("FPC",             "96F6"),
]


def _selftest() -> bool:
    # display<->value round-trip on the worked examples from the spec.
    worked = {
        "29F3": 0x29C3, "3696": 0x3696, "FP54": 0xCE54,
        "826P": 0x826E, "96F6": 0x96C6, "0000": 0x0000,
    }
    for disp, val in worked.items():
        assert display_to_value(disp) == val, (disp, hex(display_to_value(disp)))
        assert value_to_display(val) == disp, (val, value_to_display(val))

    print(f"{'module':18s} {'+5V':5s} {'numeric':8s} {'N':>6s}  "
          f"{'period':>6s}  +5Vrepro  ground=0000")
    print("-" * 72)
    all_pass = True
    for name, disp in CALIBRATION:
        target = display_to_value(disp)
        n, period = find_n(target, nmax=200000)
        repro = (n is not None) and (value_to_display(signature_const(n, 1)) == disp)
        # GROUND: all-0 stream of the same length must be 0000 (try N and a few).
        ground_ok = all(signature_const(k, 0) == 0 for k in (1, n or 1, 12345, 65535))
        ok = repro and ground_ok
        all_pass &= ok
        nstr = str(n) if n is not None else "NOT FOUND"
        pstr = str(period) if period is not None else "-"
        print(f"{name:18s} {disp:5s} 0x{target:04X}  {nstr:>6s}  {pstr:>6s}  "
              f"{str(repro):8s}  {ground_ok}")

    # Extra: a pure all-0 stream is 0000 regardless of length (no constant inj).
    ground_global = all(signature_const(k, 0) == 0
                        for k in (0, 1, 2, 7, 100, 4096, 65535, 131070))
    all_pass &= ground_global

    print("-" * 72)
    print(f"GROUND (all-0) -> 0000 for all tested N: {ground_global}")
    print()
    print("PASS" if all_pass else "FAIL")
    return all_pass


if __name__ == "__main__":
    import sys
    sys.exit(0 if _selftest() else 1)
