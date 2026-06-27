//============================================================================
// AM8304B - octal 3-state bidirectional bus transceiver, NONINVERTING
//----------------------------------------------------------------------------
// PART:       8-bit bidirectional bus transceiver (AMD). Two 8-bit ports A and
//             B; direction set by T/R, both ports forced to 3-state by Chip
//             Disable. NONINVERTING (data passes straight through). Functionally
//             a 74x245-class transceiver, but note the control polarity below.
//             *** Am8304B = NONINVERTING ; the Am8303 is the INVERTING twin. ***
// VARIATIONS: Am8304B / Am7304B (commercial / military temp, same die,
//             noninverting). Am8303 / Am7303 = inverting version, same pinout.
//             Lexicon P/N: 330-01302 ("AM8304 N" = Am8304B, plastic DIP-20).
// IN 224XL:   T&C (7.6): U3, U16, U30, U44  -- one per MCM68B10 SRAM
//             (U2/U15/U29/U43): the SRAM data-bus transceiver.
//
// PINOUT (DIP-20):
//    1  A0       20  VCC
//    2  A1       19  B0
//    3  A2       18  B1
//    4  A3       17  B2
//    5  A4       16  B3
//    6  A5       15  B4
//    7  A6       14  B5
//    8  A7       13  B6
//    9  CD       12  B7
//   10  GND      11  T/R
//
// FUNCTION (CD = Chip Disable; T/R = Transmit/Receive direction):
//      CD   T/R   A port   B port
//       0    0     OUT      IN      (receive: B -> A)
//       0    1     IN       OUT     (transmit: A -> B)
//       1    X     HI-Z     HI-Z    (disabled)
//   CD is an active-HIGH disable (HIGH -> both ports 3-state; same effect as a
//   de-asserted active-LOW chip select). Data is non-inverted A<->B.
//============================================================================
// SRC: AMD "Am73/8303 . Am73/8304B Octal Three-State Bidirectional Bus
//      Transceivers" datasheet (user-provided) - connection diagram + logic
//      symbol + metallization layout + function table all agree. Confirm
//      against schematic 060-02475.
