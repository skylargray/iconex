//============================================================================
// 74LS367 - hex 3-state buffer, non-inverting, two OE groups (74x367 family)
//----------------------------------------------------------------------------
// PART:       Six non-inverting 3-state buffers split into two independently-
//             enabled groups: /G1 (pin 1, active-LOW) enables bits 1-3 on the
//             lower half; /G2 (pin 15, active-LOW) enables bits 4-6 on the
//             upper half. Inputs and outputs alternate per bit (A1,Y1,A2,Y2...).
//             NON-INVERTING (data passes straight through when enabled).
// VARIATIONS: 74367 / 74LS367 / 74S367 share function AND pinout.
//             74LS368 is the inverting version with the same pinout.
//             Lexicon P/N: (verify against 224X parts list).
// IN 224XL:   Verify against U-IC map.
//
// PINOUT (DIP-16):
//    1  /G1      16  VCC
//    2  A1       15  /G2
//    3  Y1       14  A6
//    4  A2       13  Y6
//    5  Y2       12  A5
//    6  A3       11  Y5
//    7  Y3       10  A4
//    8  GND       9  Y4
//
// FUNCTION:
//   Bits 1-3: /G1 = LOW  -> Y1..Y3 = A1..A3 (buffered, non-inverting).
//             /G1 = HIGH -> Y1..Y3 = HI-Z.
//   Bits 4-6: /G2 = LOW  -> Y4..Y6 = A4..A6 (buffered, non-inverting).
//             /G2 = HIGH -> Y4..Y6 = HI-Z.
//============================================================================
// SRC: NSC 74LS367 datasheet DIP connection diagram (user-supplied image,
//      read directly). Confirms /G1=pin1, /G2=pin15, A/Y pairs alternating,
//      GND=pin8, VCC=pin16. Confirm against schematic 060-01318.
