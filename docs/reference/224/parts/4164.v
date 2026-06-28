//============================================================================
// 4164 - 65,536 x 1 dynamic RAM (DRAM)                      (4164 family)
//----------------------------------------------------------------------------
// PART:       64K x 1-bit DRAM. 8-bit multiplexed address (A0..A7): row latched
//             by /RAS, column by /CAS. Separate data-in (Din) and data-out
//             (Dout). Requires periodic refresh (256 rows). BEHAVIORAL model.
// VARIATIONS: 4164 / uPD4164 / MK4564 / TMS4164 / MB8264 / HM4864 (many vendors,
//             identical 16-pin pinout). 41256 (256Kx1) is a superset: pin 1
//             becomes A8. Lexicon P/N: 350-03439 (4164, 64Kx1, 150 ns).
// IN 224XL:   DMEM (7.5): U20..U35  (16 devices = the 64K x 16 delay memory).
//
// PINOUT (DIP-16):
//    1  NC        16  GND (VSS)
//    2  Din       15  CAS/
//    3  WR/       14  Dout
//    4  RAS/      13  A6
//    5  A0        12  A3
//    6  A2        11  A4
//    7  A1        10  A5
//    8  VCC        9  A7
//
// FUNCTION:
//   Row:  drive A0..A7 = row address, /RAS falling edge latches it.
//   Col:  drive A0..A7 = col address, /CAS falling edge latches it.
//   /WE = HIGH -> READ  (Dout valid after /CAS); /WE = LOW -> WRITE (Din sampled).
//   Dout is 3-state except during a read. Refresh: cycle all 256 row addresses
//   with /RAS within the device refresh period.
//============================================================================
// SRC: NEC uPD4164 (NEC 1981 catalogue) + C64-wiki ASCII pinout - both agree
//      (1=NC,2=Din,3=/WE,4=/RAS,8=VCC,14=Dout,15=/CAS,16=GND). Confirm vs 060-01318.
