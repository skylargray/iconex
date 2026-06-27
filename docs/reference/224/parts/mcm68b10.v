//============================================================================
// MCM68B10 - 128 x 8 static RAM (6810)                      (6810 family)
//----------------------------------------------------------------------------
// PART:       128 bytes x 8 bits static RAM for M6800-family buses. Static
//             (no clock, no refresh). Bidirectional 3-state data bus. Six chip
//             selects (mixed polarity). BEHAVIORAL model.
// VARIATIONS: MCM6810 (1.0 MHz) / MCM68A10 (1.5) / MCM68B10 (2.0 MHz, 250 ns) -
//             same pinout, differ only in access time. 2nd-source MC6810/F6810.
//             Lexicon P/N: 350-02626 (MCM68B10).
// IN 224XL:   T&C (7.6): U2, U15, U29, U43.
//
// PINOUT (DIP-24):
//    1  GND        24  VCC
//    2  D0         23  A0
//    3  D1         22  A1
//    4  D2         21  A2
//    5  D3         20  A3
//    6  D4         19  A4
//    7  D5         18  A5
//    8  D6         17  A6
//    9  D7         16  R/W
//   10  CS0        15  /CS5
//   11  /CS1       14  /CS4
//   12  /CS2       13  CS3
//
// FUNCTION:
//   A0..A6 select one of 128 bytes. Device is selected only when ALL six chip
//   selects are asserted -- per the standard 6810: CS0 & CS3 = HIGH (pins 10 & 13,
//   each internally inverted) and /CS1,/CS2,/CS4,/CS5 = LOW (pins 11,12,14,15).
//   R/W = HIGH -> READ (D0..D7 driven); R/W = LOW -> WRITE (D0..D7 sampled).
//   Not selected -> D0..D7 high-impedance.
//============================================================================
// SRC: pinout + CS polarity DATASHEET-VERIFIED from the Motorola MCM6810 block
//      diagram (datasheets/mcm68a10p_mot.pdf), 2026-06-26.
//      CORRECTION: prior file had CS3/CS4 polarity swapped. Datasheet shows CS3
//      (pin13) active-HIGH (internal inverter) and /CS4 (pin14) active-LOW; the two
//      active-high selects are CS0 & CS3. Confirm wiring vs schematic 060-02475.
