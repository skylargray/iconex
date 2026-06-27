//============================================================================
// 74LS194 - 4-bit bidirectional universal shift register  (74x194 family)
//----------------------------------------------------------------------------
// PART:       4-bit register with 4 synchronous modes (hold / shift-right /
//             shift-left / parallel-load) chosen by S1,S0. Positive-edge
//             clocked; asynchronous active-LOW clear.
// VARIATIONS: 74194 / 74LS194 / 74S194 share function AND pinout.
//             Lexicon P/N: 330-01288 (74LS194).
// IN 224XL:   ARU board (7.7): U3, U4, U15, U16, U17, U18.
//
// PINOUT (DIP-16):
//    1  /CLR     16  VCC
//    2  SR_SER   15  QA      SR_SER = shift-right serial in (pin 2)
//    3  A        14  QB      SL_SER = shift-left  serial in (pin 7)
//    4  B        13  QC
//    5  C        12  QD
//    6  D        11  CLK
//    7  SL_SER   10  S1
//    8  GND       9  S0
//
// FUNCTION (rising edge of CLK, unless /CLR asserted):
//   /CLR = LOW   -> QA..QD = 0   (asynchronous, overrides everything)
//   S1 S0 = 0 0  -> HOLD (no change)
//   S1 S0 = 0 1  -> SHIFT RIGHT: (QA,QB,QC,QD) <= (SR_SER,QA,QB,QC)
//   S1 S0 = 1 0  -> SHIFT LEFT : (QA,QB,QC,QD) <= (QB,QC,QD,SL_SER)
//   S1 S0 = 1 1  -> LOAD:        (QA,QB,QC,QD) <= (A,B,C,D)
//============================================================================
// SRC: KiCad 74xx.lib pin map; function per CalStateLA digital-lab IC specs.
//      Confirm against schematic 060-01318.
