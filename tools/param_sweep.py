#!/usr/bin/env python3
"""224XL parameter sweep: recover each program parameter's effect on the WCS.

Boots the real firmware (tools/boot_xl), reaches the main loop, then for each of the
program's parameters injects a range of LARC slider values, lets the firmware apply them
(de-zipper / group-table path 0x85f2 -> 0xADxx), and records which WCS microword steps
change and to what coefficient / delay value -- the parameter -> coefficient transfer table.

Two subtleties handled:
  - the WCS has 4 INTRINSICALLY-MODULATED tank taps (the Concert Hall modulated tank); those
    never settle, so we detect them (variance with no injection) and report them separately.
  - the param->coeff apply ramps via the de-zipper, so we run a settle budget per point and
    read the settled value of the (non-modulated) static steps.

Usage:  python tools/param_sweep.py [power_up_id_hex] [n_params]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot_xl as B

REGS = ['A','F','B','C','D','E','H','L','A_','F_','B_','C_','D_','E_','H_','L_',
        'IX','IY','SP','PC','I','R','IFF1','IFF2','IM','halted','icount']
GRID = [0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0, 0xFF]   # slider values (0x20 ~ default)
SETTLE = 1_000_000


def coeff(mem, s):
    l3 = mem[0x4000 + s*4 + 3]
    return None if (mem[0x4000+s*4+2] == 0xFF and l3 == 0xFF) else (-1 if l3 & 0x80 else 1)*(l3 & 0x7F)


def delay(mem, s):
    return (~(mem[0x4000+s*4] | (mem[0x4000+s*4+1] << 8))) & 0xFFFF


def sweep(power_up_id=0x01, n_params=6):
    cpu, mem, larc, aru, ms, *_ = B.boot(power_up_id=power_up_id, verbose=False)
    li = [cpu.icount]

    def runN(n):
        for _ in range(n):
            if cpu.IFF1 and (cpu.icount - li[0]) >= 64 and (larc.tx_en or larc.rx_ready(cpu)):
                if cpu.interrupt():
                    li[0] = cpu.icount
            cpu.step()

    def snap():
        return (bytes(mem), {r: getattr(cpu, r) for r in REGS},
                (list(larc.rx_q), larc.rx_at, larc.tx_en, larc.rx_int))

    def restore(s):
        mem[:] = s[0]
        for r, v in s[1].items():
            setattr(cpu, r, v)
        larc.rx_q[:], larc.rx_at, larc.tx_en, larc.rx_int = s[2][0], s[2][1], s[2][2], s[2][3]

    # 1) find intrinsically-modulated steps (vary with NO injection)
    S0 = snap()
    base_c = {s: coeff(mem, s) for s in range(128)}
    series = []
    for _ in range(8):
        runN(120_000)
        series.append([coeff(mem, s) for s in range(128)])
    modulated = sorted(s for s in range(128)
                       if base_c[s] is not None and (max(x[s] for x in series) - min(x[s] for x in series)) > 2)
    restore(S0)
    runN(300_000)                                   # settle the static steps
    baseline_c = {s: coeff(mem, s) for s in range(128) if base_c[s] is not None}
    baseline_d = {s: delay(mem, s) for s in range(128) if base_c[s] is not None}
    S1 = snap()

    result = dict(power_up_id=power_up_id, modulated_steps=modulated, params=[])
    for p in range(n_params):
        cgrid = {}   # slider value -> {step: coeff}
        dgrid = {}
        for v in GRID:
            restore(S1)
            mem[0x3c00 + p] = v
            mem[0x3c16 + p] = (v ^ 0xFF) & 0xFF      # force change-detection
            mem[0x3c14] |= 0x80                       # serial-idle flag
            runN(SETTLE)
            cgrid[v] = {s: coeff(mem, s) for s in baseline_c if s not in modulated}
            dgrid[v] = {s: delay(mem, s) for s in baseline_c if s not in modulated}
        cch = sorted(s for s in baseline_c if s not in modulated
                     and any(cgrid[v][s] != baseline_c[s] for v in GRID))
        dch = sorted(s for s in baseline_c if s not in modulated
                     and any(dgrid[v][s] != baseline_d[s] for v in GRID))
        result['params'].append(dict(
            param=p,
            coeff_steps=cch,
            delay_steps=dch,
            coeff_table={s: [cgrid[v][s] for v in GRID] for s in cch},
            delay_table={s: [dgrid[v][s] for v in GRID] for s in dch},
        ))
    return result


def main():
    pid = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x01
    npar = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    r = sweep(pid, npar)
    print(f"# power_up_id=0x{pid:02x}  slider grid = {[hex(v) for v in GRID]}")
    print(f"# intrinsically-modulated tank taps (LFO targets): {r['modulated_steps']}")
    for pr in r['params']:
        print(f"\nparam{pr['param']}: {len(pr['coeff_steps'])} coeff steps, {len(pr['delay_steps'])} delay steps")
        for s in pr['coeff_steps'][:12]:
            print(f"   coeff step{s:3d}: " + " ".join(f"{x:5d}" for x in pr['coeff_table'][s]))
        for s in pr['delay_steps'][:6]:
            print(f"   DELAY step{s:3d}: " + " ".join(f"{x:5d}" for x in pr['delay_table'][s]))
    out = os.path.join(os.path.dirname(__file__), '..', 'docs', 'reference', '224',
                       f'224XL_param_sweep_{pid:02x}.json')
    with open(out, 'w') as f:
        json.dump(r, f, indent=1)
    print(f"\nwrote {os.path.abspath(out)}")


if __name__ == '__main__':
    main()
