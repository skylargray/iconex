# 224XL v8.2.1 - record -> program-name + reverb-algorithm map

Recovered by booting the **real** v8.2.1 firmware in the Z80 emulator past its DSP power-up
self-test and reading the program name the firmware transmits to the LARC display, then
decoding each record's delay tap-map + coefficient gains. Tools: `tools/boot_xl.py`
(boot + name capture), `tools/harvest_xl.py` (driver), `tools/aru224_emulate.py` (delay/gain
decode). Names independently cross-checked 20/20 against the NVS3 directory @0xA446; the
non-FE delay tables were validated byte-identical to the firmware's own load.

All 20 programs have name + delays + gains decoded. Records are the 21-entry @0xB800 array,
walked with the firmware page-wrap stride (+0x2AA, +2 when low byte == 0xFE). Selector ID =
the record's first byte. Two build paths: **FE** (recbase+0x30==0xFE) computes offsets via
ptr-writeptr; **non-FE** copies a pre-built 128-entry offset table from recbase+0xA7..0x2A7.

| rec | base | ID | program (B=bank P=prog) | path | steps | taps | range (samp) | recirc loop |
|----:|------|----|--------------------------|------|----:|----:|------|------|
| 0 | 0xB800 | 0x01 | CONCERT HALL (B1 P1) | FE | 104 | 63 | 128..12353 | 6008x4 |
| 1 | 0xBAAA | 0x02 | PLATE (B3 P1) | FE | 99 | 61 | 128..12353 | 706x6 |
| 2 | 0xBD54 | 0x81 | INVERSE ROOM (B2 P6) | FE | 107 | 59 | 16..12353 | 4097x11 |
| 3 | 0xC000 | 0x08 | CHAMBER (B2 P3) | non-FE | 99 | 45 | 2047..16089 | 4097x3 |
| 4 | 0xC2AA | 0x10 | CD PLATE B (B3 P4) | non-FE | 101 | 70 | 61..16083 | 16083x5 |
| 5 | 0xC554 | 0x20 | BRIGHT HALL (B1 P2) | FE | 104 | 63 | 128..12353 | 6008x4 |
| 6 | 0xC800 | 0x40 | SMALL ROOM (B2 P2) | non-FE | 104 | 65 | 90..12353 | 6651x4 |
| 7 | 0xCAAA | 0x05 | DARK HALL (B1 P3) | FE | 106 | 61 | 255..12353 | 2745x4 |
| 8 | 0xCD54 | 0x21 | CD PLATE A (B3 P3) | non-FE | 99 | 58 | 16..15526 | 1009x4 |
| 9 | 0xD000 | 0x06 | HALL/HALL (B5 P1) | non-FE | 101 | 45 | 244..15356 | 2665x2 |
| 10 | 0xD2AA | 0x0A | PLATE/PLATE (B5 P2) | non-FE | 103 | 56 | 61..16220 | 4097x3 |
| 11 | 0xD554 | 0x12 | PLATE/HALL (B5 P3) | non-FE | 103 | 53 | 61..16381 | 61x2 |
| 12 | 0xD800 | 0x0C | CHORUS&ECHO (B4 P1) | non-FE | 99 | 61 | 61..12289 | 3075x4 |
| 13 | 0xDAAA | 0x14 | RES CHORDS (B4 P2) | non-FE | 28 | 11 | 1088..12289 | 6529x5 |
| 14 | 0xDD54 | 0x24 | M BAND DELAY (B4 P3) | non-FE | 79 | 47 | 61..12289 | 1025x6 |
| 15 | 0xE000 | 0x22 | PLATE/CHORUS (B5 P4) | FE | 104 | 39 | 20..15451 | 1537x5 |
| 16 | 0xE2AA | 0x11 | RICH PLATE (B3 P5) | FE | 108 | 61 | 16..12353 | 4097x8 |
| 17 | 0xE554 | 0x80 | RICH CHAMBER (B2 P4) | FE | 107 | 59 | 16..12353 | 4097x10 |
| 18 | 0xE800 | 0x42 | RICH SPLIT (B5 P5) | FE | 103 | 36 | 16..15451 | 4097x6 |
| 19 | 0xEAAA | 0x41 | DARK CHAMBER (B2 P5) | FE | 107 | 60 | 16..12353 | 4097x10 |

Delay convention: delay = -offset (samples) at 34.13 kHz; the recirc-loop column is the
most-reused in-range tap. non-FE records also carry a tight cluster of large write-offsets
(>16383) = the recirculating-tank write region.

## Coefficient gains per record (sign-magnitude / 127)

- **rec 0 CONCERT HALL** (52 fetches): -1.000, -0.811, -0.787, -0.748, -0.724, -0.591, -0.559, -0.496, -0.488, -0.472, -0.346, -0.181, -0.055, +0.976
- **rec 1 PLATE** (55 fetches): -1.000, -0.969, -0.937, -0.819, -0.748, -0.496, -0.488, -0.472, -0.402, -0.346, -0.331, -0.299, -0.244, -0.150, +0.000, +0.976
- **rec 2 INVERSE ROOM** (47 fetches): -1.000, -0.969, -0.953, -0.945, -0.937, -0.819, -0.598, -0.496, -0.488, -0.472, -0.346, -0.339, -0.244, -0.150, -0.024, +0.000, +0.976
- **rec 3 CHAMBER** (31 fetches): -0.937, -0.819, -0.748, -0.685, -0.654, -0.598, -0.551, -0.496, -0.370, -0.220, -0.150, -0.031, +0.976
- **rec 4 CD PLATE B** (58 fetches): -1.000, -0.969, -0.937, -0.819, -0.654, -0.622, -0.591, -0.559, -0.535, -0.496, -0.472, -0.346, -0.244, -0.213, -0.150, +0.000
- **rec 5 BRIGHT HALL** (52 fetches): -1.000, -0.937, -0.787, -0.748, -0.724, -0.591, -0.559, -0.496, -0.488, -0.472, -0.346, -0.244, -0.181, -0.055, +0.976
- **rec 6 SMALL ROOM** (54 fetches): -1.000, -0.811, -0.787, -0.748, -0.724, -0.559, -0.496, -0.480, -0.472, -0.370, -0.339, -0.220, -0.181, -0.031, +0.976
- **rec 7 DARK HALL** (52 fetches): -1.000, -0.811, -0.787, -0.748, -0.724, -0.559, -0.496, -0.472, -0.370, -0.339, -0.220, -0.181, -0.031, +0.976
- **rec 8 CD PLATE A** (55 fetches): -1.000, -0.969, -0.937, -0.819, -0.685, -0.591, -0.559, -0.535, -0.496, -0.472, -0.409, -0.346, -0.244, -0.236, -0.213, -0.150, +0.000, +0.976, +0.984
- **rec 9 HALL/HALL** (50 fetches): -1.000, -0.811, -0.787, -0.748, -0.724, -0.591, -0.496, -0.472, -0.370, -0.220, -0.181, -0.031, +0.976
- **rec10 PLATE/PLATE** (54 fetches): -1.000, -0.969, -0.937, -0.819, -0.748, -0.496, -0.472, -0.402, -0.346, -0.331, -0.299, -0.244, -0.150, +0.000, +0.976
- **rec11 PLATE/HALL** (50 fetches): -1.000, -0.969, -0.937, -0.819, -0.811, -0.787, -0.748, -0.724, -0.591, -0.496, -0.472, -0.370, -0.346, -0.331, -0.244, -0.220, -0.181, -0.150, -0.031, +0.000, +0.976, +1.000
- **rec12 CHORUS&ECHO** (46 fetches): -1.000, -0.976, -0.496, -0.472, -0.402, -0.339, -0.307, -0.244, +0.976, +1.000
- **rec13 RES CHORDS** (56 fetches): -1.000, -0.496, -0.480, -0.472
- **rec14 M BAND DELAY** (63 fetches): -0.843, -0.496, -0.480, -0.472, -0.339, -0.244
- **rec15 PLATE/CHORUS** (48 fetches): -1.000, -0.969, -0.937, -0.819, -0.496, -0.488, -0.472, -0.339, -0.236, -0.220, -0.150, -0.008, +0.976, +1.000
- **rec16 RICH PLATE** (43 fetches): -1.000, -0.969, -0.953, -0.945, -0.937, -0.819, -0.496, -0.488, -0.346, -0.339, -0.244, -0.150, -0.024, +0.000, +0.976, +0.992, +1.000
- **rec17 RICH CHAMBER** (44 fetches): -1.000, -0.969, -0.953, -0.945, -0.937, -0.819, -0.496, -0.488, -0.346, -0.339, -0.244, -0.228, -0.220, -0.150, -0.024, -0.008, +0.000, +0.976, +0.992, +1.000
- **rec18 RICH SPLIT** (46 fetches): -1.000, -0.976, -0.969, -0.937, -0.819, -0.496, -0.488, -0.346, -0.339, -0.244, -0.220, -0.150, -0.008, +0.976, +0.992, +1.000
- **rec19 DARK CHAMBER** (42 fetches): -1.000, -0.969, -0.953, -0.945, -0.937, -0.819, -0.622, -0.606, -0.598, -0.496, -0.488, -0.346, -0.339, -0.244, -0.150, -0.024, -0.008, +0.000, +0.976, +0.992, +1.000
