#!/usr/bin/env python3
"""224XL ARU datapath model (bit-exact reference for the C++ reconstruction).

SESSION 7 REBUILD (frontier decode). The microword decode was corrected to the owner's
T&C schematic trace (060-02475); see docs/plans/224XL-overunity-frontier.md. This fixed the
long-standing over-unity bug (8/13 programs hot -> 0 hot; CONCERT lossless). The TRUE 32-bit
microword = 4 stored bytes l0,l1,l2,l3 (= MI0-7, MI8-15, MI16-23, MI24-31):

  offset / delay OFST0-15 = MI0-15  (l0,l1)            offset = ~(l1<<8 | l0) & 0xFFFF
  lane2 (l2, used DIRECT, inv_l2=False):
    b0 = MI16 = DMEM read(1)/write(0) select          b4,b5 = RA0,RA1 (read register addr)
    b1 = MI17 = MEMAC (DMEM op enable; DRAM iff =1)    b6    = PROT (datapath-irrelevant)
    b2,b3 = WA0,WA1 (write register addr; 3=scratch)  b7    = CSIGN (coefficient sign)
  lane3 (l3, used COMPLEMENTED, inv_l3=True):
    b0 = MI24 = XFER (load result register)            b2..b7 = MI26-31 = C0..C5 (6-bit coeff mag)
    b1 = MI25 = ZERO (clear accumulator)
  lane1 (l1) bits 4,5 (used complemented) = MI12,MI13 = the non-DMEM sub-decoder select.

DEVICE DECODE (DAB source/dest) -- CONFIRMED by owner's net-by-net U47/U48 trace (060-02475):
  U47 (LS139 dual decoder) decoder-1 select=(A=MI16,B=MI17):
    Y2 (pin6, (MI17,MI16)=(1,0)) -> MEMW/  : DMEM WRITE  -> dab=RES (RDRREG co-asserts), DM[addr]<-RES
    Y3 (pin7, (MI17,MI16)=(1,1)) -> MEMR/  : DMEM READ   -> dab=DM[addr]
    Y1 (pin5, (MI17,MI16)=(0,1)) -> enables the sub-decoder (via U34A, gated by MI4 on pin2)
    Y0 (pin4, (MI17,MI16)=(0,0)) -> NOT CONNECTED -> DAB undriven.
  Sub-decoder (U47 decoder-2, select=(A=MI12,B=MI13)) ENABLED ONLY when Y1 active AND MI4=1:
    sub=(MI13<<1|MI12): 1=RDRREG/ (result reg -> DAB feedback), 3=RD AD/ (A/D audio in),
    2=RD XREG/ (host data, unmodeled), 0=idle.
  IDLE / undriven DAB (Y0=NC, or sub-decoder gated off by MI4=0): the DAB has NO pull resistors
  (schematic-confirmed) so it FLOATS and HOLDS its last driven value -- it is NOT 0.
  MI4 = offset bit 4 (the DP bit; ~l0 bit4). RDRREG/ on a write also needs DAB RSTB (MS1/MS8 strobe).

TIMING: MAC pipeline (Service Manual 3.7 + Fig 3.4) -- the multiply-and-accumulate result does not
become available until the very end of AS0 of the NEXT system cycle. So each step's product is added
to the accumulator one step LATE; XFER CK reads the accumulator (now holding the prior step's product)
and ZERO clears it, both at that instant. Implemented as a 1-step deferred product `pend`.

ARU arithmetic (schematic-confirmed 060-01318 + ADD'L MULT diagnostic 5.3.2): operand = x<<3;
prod = (operand*Cs)>>5 -- the 6-bit coefficient scale is /32, NOT /64 (the ADD'L MULT test multiplies
by 1 and by 5/4, i.e. coeff 32 = x1.0 and coeff 40 = x1.25, only representable at /32). Net per-step
gain = Cs/32. 20-bit saturating accumulator (rails +/-2^18); RES = sat16(ACC>>3).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

DMASK = 0xFFFF          # 64K-word DMEM (1 bank of 64K DRAM per manual)

# --- decode polarity (frontier-confirmed) ---
INV_L2 = False          # lane2 used direct (MEMAC = MI17 raw; RD AD/ at s75/s125)
INV_L3 = True           # lane3 used complemented (active-low C0/-C5/; 23% pure-delay move steps,
                        #   sane XFER/ZERO; NOP/all-off stored 0xFF -> 0x00. Schematic-consistent.)
INV_L1 = True           # MI12,MI13 from ~l1 bits 4,5
READ_BIT = 1            # MI16=1 => DMEM read (U47 LS139: MEMR/=MI17&MI16)


def decode_image(img, inv_l2=INV_L2, inv_l3=INV_L3, inv_l1=INV_L1):
    """Decode a 512-byte WCS image (4 active-low-ish bytes/step) to active-step dicts using the
    frontier map. NOP/pure-delay fill (l2==l3==0xFF) is skipped. Returns dicts with keys:
    s, offset, MI16, MI17, WA, RA, XFER, ZERO, csign, cs (signed 6-bit coeff), sub."""
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            continue
        vl1 = (~l1 & 0xFF) if inv_l1 else (l1 & 0xFF)
        v2 = (~l2 & 0xFF) if inv_l2 else (l2 & 0xFF)
        v3 = (~l3 & 0xFF) if inv_l3 else (l3 & 0xFF)
        offset = (~(l0 | (l1 << 8))) & DMASK
        MI16 = v2 & 1
        MI17 = (v2 >> 1) & 1
        WA = (v2 >> 2) & 3
        RA = (v2 >> 4) & 3
        csign = (v2 >> 7) & 1
        MI12 = (vl1 >> 4) & 1
        MI13 = (vl1 >> 5) & 1
        MI4 = (offset >> 4) & 1                 # DP bit = ~l0 bit4 = offset bit4; gates the sub-decoder
        xfer = v3 & 1
        zero = (v3 >> 1) & 1
        cmag = (v3 >> 2) & 0x3F
        cs = -cmag if csign else cmag
        prog.append(dict(s=s, offset=offset, MI16=MI16, MI17=MI17, WA=WA, RA=RA, MI4=MI4,
                         XFER=xfer, ZERO=zero, csign=csign, cs=cs, sub=(MI13 << 1) | MI12))
    return prog


def load_microcode(power_up_id=0x01, legacy=False, **kw):
    """Boot program <power_up_id> and decode its WCS image. legacy=True -> the old (pre-Session-7)
    decode, kept for A/B regression diffing only (it has the over-unity bug)."""
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    if legacy:
        return _load_microcode_legacy(img)
    return decode_image(img, **kw)


def sat16(x):
    return 32767 if x > 32767 else (-32768 if x < -32768 else x)


def sat20(x):
    """ARU accumulator/PP saturation (schematic-exact, 060-01318): the 74F157 sat-muxes substitute
    the B-IN pattern +0x3FFFF / -0x40000 = +262143 / -262144 = +/-2^18 on overflow."""
    return 262143 if x > 262143 else (-262144 if x < -262144 else x)


def _dab_source(st, DM, addr, RES, audio_in, last, read_bit=READ_BIT):
    """Resolve the DAB (data bus) source for a step under the CONFIRMED U47/U48 device decode.
    Returns (dab, is_dmem_write). `last` = the previous DAB value (the undriven bus holds it).

      (MI17,MI16)=(1,1) MEMR/ : DMEM read   -> DM[addr]
      (MI17,MI16)=(1,0) MEMW/ : DMEM write  -> RES (RDRREG co-asserts), DM[addr]<-RES
      (MI17,MI16)=(0,1) + MI4=1 : sub-decoder -> 1=RDRREG(RES) 3=RD AD(audio) 2=RD XREG(host) 0=idle
      otherwise (Y0=NC, or sub gated off by MI4=0) : DAB UNDRIVEN -> holds `last` (no pull resistors)."""
    is_read = st['MI17'] == 1 and st['MI16'] == read_bit
    if is_read:                                    # DMEM read
        return DM[addr], False
    if st['MI17'] == 1:                            # DMEM write (MI16 != read_bit)
        return RES, True
    if st['MI16'] == 1 and st['MI4'] == 1:         # sub-decoder enabled (Y1 active & MI4 gate)
        sub = st['sub']
        if sub == 1:                               # RDRREG/ : result register -> DAB (feedback)
            return RES, False
        if sub == 3:                               # RD AD/  : A/D audio input
            return audio_in, False
        return last, False                         # sub 2 (RD XREG, unmodeled) / 0 -> undriven hold
    return last, False                             # idle / gated-off : DAB floats, holds last value


def run_trace(prog, nsamp=4000, imp=20000, trace_window=64, read_bit=READ_BIT):
    """Frontier ARU datapath with acc_latch timing. Injects one impulse at the RD-AD (audio-in)
    step(s) at sample 0. Returns (esum_list, steps):
      esum_list[n]  : per-sample output energy = sum |RES| over XFER steps.
      steps         : flat per-step probes (n,s,addr,dab,racc_in,prod,acc,res) for n<trace_window,
                      res = RES after this step if XFER else SENT (INT64_MIN).
    ACC_prev (the acc_latch register) is a continuous pipeline register carried across steps AND
    samples; XFER loads RES = sat16(ACC_prev>>3)."""
    SENT = -(1 << 63)
    R = [0, 0, 0, 0]
    ACC = 0
    RES = 0
    pend = 0                                       # 1-step deferred MAC product (pipeline)
    DM = [0] * (DMASK + 1)
    pos = 0
    last = 0                                        # undriven DAB holds this (carries across steps+samples)
    esum_list = []
    steps = []
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        esum = 0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            audio_in = imp if n == 0 else 0
            dab, is_dmem_write = _dab_source(st, DM, addr, RES, audio_in, last, read_bit)
            last = dab
            racc_in = R[st['RA']]                  # LS670 read-before-write
            R[st['WA']] = dab
            # MAC pipeline (Manual 3.7): the prior step's product is available now -> add it;
            # XFER reads the (now-complete) accumulator; ZERO clears it; this step's product
            # is computed and DEFERRED to the next step.
            ACC = sat20(ACC + pend)
            if st['XFER']:
                RES = sat16(ACC >> 3)
                res_val = RES
                esum += abs(RES)
            else:
                res_val = SENT
            if st['ZERO']:
                ACC = 0
            prod = (racc_in << 3) * st['cs'] >> 5   # /32 coefficient scale (ADD'L MULT 5.3.2)
            pend = prod
            if is_dmem_write:
                DM[addr] = RES
            if n < trace_window:
                steps.append((n, st['s'], addr, dab, racc_in, prod, ACC, res_val))
        esum_list.append(esum)
    return esum_list, steps


def run(prog, nsamp=4000, imp=20000, read_bit=READ_BIT):
    """Per-sample output energy only (esum). See run_trace for the instrumented twin."""
    esum, _ = run_trace(prog, nsamp=nsamp, imp=imp, trace_window=0, read_bit=read_bit)
    return esum


def decay_metric(out):
    """How reverb-like: peak, then late-energy ratio + smoothness."""
    peak = max(out) or 1
    early = sum(out[:200]) / 200
    late = sum(out[2000:2200]) / 200
    return dict(peak=peak, early=round(early), late=round(late),
                late_ratio=round(late / (early or 1), 4))


# ===========================================================================
# LEGACY decode + datapath (pre-Session-7; the over-unity-buggy model). Kept ONLY for A/B
# regression diffing. NOT used by the golden/C++ reconstruction.
# ===========================================================================
def _load_microcode_legacy(img):
    prog = []
    for s in range(128):
        l0, l1, l2, l3 = img[s*4], img[s*4+1], img[s*4+2], img[s*4+3]
        if l2 == 0xFF and l3 == 0xFF:
            prog.append(None); continue
        ctl = (~l2) & 0xFF
        offset = (~(l0 | (l1 << 8))) & 0xFFFF
        coeff = (-(l3 & 0x7F) if l3 & 0x80 else (l3 & 0x7F))
        prog.append(dict(s=s, offset=offset, coeff=coeff,
                         ZERO=(ctl >> 7) & 1, b3=(ctl >> 3) & 1, XFER=(ctl >> 2) & 1,
                         WA=ctl & 3, b5=(ctl >> 5) & 1, b4=(ctl >> 4) & 1))
    return [p for p in prog if p]


def fpc_input_step(prog):
    """LEGACY FPC input-step fingerprint (offset bit15 set, WA!=3, low14==0x3FFF)."""
    for p in prog:
        if 'WA' in p and (p['offset'] & 0x8000) and p['WA'] != 3 and (p['offset'] & 0x3FFF) == 0x3FFF:
            return p['s']
    return None


if __name__ == '__main__':
    prog = load_microcode(0x01)
    print(f"CONCERT (frontier decode): {len(prog)} active steps")
    nzc = sum(1 for st in prog if st['cs'] == 0)
    nxf = sum(1 for st in prog if st['XFER'])
    nrd = sum(1 for st in prog if st['MI17'] == 0 and st['MI16'] == 1 and st['sub'] == 3)
    print(f"  zero-coeff move steps={nzc}  XFER={nxf}  RD-AD(input) steps={nrd}")
    esum, steps = run_trace(prog, nsamp=4000)
    m = decay_metric(esum)
    print(f"  peak={m['peak']} early={m['early']} late={m['late']} late/early={m['late_ratio']}")
