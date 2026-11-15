"""Execute the source's 8086 instruction sequence with Keystone and Unicorn."""

from itertools import product
from pathlib import Path
import random
import re
import struct

from keystone import Ks, KS_ARCH_X86, KS_MODE_16
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_CS, UC_X86_REG_DS,
    UC_X86_REG_SS, UC_X86_REG_SP,
)


def main():
    source = Path(__file__).with_name("sort_signed_words_exe.asm").read_text(encoding="ascii")
    body = source.split("MAIN PROC", 1)[1].split("MAIN ENDP", 1)[0]
    body = "\n".join(line.split(";", 1)[0].strip() for line in body.splitlines())
    body = body.replace("@DATA", "0x2000")
    body = re.sub(r"ARR\[([^]]+)\]", r"word ptr [\1+2]", body)
    body = re.sub(r"\bN\b", "word ptr [0]", body)
    code, _ = Ks(KS_ARCH_X86, KS_MODE_16).asm(body, addr=0)
    code = bytes(code)
    sample = [7, -3, 12, 0, -8, 7]
    cases = [
        sample, [], [5], [2, 1], [1, 2], [7, 7, 7],
        [-32768, 32767], [32767, 0, -32768, -1, 32767],
        [-1, -5, -2], list(range(20)), list(range(20, 0, -1)),
    ]
    cases += [list(values) for size in range(1, 6) for values in product((-1, 0, 1), repeat=size)]
    rng = random.Random(8086)
    cases += [[rng.randint(-32768, 32767) for _ in range(rng.randrange(65))] for _ in range(50)]

    for values in cases:
        cpu = Uc(UC_ARCH_X86, UC_MODE_16)
        cpu.mem_map(0, 0x100000)
        cpu.mem_write(0x10000, code)
        cpu.reg_write(UC_X86_REG_CS, 0x1000)
        cpu.reg_write(UC_X86_REG_DS, 0x0800)  # DOS-style initial DS differs from the data segment.
        cpu.reg_write(UC_X86_REG_SS, 0x3000)
        cpu.reg_write(UC_X86_REG_SP, 0x100)
        payload = struct.pack("<H", len(values)) + struct.pack("<" + "h" * len(values), *values)
        cpu.mem_write(0x20000 - 16, b"\xA5" * 16 + payload + b"\x5A" * 16)
        exited = []

        def interrupt(current, number, _):
            assert number == 0x21 and current.reg_read(UC_X86_REG_AX) == 0x4C00
            exited.append(True)
            current.emu_stop()

        cpu.hook_add(UC_HOOK_INTR, interrupt)
        cpu.emu_start(0x10000, 0x10000 + len(code), count=50 * max(1, len(values)) ** 2 + 100)
        assert exited, ("DOS exit not reached", values)
        assert cpu.reg_read(UC_X86_REG_DS) == 0x2000
        assert cpu.reg_read(UC_X86_REG_SP) == 0x100
        expected = struct.pack("<H", len(values)) + struct.pack("<" + "h" * len(values), *sorted(values))
        actual = bytes(cpu.mem_read(0x20000 - 16, 16 + len(payload) + 16))
        assert actual == b"\xA5" * 16 + expected + b"\x5A" * 16, values

    print(f"PASS: {len(cases)} arrays; signed order, array bounds, N, DS, SP, and DOS exit.")


if __name__ == "__main__":
    main()
