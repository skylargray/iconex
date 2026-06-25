#!/usr/bin/env python3
"""Symbolic single-sample flow graph for the CORRECTED decode (frontier device decode +
/32 multiply scale + exact MAC pipeline). Carries the audio INPUT as an atom so we can see
(a) each DMEM cell's self-feedback gain (loop gain) and (b) whether the audio couples into
the tank at all. Validated against a literal float one-sample run."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
random.seed(123)


def scale(v, k):
    return {} if k == 0.0 else {a: c*k for a, c in v.items()}


def add(v, w):
    r = dict(v)
    for a, c in w.items():
        r[a] = r.get(a, 0.0) + c
        if r[a] == 0.0:
            del r[a]
    return r


def sym_sweep(prog, read_bit=1):
    R = [{('R', i): 1.0} for i in range(4)]
    ACC = {('ACC',): 1.0}
    RES = {('RES',): 1.0}
    pend = {('pend',): 1.0}
    DM = {}
    IN = {('IN',): 1.0}

    def dm_read(off):
        if off not in DM:
            DM[off] = {('M', off): 1.0}
        return DM[off]
    for st in prog:
        off = st['offset']
        is_read = st['MI17'] == 1 and st['MI16'] == read_bit
        is_write = st['MI17'] == 1 and not is_read
        is_sub = st['MI17'] == 0 and st['MI16'] == 1
        if is_sub and st['sub'] == 3:
            dab = dict(IN)
        elif is_read:
            dab = dm_read(off)
        elif is_sub and st['sub'] == 1:
            dab = dict(RES)
        elif is_write:
            dab = dict(RES)
        else:
            dab = {}
        x = dict(R[st['RA']])
        R[st['WA']] = dict(dab)
        ACC = add(ACC, pend)                 # previous step's product now available
        if st['XFER']:
            RES = scale(ACC, 1.0/8.0)        # RES = ACC>>3
        if st['ZERO']:
            ACC = {}
        pend = scale(x, st['cs']/4.0)        # /32 net: prod=(x<<3)*cs>>5 = x*cs/4
        if is_write:
            DM[off] = dict(RES)
    return dict(dm_new=DM, R_new=R, ACC_new=ACC, RES_new=RES, pend_new=pend)


def validate(prog, read_bit=1, trials=3):
    res = sym_sweep(prog, read_bit)
    atoms = set()
    for v in list(res['dm_new'].values()) + res['R_new'] + [res['ACC_new'], res['RES_new'], res['pend_new']]:
        atoms |= set(v.keys())
    maxerr = 0.0
    for _ in range(trials):
        cR = [random.uniform(-1, 1) for _ in range(4)]
        cACC = random.uniform(-1, 1); cRES = random.uniform(-1, 1)
        cpend = random.uniform(-1, 1); cIN = random.uniform(-1, 1)
        cM = {a[1]: random.uniform(-1, 1) for a in atoms if a[0] == 'M'}

        def ev(v):
            s = 0.0
            for a, c in v.items():
                if a[0] == 'R': s += c*cR[a[1]]
                elif a[0] == 'ACC': s += c*cACC
                elif a[0] == 'RES': s += c*cRES
                elif a[0] == 'pend': s += c*cpend
                elif a[0] == 'IN': s += c*cIN
                elif a[0] == 'M': s += c*cM.get(a[1], 0.0)
            return s
        R = list(cR); ACC = cACC; RES = cRES; pend = cpend; DM = dict(cM)
        for st in prog:
            off = st['offset']
            is_read = st['MI17'] == 1 and st['MI16'] == read_bit
            is_write = st['MI17'] == 1 and not is_read
            is_sub = st['MI17'] == 0 and st['MI16'] == 1
            if is_sub and st['sub'] == 3: dab = cIN
            elif is_read: dab = DM.get(off, 0.0)
            elif is_sub and st['sub'] == 1: dab = RES
            elif is_write: dab = RES
            else: dab = 0.0
            x = R[st['RA']]; R[st['WA']] = dab
            ACC = ACC + pend
            if st['XFER']: RES = ACC/8.0
            if st['ZERO']: ACC = 0.0
            pend = x*st['cs']/4.0
            if is_write: DM[off] = RES
        err = abs(ev(res['RES_new'])-RES)
        for O, v in res['dm_new'].items():
            err = max(err, abs(ev(v)-DM[O]))
        maxerr = max(maxerr, err)
    return maxerr


def main():
    pid = int(os.environ.get('PID', '0x01'), 16)
    prog = A.load_microcode(pid)
    err = validate(prog)
    res = sym_sweep(prog)
    print(f"pid={pid:#x}: symbolic-map validation err={err:.2e} ({'OK' if err < 1e-9 else 'FAIL'})")
    dm = res['dm_new']
    print(f"DMEM cells written this sample: {len(dm)}")
    # self-feedback gain per cell + input coupling
    self_gains = []
    in_coupled = 0
    for O, v in dm.items():
        self_g = v.get(('M', O), 0.0)
        self_gains.append((O, self_g, v.get(('IN',), 0.0)))
        if abs(v.get(('IN',), 0.0)) > 1e-9:
            in_coupled += 1
    self_gains.sort(key=lambda t: -abs(t[1]))
    print(f"cells with direct INPUT coupling: {in_coupled}/{len(dm)}")
    print(f"max |self-feedback gain| = {max(abs(g) for _, g, _ in self_gains):.4f}")
    print("\ntop cells by |self-feedback gain| (O, self_g, input_g):")
    for O, g, ig in self_gains[:14]:
        print(f"  M[{O:#06x}]  self={g:+.4f}  input={ig:+.4f}")
    # does ANY cell's new value depend (directly) on the input?  And the spectral radius proxy:
    # build the cell->cell matrix (only among written cells) and estimate max eigenvalue via power iter
    cells = list(dm.keys()); idx = {O: i for i, O in enumerate(cells)}; n = len(cells)
    import math
    M = [[0.0]*n for _ in range(n)]
    inj = [0.0]*n
    for O, v in dm.items():
        i = idx[O]
        for a, c in v.items():
            if a[0] == 'M' and a[1] in idx:
                M[i][idx[a[1]]] += c
            elif a[0] == 'IN':
                inj[i] += c
    # power iteration for spectral radius
    x = [random.uniform(-1, 1) for _ in range(n)]
    lam = 0.0
    for _ in range(2000):
        y = [sum(M[i][j]*x[j] for j in range(n)) for i in range(n)]
        nrm = math.sqrt(sum(t*t for t in y)) or 1e-30
        lam = nrm; x = [t/nrm for t in y]
    print(f"\ncell-graph spectral radius (loop gain) ~ {lam:.5f}  (>=1 sustains; <1 decays)")
    print(f"input injection vector nonzero entries: {sum(1 for t in inj if abs(t)>1e-9)}/{n}")


if __name__ == '__main__':
    main()
