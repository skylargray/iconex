//============================================================================
// 74LS377 - octal D flip-flop with clock enable            (74x377 family)
//----------------------------------------------------------------------------
// PART:       Eight positive-edge D flip-flops, common clock (CP) and common
//             active-LOW clock-enable (/E). Outputs always driven (NO 3-state;
//             that is the difference from the '374). 20-pin.
// VARIATIONS: 74377 / 74LS377 / 74S377 / 74F377 share function AND pinout.
//             Lexicon P/N: 330-01294 (74LS377).
// IN 224XL:   T&C (7.6): U19.
//
// PINOUT (DIP-20):
//    1  /E       20  VCC      /E = clock enable, active LOW (pin 1)
//    2  Q0       19  Q7       CP = clock, rising edge      (pin 11)
//    3  D0       18  D7
//    4  D1       17  D6
//    5  Q1       16  Q6
//    6  Q2       15  Q5
//    7  D2       14  D5
//    8  D3       13  D4
//    9  Q3       12  Q4
//   10  GND      11  CP
//
// FUNCTION:
//   Rising edge of CP:  /E = LOW  -> Qn <= Dn  (all 8 bits)
//                       /E = HIGH -> HOLD (no change).
//   Outputs Q0..Q7 are always driven (no high-impedance state).
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '377 (enable, no 3-state).
//      Confirm against schematic 060-01318.
