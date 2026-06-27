//============================================================================
// 74LS163 - synchronous 4-bit binary counter, SYNC clear   (74x16x family)
//----------------------------------------------------------------------------
// PART:       Presettable synchronous 4-bit binary (mod-16) up-counter.
//             Positive-edge clock; SYNCHRONOUS clear and SYNCHRONOUS load.
//             *** '163 = SYNCHRONOUS clear. The '161 (identical pinout) has
//             ASYNCHRONOUS clear - do not confuse. '160/'162 = decade. ***
// VARIATIONS: 74163 / 74LS163 / 74S163 / 74F163 share function AND pinout.
//             Lexicon P/Ns: 330-00712 (74LS163), 330-01287 (74S163).
// IN 224XL:   74LS163 (330-00712): ARU U45,U46,U47,U48,U49 ; T&C U1,U14.
//             74S163  (330-01287): T&C U4,U5,U17,U18,U41,U56.
//
// PINOUT (DIP-16):
//    1  /CLR     16  VCC     /CLR = synchronous clear, active LOW  (pin 1)
//    2  CLK      15  RCO     /LD  = synchronous load,  active LOW  (pin 9)
//    3  A (D0)   14  QA      ENP,ENT = count enables (both HIGH to count)
//    4  B (D1)   13  QB
//    5  C (D2)   12  QC
//    6  D (D3)   11  QD
//    7  ENP      10  ENT
//    8  GND       9  /LD
//
// FUNCTION (all actions on rising edge of CLK):
//   /CLR = LOW                  -> QA..QD = 0000 (synchronous; top priority).
//   /CLR=H, /LD = LOW           -> QA..QD <= (A,B,C,D) (synchronous load).
//   /CLR=H, /LD=H, ENP&ENT = H  -> COUNT UP (0..15, then wraps to 0).
//   /CLR=H, /LD=H, ENP&ENT != H -> HOLD.
//   RCO = HIGH when (QA..QD = 1111) AND (ENT = HIGH).  [ripple carry out]
//============================================================================
// SRC: KiCad 74xx.lib shared '16x pin map (160/161/162/163 pin-compatible);
//      '163 synchronous-clear behavior per TI datasheet. Confirm vs 060-01318.
