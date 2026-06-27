//============================================================================
// 74F374 - octal D flip-flop, 3-state outputs, common CLK+/OE  (74x374 family)
//----------------------------------------------------------------------------
// PART:       Eight edge-triggered D flip-flops, common positive-edge clock
//             (CP) and common 3-state output enable (/OE). NOTE: '374 is an
//             EDGE-triggered register; the '373 is a transparent LATCH (diff
//             pinout). 20-pin package.
// VARIATIONS: 74374 / 74LS374 / 74S374 / 74F374 share function AND pinout.
//             Lexicon P/N: 330-03342 (74F374).
// IN 224XL:   ARU board (7.7): U10, U11, U43, U44.
//             T&C board (7.6): U31, U45.
//
// PINOUT (DIP-20):
//    1  /OE      20  VCC      /OE = output enable, LOW  (pin 1)
//    2  Q0       19  Q7       CP  = clock, rising edge  (pin 11)
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
//   Rising edge of CP: Qn <= Dn  (all 8 bits captured together).
//   /OE = HIGH -> Q0..Q7 high-impedance (Z); stored data unaffected.
//   /OE = LOW  -> stored data driven onto Q0..Q7.
//============================================================================
// SRC: KiCad 74xx.lib pin map; standard '374 function.
//      Confirm against schematic 060-01318.
