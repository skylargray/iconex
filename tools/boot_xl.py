#!/usr/bin/env python3
"""224XL v8.2.1 operational boot harness.

reset(0x0000 -> 0x003B) -> LARC 8251 handshake -> power-up self-test (POST).

Models the LARC serial link (8251 @ 0xEE data / 0xEF status) well enough to pass the
power-up handshake, and lets the ARU/DSP I/O ports be configured (default: stub 0xFF).
Instruments:
  - every distinct low-port (<0x10) IN read site (PC, port) and the value returned,
  - every OUT to the ARU/DSP ports,
  - register snapshot + caller at every DIAG-error-handler entry
      0x0217 ('H'-type) and 0x021D ('E'-type),
  - the error message the handler builds in the 0x3F4F display buffer (ASCII),
  - serial TX bytes (OUT 0xEE), masked to 7 bits = the LARC display ASCII.

Goal: see exactly which self-test fails and what it expected vs read, so the DSP
port model can be made faithful enough to pass POST and reach program load.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from collections import Counter
from z80emu import Z80

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "ROMs", "Lexicon 224", "224XL v8_21")

ERR_H = 0x0217   # 'H'-type DIAG error handler entry
ERR_E = 0x021D   # 'E'-type DIAG error handler entry


def load_mem():
    mem = bytearray(0x10000)
    for n, base in [(1, 0), (2, 0x800), (3, 0x1000)]:
        b = np.fromfile(f"{DIR}/SBC{n} 2716.BIN", dtype=np.uint8)
        mem[base:base + len(b)] = b.tobytes()
    for n in range(1, 9):
        b = np.fromfile(f"{DIR}/NVS{n} 2732.BIN", dtype=np.uint8)
        base = 0x8000 + (n - 1) * 0x1000
        mem[base:base + len(b)] = b.tobytes()
    return mem


class LARC:
    """8251 USART + LARC model.

    Port 0xEF (status): bit0=TxRDY, bit1=RxRDY, bits3-5 (0x38)=error (kept 0).
    Port 0xEE (data): TX byte (captured) on OUT; RX byte on IN.

    The handshake (reset 0x003B-0x0089) is POLLED with IFF1=0, so we serve the
    0xC8 reply via the status/data ports directly. After 0x0089 the firmware EIs
    and serial becomes interrupt-driven (8251 TxRDY/RxRDY -> RST38 ISR @0x03EE);
    we fire interrupts (see boot()) gated on tx_en / rx_pending.
    """
    def __init__(self):
        self.rx_q = []          # pending RX bytes (FIFO)
        self.rx_at = 0          # icount when head becomes readable
        self.tx = []            # captured TX bytes
        self.tx_en = False      # 8251 TxEN (command bit0) -> gates TxRDY interrupts
        self.rx_int = False     # RxEN (command bit2)

    # ---- queue an RX byte to be delivered to the SBC ----
    def queue_rx(self, cpu, b, delay=40):
        self.rx_q.append(b)
        if len(self.rx_q) == 1:
            self.rx_at = cpu.icount + delay

    def rx_ready(self, cpu):
        return bool(self.rx_q) and cpu.icount >= self.rx_at

    def out(self, cpu, port, v):
        if port == 0xEE:
            self.tx.append(v)
            if v == 0xE0 and not self.rx_q:          # power-up handshake request
                self.queue_rx(cpu, 0xC8, delay=40)
        elif port == 0xEF:                            # 8251 command/mode register
            # mode word 0xCE (after reset) -> ignore; command words carry TxEN(bit0)/RxEN(bit2)
            if v not in (0xCE,):
                self.tx_en = bool(v & 0x01)
                self.rx_int = bool(v & 0x04)

    def status(self, cpu):
        s = 0x01                                      # TxRDY: transmitter holding reg empty
        if self.rx_ready(cpu):
            s |= 0x02                                 # RxRDY
        return s

    def data(self, cpu):
        if self.rx_ready(cpu):
            b = self.rx_q.pop(0)
            if self.rx_q:
                self.rx_at = cpu.icount + 12          # next byte shortly after
            return b
        return 0xFF


class ARU:
    """Minimal ARU/DSP port model.

    Data path is active-low (roadmap: every store preceded by CPL): the 16-bit
    data latch reads back complemented. 0x06=low byte, 0x07=high byte. 0x03 bit0 =
    busy/ready handshake (return ready). Other ports return benign defaults; the
    POST signature test mixes inverted/non-inverted hardware taps that genuinely
    need the real ARU, so POST errors are suppressed (see boot suppress_post).
    """
    def __init__(self):
        self.lo = 0
        self.hi = 0

    def out(self, port, v):
        if port == 0x06:
            self.lo = v & 0xFF
        elif port == 0x07:
            self.hi = v & 0xFF

    def inp(self, port):
        if port == 0x06:
            return (~self.lo) & 0xFF                   # active-low readback
        if port == 0x07:
            return (~self.hi) & 0xFF
        if port == 0x03:
            return 0x00                                # bit0=0 => not busy / ready
        if port in (0x08, 0x09):
            return 0x00                                # no panel keys / no overload
        return 0x00


def regs(cpu):
    return dict(A=cpu.A, B=cpu.B, C=cpu.C, D=cpu.D, E=cpu.E, H=cpu.H, L=cpu.L,
                HL=cpu.HL, DE=cpu.DE, BC=cpu.BC)


def ascii7(b):
    return "".join(chr(x & 0x7F) if 0x20 <= (x & 0x7F) < 0x7F else "." for x in b)


def boot(max_ins=20_000_000, irq_period=64, suppress_post=True,
         stop_pc=0x8169, stop_hits=3, watch=None, power_up_id=None,
         cap_offsets=False, verbose=True):
    """Boot v8.2.1 reset->handshake->POST->normal-op.

    irq_period   : fire a maskable interrupt every N ins when IFF1 & (tx_en|rx_pending).
    suppress_post: patch DIAG error handlers 0x0217/0x021D to RET (model 'self-tests pass').
    stop_pc/hits : stop after reaching stop_pc this many times (default main loop 0x8169).
    watch        : optional set of PCs to log first-hit icount for.
    power_up_id  : if set, patch 0x8160 'LD A,(0xB800)' -> 'LD A,id; NOP' so the firmware
                   loads program <id> at power-up (id = a record first-byte selector).
    """
    mem = load_mem()
    cpu = Z80(mem)
    larc = LARC()
    aru = ARU()
    if suppress_post:
        mem[ERR_H] = 0xC9       # RET  (suppress 'H' DIAG error -> non-blocking)
        mem[ERR_E] = 0xC9       # RET  (suppress 'E' DIAG error)
    if power_up_id is not None:
        # 0x8160: 3A 00 B8 (LD A,(0xB800)) -> 3E <id> 00 (LD A,id ; NOP)
        mem[0x8160] = 0x3E
        mem[0x8161] = power_up_id & 0xFF
        mem[0x8162] = 0x00

    out_log = Counter()
    out_first = {}
    in_sites = {}
    errors = []
    milestones = {}
    watch = set(watch or [])

    def inh(p):
        pc = (cpu.PC - 2) & 0xFFFF
        if p == 0xEF:
            return larc.status(cpu)
        if p == 0xEE:
            return larc.data(cpu)
        v = aru.inp(p)
        in_sites.setdefault((pc, p), v)
        return v

    def outh(p, v):
        if p in (0xEE, 0xEF):
            larc.out(cpu, p, v)
            return
        aru.out(p, v)
        out_log[p] += 1
        out_first.setdefault(p, ((cpu.PC - 2) & 0xFFFF, v))

    cpu.in_hook = inh
    cpu.out_hook = outh
    cpu.PC = 0x0000

    last_irq = 0
    stop_count = 0
    cap = []                 # captured B55B offset writes (delay = -offset) in load window
    prev_cf1 = 0x3F4D
    in_load = False

    for i in range(max_ins):
        pc = cpu.PC
        if pc in watch and pc not in milestones:
            milestones[pc] = cpu.icount
        # capture B55B offset-buffer writes (0x3cf1 ptr decrements) during program load
        if cap_offsets:
            if pc == 0x13B6:
                in_load = True
            elif pc == 0x8169:
                in_load = False
            if in_load:
                cur = cpu.rw(0x3CF1)
                if 0x3000 <= cur < prev_cf1:
                    a = cur
                    while a < prev_cf1:
                        v = cpu.m[a] | (cpu.m[a + 1] << 8)
                        sv = v - 0x10000 if v & 0x8000 else v
                        cap.append(-sv)
                        a += 2
                prev_cf1 = cur
        if pc in (ERR_H, ERR_E) and not suppress_post:
            errors.append(dict(handler='E' if pc == ERR_E else 'H',
                               caller=cpu.rw(cpu.SP), icount=cpu.icount, **regs(cpu)))
        for key, mpc in (('handshake', 0x0089), ('normal_op', 0x813B),
                         ('mainloop', 0x8169), ('prog_load', 0x13B6), ('display', 0x82CF)):
            if pc == mpc:
                milestones.setdefault(key, cpu.icount)
        if pc == stop_pc:
            stop_count += 1
            if stop_count >= stop_hits:
                break
        # interrupt-driven serial after EI
        if irq_period and cpu.IFF1 and (cpu.icount - last_irq) >= irq_period \
                and (larc.tx_en or larc.rx_ready(cpu)):
            if cpu.interrupt():
                last_irq = cpu.icount
        try:
            cpu.step()
        except Exception as e:
            print(f"  ABORT @0x{cpu.PC:04X} after {i} ins (icount {cpu.icount}): {e}")
            break
    else:
        print(f"  ran full {max_ins} ins, PC=0x{cpu.PC:04X}")

    if verbose:
        print("\nmilestones (icount):")
        for k in ('handshake', 'normal_op', 'prog_load', 'display', 'mainloop'):
            print(f"    {k:12}: {milestones.get(k)}")
        for w in sorted(watch):
            print(f"    PC 0x{w:04X}: {milestones.get(w)}")
        tx = bytes(larc.tx)
        print(f"\nserial TX ({len(tx)} bytes), ASCII (7-bit): {ascii7(tx)!r}")
        print(f"\nARU/DSP OUT ports: {[(hex(p),c) for p,c in out_log.most_common()]}")
        if errors:
            print(f"\nDIAG errors: {len(errors)}")
            for e in errors[:8]:
                tc = (e['A'] + e['D']) & 0xFF
                print(f"    [{e['handler']}{tc:02X}] caller=0x{e['caller']:04X} "
                      f"C={e['C']:02X} B={e['B']:02X} ADDR={e['HL']:04X}")
        print(f"\n0x3F4F display buffer: {ascii7(mem[0x3F4F:0x3F80])!r}")
        # the DL-1414 display image the firmware maintains for the LARC
        print(f"0x3F8E area:           {ascii7(mem[0x3F8E:0x3FA0])!r}")
    return cpu, mem, larc, aru, milestones, cap


if __name__ == "__main__":
    print("### 224XL v8.2.1 full boot: ISR serial + ARU latch + POST-pass model ###")
    boot(watch={0x813B, 0x8169, 0x82CF, 0x13B6})
