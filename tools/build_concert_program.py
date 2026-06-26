#!/usr/bin/env python3
"""Track E.1 builder: reconstruct the faithful per-microword CONCERT program (recbase 0xB800).

VALIDATED SPINE (Track A/C, non-circular):
  * OFFSET = offbuf[k] = aru224_emulate.tap_map(recbase, cce=SIZE)[k]   (SAMPLES; delay=+offset)
  * COEFF  = mem[recbase+0xAD+4*k]  (bit7=CSIGN, bits0-6 magnitude/127)  -> captured via the
            0xB510 hook (aru224_emulate.capture_coeffs) which fetches exactly recbase+0xAD+4*slot.
  * The interpreter (0xAA9F) emits, in bytecode order, AB0C->B510 slot references; each reference
    names index k. 52 references -> 52 offset-bearing microwords for CONCERT, in COEFF-MATCHED
    consecutive pairs (read-tap + accumulate-partner). This ordered (k, offset, coeff) stream IS the
    program spine and is what we emit per-microword.

CONTROL lanes (device/WA/RA/XFER/ZERO): owner-traced map decoded from the real 0x4000 hardware
  image (aru_datapath.decode_image) is TRUSTED for lane2/lane3 semantics. We attach, per emitted
  microword, the datapath role derived from the validated pair structure (see method below) so the
  recirculating loop closes. We DO NOT read offsets from the 0x4000 image (Track C: garbage).

SPECIAL TAPS (handled explicitly):
  * offset == -1 (0xFFFF): sentinel / write-head marker (the FE/non-FE fill value). Treated as a
    DMEM WRITE head (store the running accumulator into the delay line) rather than an ordinary read.
  * large-negative (e.g. -12289/-12353, -4097, -4481, -5249): special taps. -4097 = -(4096+1) and
    -12289 = -(12288+1) are loop/wrap write-pointers (negative = "write at CPC+|off|" head, i.e. the
    delay-line input side). The single large-negative -12353 at slot 0 (step 0 partner) is the audio
    INPUT injection tap. These are emitted as WRITE/input taps, not read taps.

Run: python tools/build_concert_program.py            # builds CONCERT @ cce=0, writes CSV+JSON
"""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru224_emulate as A

RECBASE = 0xB800
FS = 34130.0          # ARU sample rate (Hz)


def slot_sequence(recbase=RECBASE):
    """Ordered (k, coeff_byte) slot-reference stream emitted by the interpreter, via the B510 hook."""
    cf = A.capture_coeffs(recbase)
    return [(((de - 0x4003) // 4) & 0xFF, b) for de, b in cf]


INPUT_OFFSET = -12353                  # step-0 partner: audio injection point (SIZE-invariant)


def classify_tap(offset):
    """Datapath role of a tap from its (signed) offset word. SIZE-robust: keyed on the special
    sentinels, not magnitude (delays scale with SIZE; -1 and -12353 do NOT)."""
    if offset == -1:
        return 'WRITE_HEAD'            # 0xFFFF sentinel = delay-line write head
    if offset == INPUT_OFFSET:
        return 'INPUT'                 # audio injection point (step-0 partner, SIZE-invariant)
    if offset < 0:
        return 'WRITE_NEG'             # negative wrap write-pointer (loop input / write side)
    return 'READ'                      # ordinary positive delay tap (read)


def build_program(recbase=RECBASE, cce=0, ccf=0):
    """Per-microword program from the validated slot-keyed spine.

    Returns list of dicts (emission order), each:
      idx        : emission position (0..N-1)
      slot_k     : the named slot index k (bytecode byte AND 0x7f)
      offset     : offbuf[k] (samples, signed)  -- the VALIDATED offset
      coeff_byte : raw sign-magnitude byte from recbase+0xAD+4k
      csign      : 1 if negative
      cmag       : 0..127 magnitude
      gain       : signed coeff / 127.0
      role       : READ / WRITE_HEAD / WRITE_NEG / INPUT / SPECIAL_NEG
      pair_id    : index of the pair this microword belongs to (coeff-matched consecutive)
      pair_role  : 'hi' (first of pair) / 'lo' (second) / 'single'
    """
    seq = slot_sequence(recbase)
    offs = A.tap_map(recbase, cce=cce, ccf=ccf, verbose=False)
    prog = []
    i = 0
    pair_id = 0
    idx = 0
    while i < len(seq):
        k, b = seq[i]
        is_pair = (i + 1 < len(seq) and seq[i + 1][1] == b)
        members = [(k, b)]
        if is_pair:
            members.append(seq[i + 1])
        for j, (kk, bb) in enumerate(members):
            off = offs[kk] if kk < len(offs) else 0
            csign = 1 if (bb & 0x80) else 0
            cmag = bb & 0x7f
            prog.append(dict(
                idx=idx, slot_k=kk, offset=off, coeff_byte=bb,
                csign=csign, cmag=cmag, gain=(-cmag if csign else cmag) / 127.0,
                role=classify_tap(off),
                pair_id=pair_id,
                pair_role=('single' if not is_pair else ('hi' if j == 0 else 'lo')),
            ))
            idx += 1
        pair_id += 1
        i += 2 if is_pair else 1
    return prog


def save_tables(prog, cce=0, outdir=None):
    outdir = outdir or os.path.dirname(os.path.abspath(__file__))
    stem = os.path.join(outdir, f"concert_program_cce{cce:02X}")
    cols = ['idx', 'slot_k', 'offset', 'coeff_byte', 'csign', 'cmag', 'gain',
            'role', 'pair_id', 'pair_role']
    with open(stem + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in prog:
            w.writerow({c: (round(p[c], 4) if isinstance(p[c], float) else p[c]) for c in cols})
    with open(stem + '.json', 'w') as f:
        json.dump(prog, f, indent=2)
    return stem + '.csv', stem + '.json'


def summarize(prog, cce=0):
    from collections import Counter
    n = len(prog)
    reads = [p for p in prog if p['role'] == 'READ']
    writes = [p for p in prog if p['role'] in ('WRITE_HEAD', 'WRITE_NEG', 'INPUT')]
    pos_delays = [p['offset'] for p in reads]
    cnt = Counter(pos_delays)
    loop = cnt.most_common(1)[0] if cnt else (0, 0)
    print(f"=== CONCERT per-microword program (cce=0x{cce:02X}) ===")
    print(f"  microwords: {n}   reads(+delay)={len(reads)}  write/input/sentinel={len(writes)}")
    print(f"  pairs: {len(set(p['pair_id'] for p in prog if p['pair_role'] != 'single'))}"
          f"  singles: {sum(1 for p in prog if p['pair_role']=='single')}")
    print(f"  recirc loop tap (most-recurring read delay): {loop[0]} samp"
          f"  ({loop[0]/FS*1000:.1f} ms) x{loop[1]}")
    print(f"  read-delay range: {min(pos_delays)}..{max(pos_delays)} samp"
          f"  ({min(pos_delays)/FS*1000:.1f}..{max(pos_delays)/FS*1000:.1f} ms)")
    print(f"  roles: {Counter(p['role'] for p in prog)}")
    print(f"  coeff |gain|: min={min(abs(p['gain']) for p in prog):.3f}"
          f"  max={max(abs(p['gain']) for p in prog):.3f}")


def live_offset_crosscheck(recbase=RECBASE, power_up_id=0x01):
    """INDEPENDENT cross-check: boot the REAL firmware, snapshot the hardware OFFTAB interleave
    (AA38 writes at 0x41FD-4k via PC 0xAA42/0xAA46), and confirm offbuf[k]==tap_map[k] 128/128 at
    the LIVE SIZE byte (0x3CCE). This proves the assigned offsets equal what the hardware loads."""
    from z80emu import Z80
    import boot_xl as Bz
    from boot_xl import LARC, ARU, ERR_H, ERR_E
    mem = Bz.load_mem(); cpu = Z80(mem); larc = LARC(); aru = ARU()
    mem[ERR_H] = 0xC9; mem[ERR_E] = 0xC9
    mem[0x8160] = 0x3E; mem[0x8161] = power_up_id & 0xFF; mem[0x8162] = 0x00
    cpu.in_hook = lambda p: (larc.status(cpu) if p == 0xEF else
                             larc.data(cpu) if p == 0xEE else aru.inp(p))
    cpu.out_hook = lambda p, v: (larc.out(cpu, p, v) if p in (0xEE, 0xEF) else aru.out(p, v))
    cpu.PC = 0
    words = {}
    orig_wb = cpu.wb
    def wb(a, v):
        if cpu.PC in (0xAA42, 0xAA46):
            words.setdefault(a & 0xFFFF, v & 0xFF)
        orig_wb(a, v)
    cpu.wb = wb
    last_irq = 0; live_size = None
    for _ in range(20_000_000):
        if cpu.PC == 0xAA9F and len(words) >= 256:
            live_size = cpu.m[0x3CCE]; break
        if cpu.IFF1 and (cpu.icount - last_irq) >= 64 and (larc.tx_en or larc.rx_ready(cpu)):
            if cpu.interrupt():
                last_irq = cpu.icount
        cpu.step()
    offs = A.tap_map(recbase, cce=live_size, verbose=False)
    match = tot = 0
    for k in range(128):
        hi = 0x41FD - 4 * k; lo = hi - 1
        if hi in words and lo in words:
            v = (words[hi] << 8) | words[lo]
            sv = v - 0x10000 if v & 0x8000 else v
            tot += 1
            if sv == offs[k]:
                match += 1
    return dict(live_size=live_size, match=match, total=tot, offs=offs)


if __name__ == '__main__':
    cce = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0
    prog = build_program(cce=cce)
    summarize(prog, cce)
    csvp, jsonp = save_tables(prog, cce)
    print(f"\n  wrote {csvp}\n  wrote {jsonp}")
    if '--crosscheck' in sys.argv:
        cc = live_offset_crosscheck()
        print(f"\n  LIVE OFFSET CROSS-CHECK: hardware OFFTAB interleave vs tap_map(cce=0x{cc['live_size']:02X}):"
              f" {cc['match']}/{cc['total']} match")
