#!/usr/bin/env python3
"""Find the routing/gain that makes ZERO DELAY = unity passthrough.

We brute-force the missing routing detail: which register the FPC OUTPUT step reads,
and how the captured output value relates to it (raw pass-through vs single multiply by
the step's coeff vs the accumulated MAC). The diagnostic ground truth (output==input,
unity) selects the physically-correct combination, and the resulting gain is the model's
true passthrough gain -> the CONCERT scaling check.

Input lands in R[2] (step 75 WA=2). Output step 76 WA=3, coeff +124 (C=+0.96875).
We test, for the output step, value = f(R[src]) over src in {0,1,2,3} and these forms:
  raw      : R[src]
  mul      : sat16( ((R[src]<<3)*Cout)>>6 >>3 )         (one multiply by output coeff)
  mul_in   : R[src] passed through input-coeff then output-coeff (chain)
We also test whether an implicit per-sample accumulator-clear + 'output = sat16(ACC>>3)'
where ACC accumulated R[2]*Cin gives unity.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aru_datapath as A
import importlib.util
spec = importlib.util.spec_from_file_location("_hd", os.path.join(os.path.dirname(__file__), "_hunt_diagunity.py"))
_hd = importlib.util.module_from_spec(spec); spec.loader.exec_module(_hd)

DMASK = A.DMASK


def csint(coeff):
    mag = abs(coeff)
    return -(mag >> 1) if coeff < 0 else (mag >> 1)


def run_route(prog, nsamp, imp, out_src, form, mode='int'):
    """out_src: register index the FPC output step reads. form: 'raw'|'mul'|'mul2'."""
    if mode == 'int':
        R = [0,0,0,0]; ACC = 0; RES = 0; DM = [0]*(DMASK+1)
    else:
        R = [0.0]*4; ACC = 0.0; RES = 0.0; DM = [0.0]*(DMASK+1)
    pos = 0
    in_step = A.fpc_input_step(prog)
    out_steps = [st['s'] for st in prog if st['WA'] == 3 and (st['offset'] & 0x8000)]
    out_log = {s: [] for s in out_steps}
    # find the input step's coeff for the matching channel (simplify: use step's own coeff)
    for n in range(nsamp):
        pos = (pos + 1) & DMASK
        if mode == 'int': ACC = 0
        else: ACC = 0.0
        for st in prog:
            addr = (pos - st['offset']) & DMASK
            is_out = (st['offset'] & 0x8000) and st['WA'] == 3
            is_in = in_step is not None and st['s'] == in_step
            if is_in:
                dab = imp if n == 0 else 0
            elif is_out:
                dab = 0
            else:
                dab = RES if st['b3'] else DM[addr]
            Cs = csint(st['coeff'])
            x = R[out_src] if is_out else 0  # only output step's read matters here
            R[st['WA']] = dab
            if st['b3']:
                DM[addr] = RES
            if is_out:
                xv = R[out_src]  # read AFTER writes in this sample's earlier steps already happened
                if form == 'raw':
                    outv = xv
                elif form == 'mul':
                    if mode == 'int':
                        outv = A.sat16((((xv << 3) * Cs) >> 6) >> 3)
                    else:
                        outv = (xv*8.0*Cs/64.0)/8.0
                elif form == 'mul_full':
                    # x * (Cs/64) full-scale (no >>3 attenuation) = x*C
                    if mode == 'int':
                        outv = A.sat16((xv * Cs) >> 6)
                    else:
                        outv = xv*Cs/64.0
                else:
                    outv = None
                out_log[st['s']].append(outv)
    return out_log


def report(prog, nsamp, imp, label):
    print(f"\n##### {label}: brute-force output routing #####")
    for out_src in range(4):
        for form in ('raw', 'mul', 'mul_full'):
            ol = run_route(prog, nsamp, imp, out_src, form)
            for s, seq in ol.items():
                nz = [(i, v) for i, v in enumerate(seq) if abs(v) > 1e-9]
                if not nz:
                    continue
                i0, v0 = nz[0]
                pk_i, pk_v = max(nz, key=lambda t: abs(t[1]))
                flag = '  <== UNITY!' if abs(abs(v0/imp) - 1.0) < 0.05 else ''
                print(f"  out_src=R[{out_src}] form={form:8s} step{s}: "
                      f"first nz @n={i0} v={v0!r} gain={v0/imp:+.6f} | peak@n={pk_i} v={pk_v!r}{flag}")


if __name__ == '__main__':
    img0 = _hd.build_image(zero_delay=True)
    prog0 = _hd.decode(img0)
    report(prog0, 300, 20000, "ZERO DELAY")
