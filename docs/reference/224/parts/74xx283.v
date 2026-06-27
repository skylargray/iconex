//============================================================================
// 74x283 - 4-bit binary full adder with fast (look-ahead) carry  (74x283 family)
//----------------------------------------------------------------------------
// PART:       Adds two 4-bit operands A1..A4 + B1..B4 + carry-in C0 -> 4-bit sum
//             S1..S4 (Sigma) + carry-out C4. Internal carry look-ahead. Combinational.
// VARIATIONS: 74283 / 74LS283 / 74S283 / 74F283 share function AND pinout.
//             Lexicon P/N: (TBD - owner).
// IN 224XL:   ARU (7.7): U19,U20,U21,U22,U23 (74F283, accumulator adders) ;
//                        U13,U24,U25,U38,U39 (74F283, multiplier partial-product adders).
//             DMEM (7.5): U49,U50,U63,U64 (74S/LS283, the CPC-offset address adder).
//
// PINOUT (DIP-16):   (S=Sigma sum.  A1/B1/S1 = LSB = bit0 ... A4/B4/S4 = MSB = bit3)
//    1  S2       16  VCC
//    2  B2       15  B3
//    3  A2       14  A3
//    4  S1       13  S3
//    5  A1       12  A4
//    6  B1       11  B4
//    7  C0 (Cin) 10  S4
//    8  GND       9  C4 (Cout)
//
// FUNCTION:
//   {C4, S4..S1} = (A4..A1) + (B4..B1) + C0   (4-bit add with carry).
//   *** NOTE the "crossed" upper-nibble pin order ***: A3=14 / A4=12, S3=13 / S4=10,
//   B3=15 / B4=11 (it is NOT a linear 10..15 layout). Building a netlist from a
//   wrong assumption here silently bit-scrambles the upper nibble.
//============================================================================
// SRC: pinout DATASHEET-VERIFIED from TI SDLS095A (datasheets/74283_TI_SDLS095A.pdf),
//      2026-06-26. Matches the owner ARU pin trace (060-01318). Confirm DMEM usage
//      against schematic 060-02512.
