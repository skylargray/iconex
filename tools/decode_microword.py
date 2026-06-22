#!/usr/bin/env python
"""
224XL ARU microword per-step decoder.

Reconciled bit-field map (active-low storage; see report). For each step S the
4 stored bytes live at 0x4000 + S*4 + lane, lane 0..3:

  lane0 = OFST low byte   (stored active-low)
  lane1 = OFST high byte  (stored active-low)   -> offset = ~(lane1<<8|lane0) & 0xFFFF
                                                    delay  = offset (DMEM addr = pos - offset)
  lane2 = CONTROL byte, read as ctl = (~lane2) & 0xFF (complement):
            bit7   = ZERO   (clear accumulator at section start)
            bit6   = PROTECT / MAC-enable (operate)
            bits5:2= RA / XFER MAC-phase field (read-addr + transfer; not fully split)
            bits1:0= WA   (register-file write address, 1 of 4; 3 = pass-through)
  lane3 = COEFFICIENT byte, read RAW (NOT complemented for magnitude):
            bit7   = CSIGN  (raw bit7 = 1 -> negative)            [active-low]
            bits6:0= 7-bit magnitude, value = mag/127

A step whose coeff+control half is stored 0xFFFF (lane2==lane3==0xFF) is a
NOP / pure-delay fill step (coeff = 0).

Usage:  python tools/decode_microword.py [power_up_id_hex]   (default 0x01 CONCERT HALL)
"""
import sys
sys.path.insert(0, 'tools')
import boot_xl as B


def decode(power_up_id=0x01):
    cpu, mem, *rest = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    out = []
    for s in range(128):
        o = s * 4
        l0, l1, l2, l3 = img[o], img[o+1], img[o+2], img[o+3]

        offset = (~(l0 | (l1 << 8))) & 0xFFFF          # active-low 16-bit
        nop = (l2 == 0xFF and l3 == 0xFF)

        # coefficient (lane3, raw magnitude, raw active-low sign)
        mag = (l3 & 0x7F) / 127.0
        csign = (l3 >> 7) & 1                            # 1 = negative
        coeff = -mag if csign else mag

        # control (lane2, complemented) -- RA/XFER resolved via the ARU datapath model
        ctl = (~l2) & 0xFF
        zero    = (ctl >> 7) & 1
        protect = (ctl >> 6) & 1
        ra      = (ctl >> 4) & 3                          # bits5:4 = read-register addr (RA1,RA0)
        rw      = (ctl >> 3) & 1                          # bit3 = DMEM read/write or DAB-source sel
        xfer    = (ctl >> 2) & 1                          # bit2 = XFER (load result reg / write tank)
        wa      = ctl & 3

        if nop:
            out.append(dict(step=s, delay=offset, nop=True))
        else:
            out.append(dict(step=s, delay=offset, coeff=round(coeff, 3),
                            CSIGN=csign, WA=wa, RA=ra, RW=rw, XFER=xfer,
                            ZERO=zero, PROT=protect, nop=False))
    return out


if __name__ == '__main__':
    pid = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x01
    rows = decode(pid)
    print(f"# power_up_id=0x{pid:02x}")
    print(f"{'S':>3} {'delay':>6} {'coeff':>7} {'SGN':>3} {'WA':>2} {'RA':>2} "
          f"{'RW':>2} {'XF':>2} {'ZR':>2} {'PR':>2}")
    for r in rows:
        if r['nop']:
            print(f"{r['step']:3d} {r['delay']:6d}    NOP (pure delay / fill)")
        else:
            print(f"{r['step']:3d} {r['delay']:6d} {r['coeff']:+7.3f} "
                  f"{r['CSIGN']:3d} {r['WA']:2d} {r['RA']:2d} "
                  f"{r['RW']:2d} {r['XFER']:2d} {r['ZERO']:2d} {r['PROT']:2d}")
