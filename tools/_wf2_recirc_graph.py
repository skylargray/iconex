#!/usr/bin/env python3
"""WF2: full recirculation graph + stereo-mirror-vs-serial-stage test.

For the whole 110-step CONCERT program, instrument every DMEM write (addr->n,step)
and every DMEM read (addr-> matching last writer + delay). Build the directed graph
write_step -> read_step with the modal (min) delay and occurrence count.

Then specifically classify the band-split halves H1=s37..46 and H2=s89..98:
  - which steps each half READS from (writer steps), and writes TO (reader steps)
  - whether H1 and H2 share DMEM addresses (=> serial/coupled) or are disjoint (=> stereo)
  - whether there is a cross-half edge H1->H2 or H2->H1 (=> serial), or only intra-half (=> stereo)
Also: track register-file (R0..R3) producer->consumer to see if the two halves share
the accumulator/register state serially within one sample.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
DMASK = A.DMASK

H1 = set(range(37, 47))   # 37..46
H2 = set(range(89, 99))   # 89..98


def half(s):
    if s in H1: return 'H1'
    if s in H2: return 'H2'
    return '--'


def main():
    prog = A.load_microcode(0x01)
    pick = lambda st: (st['b5'] << 1) | st['b4']
    bystep = {p['s']: p for p in prog}

    R = [0, 0, 0, 0]; ACC = 0; RES = 0
    DM = [0]*(DMASK+1); pos = 0
    last_write = {}            # addr -> (n, step)
    edges = {}                 # (wstep, rstep) -> {'delays':[], 'addrs':set()}
    addr_writers = {}          # addr -> set(step)  (who ever writes this addr)
    addr_readers = {}          # addr -> set(step)  (who ever reads this addr)
    N = 3000
    for n in range(N):
        pos = (pos+1) & DMASK
        for st in prog:
            s = st['s']
            addr = (pos - st['offset']) & DMASK
            if st['b3']:
                dab = RES
            else:
                dab = DM[addr]
                if n > 200:
                    addr_readers.setdefault(addr, set()).add(s)
                    if addr in last_write:
                        wn, wstep = last_write[addr]
                        e = edges.setdefault((wstep, s), {'delays': [], 'n': 0})
                        e['delays'].append(n-wn); e['n'] += 1
            if n == 0 and st is prog[0]: dab += 20000
            mag = abs(st['coeff']); Cs = -(mag>>1) if st['coeff']<0 else (mag>>1)
            x = R[pick(st)]; R[st['WA']] = dab
            if st['ZERO']: ACC = 0
            ACC = A.sat20(ACC + (((x<<3)*Cs) >> 6))
            if st['XFER']: RES = A.sat16(ACC >> 3)
            if st['b3']:
                DM[addr] = RES
                last_write[addr] = (n, s)
                if n > 200:
                    addr_writers.setdefault(addr, set()).add(s)

    # ---- Classify edges by half ----
    print("=== ALL recirculation edges touching the band-split halves H1=37-46, H2=89-98 ===")
    print("(writer -> reader : modal_delay  count)")
    rel = []
    for (ws, rs), e in edges.items():
        if half(ws) != '--' or half(rs) != '--':
            md = min(e['delays'])
            rel.append((half(ws), ws, half(rs), rs, md, e['n']))
    rel.sort(key=lambda t: (t[1], t[3]))
    for hw, ws, hr, rs, md, cnt in rel:
        tag = ''
        if hw != '--' and hr != '--':
            tag = '  <== CROSS-HALF' if hw != hr else '  (intra-half)'
        print(f"  {hw} s{ws:<3} -> {hr} s{rs:<3}  delay={md:<4} cnt={cnt}{tag}")

    # ---- Cross-half edge summary ----
    print("\n=== CROSS-HALF edge summary (H1<->H2 ONLY) ===")
    h1_to_h2 = [t for t in rel if t[0] == 'H1' and t[2] == 'H2']
    h2_to_h1 = [t for t in rel if t[0] == 'H2' and t[2] == 'H1']
    print(f"  H1 -> H2 edges: {[(f's{t[1]}', f's{t[3]}', f'd{t[4]}') for t in h1_to_h2]}")
    print(f"  H2 -> H1 edges: {[(f's{t[1]}', f's{t[3]}', f'd{t[4]}') for t in h2_to_h1]}")

    # ---- Shared DMEM addresses between halves ----
    print("\n=== Shared DMEM addresses between H1 and H2 (any read OR write) ===")
    def touched(steps):
        addrs = set()
        for a, ws in addr_writers.items():
            if ws & steps: addrs.add(a)
        for a, rs in addr_readers.items():
            if rs & steps: addrs.add(a)
        return addrs
    a1 = touched(H1); a2 = touched(H2)
    shared = a1 & a2
    print(f"  H1 touches {len(a1)} addrs, H2 touches {len(a2)} addrs, SHARED={len(shared)}")
    if shared:
        for a in sorted(shared):
            print(f"    addr 0x{a:04X}: writers={sorted(addr_writers.get(a,set()))} readers={sorted(addr_readers.get(a,set()))}")

    # ---- Within-half: does each half close its own loop? ----
    print("\n=== Intra-half closure: writers and readers per half ===")
    for nm, hs in [('H1', H1), ('H2', H2)]:
        w = sorted({s for a in (addr_writers) for s in addr_writers[a] if s in hs})
        r = sorted({s for a in (addr_readers) for s in addr_readers[a] if s in hs})
        print(f"  {nm}: write-back steps (b3=1)={w}  read steps={r}")


if __name__ == '__main__':
    main()
