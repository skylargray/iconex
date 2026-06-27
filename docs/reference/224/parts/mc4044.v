//============================================================================
// MC4044 - phase-frequency detector + charge pump + amplifier  (MC4344/MC4044)
//----------------------------------------------------------------------------
// PART:       PLL building block with FOUR separately-pinned sections:
//             (1) phase-freq detector #1  (2) phase-freq detector #2
//             (3) charge pump             (4) on-chip Darlington amplifier.
//             Accepts TTL R/V inputs, generates an error voltage proportional
//             to freq/phase difference. Semi-analog -> BEHAVIORAL model only.
// VARIATIONS: MC4044 (P plastic / L ceramic) / MC4344 (same die). 14-pin.
//             Combine with an MC4324/4024 or MC1648 VCO for a full loop.
//             Lexicon P/N: 330-01298 (MC4044).
// IN 224XL:   T&C (7.6): U27   (sample-clock / VCO phase lock).
//
// PINOUT (DIP-14):
//    1  R          14  VCC
//    2  D1         13  U1
//    3  V          12  U2
//    4  PU         11  PD
//    5  UF         10  DF
//    6  D2          9  Amp In (A)
//    7  GND         8  Output
//
// FUNCTION (four independent sections):
//   PD#1 (sequential): inputs R, V -> outputs U1, D1. Both HIGH = locked
//        (R,V equal in freq AND phase). Responds only to NEGATIVE transitions
//        (duty-cycle independent). V slower/lagging -> U1 LOW; V faster/
//        leading -> D1 LOW.
//   PD#2 (combinatorial quadrature): shared R, V -> outputs U2, D2. Used as an
//        out-of-lock / loss-of-lock indicator (needs 50% duty inputs).
//   Charge pump: inputs PU, PD (wire PU from U1/U2, PD from D1/D2) -> outputs
//        UF, DF (fixed-amplitude +/- pulses to the loop filter).
//   Amplifier: on-chip Darlington, Amp In (pin 9) -> Output (pin 8); serves as
//        the loop-filter amplifier (Output Vmax <= 8.0 V).
//============================================================================
// SRC: Motorola MC4344/MC4044 datasheet (user-provided): PIN ASSIGNMENT +
//      LOGIC DIAGRAM (VCC=14, GND=7) - pin numbers verified. Confirm against
//      schematic 060-02475.
