#!/usr/bin/env python3
"""Decisive experiment (from concert-loop-closure workflow): the all-pass cascades' paired
offsets are DMEM read+write-back of per-line delays, NOT 'idle' steps. The low 12 bits of the
offset = delay within a line (13-120 ms, sensible); the high nibble = region/line select.

Test: reclassify offsets that appear exactly 2x among currently-non-DMEM steps as a DMEM
read (first occurrence) + DMEM write-back (second), and measure whether the tank sustains a
clean decaying envelope. Sweep read/write order and addressing mode (flat 16-bit vs
region-segmented {hi4:lo12})."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
from collections import defaultdict, Counter

prog = A.load_microcode(0x01)
SR = 34130.0

def sat20(x): return 262143 if x > 262143 else (-262144 if x < -262144 else x)
def sat16(x): return 32767 if x > 32767 else (-32768 if x < -32768 else x)

def base_kind(p):
    if p['MI17'] == 1 and p['MI16'] == 1: return 'DREAD'
    if p['MI17'] == 1: return 'DWRITE'
    if p['MI16'] == 1 and p['MI4'] == 1:
        return {1: 'RDRREG', 2: 'RDXREG', 3: 'RDAD', 0: 'sub0'}[p['sub']]
    return 'idle'

# find offsets appearing exactly 2x among non-DMEM steps -> tag first=read, second=write
nondmem = defaultdict(list)
for p in prog:
    if base_kind(p) not in ('DREAD', 'DWRITE'):
        nondmem[p['offset']].append(p['s'])
pair_role = {}   # s -> 'apread'/'apwrite'
for off, ss in nondmem.items():
    if len(ss) == 2:
        a, b = sorted(ss)
        pair_role[a] = 'apread'
        pair_role[b] = 'apwrite'

def addr_of(off, pos, mode):
    if mode == 'flat':
        return (pos - off) & 0xFFFF
    # region: hi4 selects a 4K line; delay = low12 within that line's 4K circular buffer
    return (off & 0xF000) | ((pos - (off & 0x0FFF)) & 0x0FFF)

def run(order, mode, nsamp=90000, imp=1000):
    R = [0, 0, 0, 0]; ACC = 0; RES = 0; pend = 0
    DM = [0] * 0x10000; pos = 0; last = 0; out = []
    for n in range(nsamp):
        pos = (pos + 1) & 0xFFFF
        ain = imp if n == 0 else 0
        esum = 0
        for st in prog:
            s = st['s']; off = st['offset']; addr = addr_of(off, pos, mode)
            role = pair_role.get(s)
            isw = False
            k = base_kind(st)
            if k == 'DREAD':
                dab = DM[addr]
            elif k == 'DWRITE':
                dab = RES; isw = True
            elif role == ('apread' if order == 'rw' else 'apwrite'):
                dab = DM[addr]                       # all-pass delay read
            elif role == ('apwrite' if order == 'rw' else 'apread'):
                dab = RES; isw = True                # all-pass write-back
            elif k == 'RDAD':
                dab = ain
            elif k == 'RDRREG':
                dab = RES
            else:
                dab = last                           # idle/hold (RDXREG, sub0, ungated)
            last = dab
            racc = R[st['RA']]; R[st['WA']] = dab
            ACC = sat20(ACC + pend)
            if st['XFER']:
                RES = sat16(ACC >> 3); esum += abs(RES)
            if st['ZERO']:
                ACC = 0
            pend = (racc << 3) * st['cs'] >> 5
            if isw:
                DM[addr] = RES
        out.append(esum)
    return out

def envelope(out):
    pk = max(out) or 1
    nz = sum(1 for x in out if x)
    last_nz = max((i for i, x in enumerate(out) if x), default=-1)
    # windowed mean energy to see decay shape
    w = [round(sum(out[i:i+500]) / 500) for i in range(0, 90000, 10000)]
    # crude RT60: sample where windowed energy first falls below peak_window/1000
    return pk, nz, last_nz, w

print('paired all-pass steps found:', len(pair_role), '(', sum(1 for v in pair_role.values() if v=='apread'), 'read /', sum(1 for v in pair_role.values() if v=='apwrite'), 'write )')
print()
print('%-22s peak     nz/90k  last_nz  windowed-energy@[0,10k,20k,30k,40k,50k,60k,70k,80k]'%'config')
for order in ('rw', 'wr'):
    for mode in ('flat', 'region'):
        out = run(order, mode)
        pk, nz, last_nz, w = envelope(out)
        print('%-22s %-8d %-7d %-8d %s' % ('%s/%s' % (order, mode), pk, nz, last_nz, w))
