//============================================================================
// 74LS123 - dual retriggerable monostable multivibrator    (74x123 family)
//----------------------------------------------------------------------------
// PART:       Two retriggerable one-shots (monostables) with clear. Each fires
//             a single output pulse on a trigger edge; the pulse WIDTH is set
//             by an external R (Rext->VCC) and C (across Cext-RCext): tw ~ K*R*C.
//             Retriggerable: a new trigger during the pulse restarts/extends it.
//             *** Timing is analog (RC-set), not a pure logic delay. ***
// VARIATIONS: 74123 / 74LS123 / 74S123 / 74HC123 share function AND pinout.
//             Lexicon P/N: 330-01316 (74LS123).
// IN 224XL:   T&C (7.6): U13.
//
// PINOUT (DIP-16):  *** CORRECTED 2026-06-26 from datasheet (see SRC) ***
//    1  1A         16  VCC
//    2  1B         15  1Rext/Cext
//    3  1/CLR      14  1Cext
//    4  1/Q        13  1Q
//    5  2Q         12  2/Q
//    6  2Cext      11  2/CLR
//    7  2Rext/Cext 10  2B
//    8  GND         9  2A
//   NOTE: the '123 cross-couples the two one-shots across the package -
//   one-shot 2's Q/Cext/Rext are pins 5/6/7, one-shot 1's are pins 13/14/15.
//
// FUNCTION (per one-shot; /CLR = HIGH to allow triggering):
//   Trigger on FALLING edge of A (with B = HIGH), or RISING edge of B
//   (with A = LOW) -> Q pulses HIGH (/Q pulses LOW) for tw ~ K*R*C.
//   /CLR = LOW -> terminates pulse immediately / inhibits (Q = LOW).
//============================================================================
// SRC: pinout DATASHEET-VERIFIED from TI SDLS043 (datasheets/74123_TI.pdf), 2026-06-26.
//      CORRECTION: the prior KiCad-sourced map had one-shot 1 and one-shot 2's
//      Q/Cext/Rext nets swapped between pins 5,6,7 and 13,14,15. Datasheet is
//      authoritative: pin5=2Q, pin6=2Cext, pin7=2Rext/Cext; pin13=1Q, pin14=1Cext,
//      pin15=1Rext/Cext. Still confirm in-circuit usage against schematic 060-02475 (T&C U13).
