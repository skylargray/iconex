#!/usr/bin/env python3
"""Export bit-exact golden artifacts for the C++ diff harness.

For each program id writes, under tools/harness/224xl/golden/:
  <id>_meta.json  - {power_up_id, n_active, nsamp, trace_window, imp}
  <id>_wcs.bin    - the raw 512-byte WCS image
  <id>_fields.json- decoded active-step fields (layer-1 parity reference)
  <id>_esum.bin   - nsamp x int64 LE per-sample energy (layer-2 parity)
  <id>_steps.bin  - trace_window x n_active x 8 int64 LE probe records (layer-2)

Usage: python tools/export_golden_224.py [id_hex ...]   (default 0x01)
"""
import sys, os, json, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B
import aru_datapath as A

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(REPO, "tools", "harness", "224xl", "golden")
RA_PICK = lambda st: (st['b5'] << 1) | st['b4']
NSAMP = 4000
TRACE_WINDOW = 64
IMP = 20000


def export(power_up_id):
    os.makedirs(GOLD, exist_ok=True)
    tag = f"{power_up_id:02x}"
    cpu, mem, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    img = bytes(mem[0x4000:0x4200])
    prog = A.load_microcode(power_up_id)
    esum, steps = A.run_trace(prog, RA_PICK, nsamp=NSAMP, imp=IMP, trace_window=TRACE_WINDOW)

    with open(os.path.join(GOLD, f"{tag}_wcs.bin"), "wb") as f:
        f.write(img)

    fields = [dict(s=p['s'], offset=p['offset'], coeff=p['coeff'],
                   ZERO=p['ZERO'], b3=p['b3'], XFER=p['XFER'], WA=p['WA'],
                   RA=(p['b5'] << 1) | p['b4']) for p in prog]
    with open(os.path.join(GOLD, f"{tag}_fields.json"), "w") as f:
        json.dump(fields, f)

    with open(os.path.join(GOLD, f"{tag}_esum.bin"), "wb") as f:
        f.write(struct.pack(f"<{len(esum)}q", *esum))

    with open(os.path.join(GOLD, f"{tag}_steps.bin"), "wb") as f:
        for rec in steps:                       # rec = 8-tuple of ints
            f.write(struct.pack("<8q", *rec))

    meta = dict(power_up_id=power_up_id, n_active=len(prog),
                nsamp=NSAMP, trace_window=TRACE_WINDOW, imp=IMP)
    with open(os.path.join(GOLD, f"{tag}_meta.json"), "w") as f:
        json.dump(meta, f)
    print(f"exported golden for 0x{tag}: {len(prog)} active steps, {NSAMP} samples")


if __name__ == '__main__':
    ids = [int(a, 16) for a in sys.argv[1:]] or [0x01]
    for i in ids:
        export(i)
