#!/usr/bin/env python3
"""224XL CONCERT reverb-tank harness (Session 10).

Goal: make the static-WCS CONCERT tank ring (RT60 ~ 20 s) under a SCHEMATIC-FAITHFUL DMEM model.

Schematic ground truth extracted this session from 060-02512 (sheets 1+2) + manual 3.6:
  * CPC = 16-bit counter U51+U65, incremented ONCE PER SAMPLE (manual 3.6).
  * addr = CPC - offset  (2's complement: adder U49/U50/U63/U64 adds OFST/ = ~offset with carry-in high).
  * DMEM = TWO banks of 64K x1 4164 DRAMs (U20-U35 = bank0 via CAS0/; U1-U16 = bank1 via CAS1/).
    OWNER-CORRECTED: parts list "IC, DRAM, 4164, 64KX1, 150NS" + photo images/224x_dmem.jpg (32 chips,
    two rows of 16). The schematic DRAWS the 4116 footprint (7 addr pins + 3 supplies) but jumpers
    J1-J4 (ECO 830126) reconfigure it for 4164 (pin9->A7, pin8=+5V) => 64K/bank => 128K total.
    Within-bank addr = A0..A15 (64K, muxed 8+8 onto AD0-AD7); A16 = bank select = carry-out of adder
    U64 (within=(pos-offset)&0xFFFF, bank=1 iff pos>=offset). Addr+control of ALL RAMs tied (manual 3.6);
    only CAS differs; bank reaches CAS0//CAS1/ via jumper J5 -> U58D (1/6 S04) -> U43A/U43B (1/3 S10).
  * DMASK=0xFFFF is the WITHIN-bank (64K) mask; total is 128K with bit16=bank. (Buffer size is NOT the
    dead-tank bug -- the impulse dies in EVERY size incl. true 128K; the bug is loop-gain/feedback routing.)

Datapath corrections kept from Session 9 (owner-confirmed):
  * MAC is IMMEDIATE (not deferred): per step  if ZERO: ACC=0; ACC=sat20(ACC + (x<<3)*cs>>5); if XFER: RES=sat16(ACC>>3)
  * Idle steps (MI17=0 & MI16=0) drive DAB = RES (result-register feedback), not 0.

Addressing modes (the experiment knob):
  linear  : single circular buffer, addr=(pos-offset)&mask        (mask=0x7FFF for 32K, 0xFFFF legacy)
  bank14  : two SEPARATE 16K regions, bank=(addr>>14)&1, within=(addr)&0x3FFF  [== linear 0x7FFF]
  obank14 : program-controlled bank = OFFSET bit14, within=(pos-offset)&0x3FFF  (separate streams)
  obank15 : program-controlled bank = OFFSET bit15, within=(pos-offset)&0x3FFF
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as AD


def sat16(x): return 32767 if x > 32767 else (-32768 if x < -32768 else x)
def sat20(x): return 262143 if x > 262143 else (-262144 if x < -262144 else x)


def classify(st, read_bit=1):
    """Return one of: 'wr','rd','rdrreg','rdad','xreg','idle'."""
    if st['MI17'] == 1 and st['MI16'] == read_bit:  return 'rd'
    if st['MI17'] == 1 and st['MI16'] != read_bit:  return 'wr'
    if st['MI17'] == 0 and st['MI16'] == 1:
        return {3: 'rdad', 1: 'rdrreg'}.get(st['sub'], 'xreg')
    return 'idle'


def cell_addr(pos, offset, mode):
    """Return (bank, within, key) for a DMEM access. key is a unique hashable cell id."""
    if mode == 'linear64':
        a = (pos - offset) & 0xFFFF;                       return 0, a, a
    if mode == 'linear32':
        a = (pos - offset) & 0x7FFF;                       return 0, a, a
    if mode == 'bank14':                 # == linear32, but explicit bank split
        a = (pos - offset) & 0x7FFF;     b = (a >> 14) & 1; return b, a & 0x3FFF, a
    if mode == 'obank14':                # program bank = offset bit14
        b = (offset >> 14) & 1;  w = (pos - offset) & 0x3FFF; return b, w, (b << 14) | w
    if mode == 'obank15':                # program bank = offset bit15
        b = (offset >> 15) & 1;  w = (pos - offset) & 0x3FFF; return b, w, (b << 14) | w
    if mode == 'obank1514':              # 2-bit program bank from offset bits 15,14 -> 4 regions of 16K
        b = (offset >> 14) & 3;  w = (pos - offset) & 0x3FFF; return b, w, (b << 14) | w
    raise ValueError(mode)


def run(prog, mode='linear32', nsamp=200000, imp=20000, read_bit=1, probe_every=256):
    R = [0, 0, 0, 0]
    ACC = 0; RES = 0
    DM = {}                              # sparse cell store: key -> value
    pos = 0
    energy = []                          # (sample, total |DM|, nonzero_cells, out_proxy)
    out_proxy_acc = 0
    for n in range(nsamp):
        pos = (pos + 1) & 0xFFFF
        sample_out = 0
        for st in prog:
            kind = classify(st, read_bit)
            offset = st['offset']
            b, w, key = cell_addr(pos, offset, mode)
            audio_in = imp if n == 0 else 0
            # resolve DAB source
            if kind == 'rdad':       dab = audio_in
            elif kind == 'rd':       dab = DM.get(key, 0)
            elif kind == 'rdrreg':   dab = RES
            elif kind == 'idle':     dab = RES            # CORRECTION 2: idle feeds result-reg
            else:                    dab = 0              # xreg / sub idle
            racc_in = R[st['RA']]
            R[st['WA']] = dab
            # CORRECTION 1: immediate MAC
            if st['ZERO']:
                ACC = 0
            ACC = sat20(ACC + ((racc_in << 3) * st['cs'] >> 5))
            if st['XFER']:
                RES = sat16(ACC >> 3)
                sample_out += abs(RES)
            if kind == 'wr':
                DM[key] = RES
        if n % probe_every == 0:
            tot = 0
            for v in DM.values(): tot += abs(v)
            energy.append((n, tot, len(DM), sample_out))
    return energy


def edc_rt60(energy, fs=34133.0):
    """Energy-decay: take total-DMEM-|.| curve, normalize, find -60 dB time (linear-fit on log)."""
    xs = [e[0] / fs for e in energy]
    ys = [e[1] for e in energy]
    pk = max(ys) or 1
    # peak region & late region
    peak_i = ys.index(pk)
    db = [(xs[i], 20 * math.log10((ys[i] + 1e-9) / pk)) for i in range(peak_i, len(ys))]
    # estimate slope over the span where db drops from -5 to -45 (avoid floor)
    seg = [(t, d) for t, d in db if -55 <= d <= -3]
    if len(seg) < 3:
        return None, db
    # least squares slope dB/s
    n = len(seg); st = sum(t for t, _ in seg); sd = sum(d for _, d in seg)
    stt = sum(t * t for t, _ in seg); std = sum(t * d for t, d in seg)
    denom = (n * stt - st * st) or 1e-9
    slope = (n * std - st * sd) / denom         # dB per second (negative)
    if slope >= 0:
        return None, db
    rt60 = -60.0 / slope
    return rt60, db


if __name__ == '__main__':
    prog = AD.load_microcode(0x01)
    # recirculation graph: which register each step writes (WA) / reads (RA)
    print("=== CONCERT step roles ===")
    roles = {}
    for st in prog:
        roles.setdefault(classify(st), []).append(st['s'])
    for k, v in roles.items():
        print(f"  {k:8s} x{len(v):2d}: {v}")
    print()
    modes = sys.argv[1:] or ['linear64', 'linear32', 'obank14', 'obank15', 'obank1514']
    N = 120000
    for mode in modes:
        en = run(prog, mode=mode, nsamp=N)
        peak = max(e[1] for e in en) or 1
        last = en[-1][1]
        maxcells = max(e[2] for e in en)
        endcells = en[-1][2]
        rt60, _ = edc_rt60(en)
        # energy at 0.1s, 0.5s, 1s, 3s
        def at(tsec):
            idx = min(range(len(en)), key=lambda i: abs(en[i][0] / 34133.0 - tsec))
            return en[idx][1]
        print(f"mode={mode:9s} peakE={peak:>10d} cells(max={maxcells:4d} end={endcells:4d}) "
              f"E@.1s={at(0.1):>9d} E@.5s={at(0.5):>9d} E@1s={at(1.0):>9d} E@3s={at(3.0):>9d} "
              f"RT60={'%.2f'%rt60 if rt60 else 'n/a':>6}")
