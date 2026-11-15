"""Execute the solution's 8086 instruction sequence with Keystone and Unicorn."""

from pathlib import Path
import re
import struct

from keystone import Ks, KS_ARCH_X86, KS_MODE_16
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_CS, UC_X86_REG_DS,
    UC_X86_REG_SS, UC_X86_REG_SP,
)


def main():
    source = Path(__file__).with_name("reverse_string_exe.asm").read_text(encoding="ascii")
    body = source.split("MAIN PROC", 1)[1].split("MAIN ENDP", 1)[0]
    body = "\n".join(line.split(";", 1)[0].strip() for line in body.splitlines())
    body = body.replace("@DATA", "0x2000")
    body = re.sub(r"S\[([^]]+)\]", r"byte ptr [\1+2]", body)
    body = re.sub(r"\bN\b", "word ptr [0]", body)
    encoded, _ = Ks(KS_ARCH_X86, KS_MODE_16).asm(body, addr=0)
    code = bytes(encoded)
    cases = [b"hello", b"x", b"ab", b"abcd", b"aaaa", b"level",
             b"hello world", b"a\0b", bytes(range(100))]

    for text in cases:
        cpu = Uc(UC_ARCH_X86, UC_MODE_16)
        cpu.mem_map(0, 0x100000)
        cpu.mem_write(0x10000, code)
        cpu.reg_write(UC_X86_REG_CS, 0x1000)
        cpu.reg_write(UC_X86_REG_DS, 0x0800)
        cpu.reg_write(UC_X86_REG_SS, 0x3000)
        cpu.reg_write(UC_X86_REG_SP, 0x100)
        payload = struct.pack("<H", len(text)) + text
        cpu.mem_write(0x20000 - 16, b"\xA5" * 16 + payload + b"\x5A" * 16)
        exited = []
        depths = []

        def instruction(current, address, size, _):
            depths.append(current.reg_read(UC_X86_REG_SP))

        def interrupt(current, number, _):
            assert number == 0x21 and current.reg_read(UC_X86_REG_AX) == 0x4C00
            exited.append(True)
            current.emu_stop()

        cpu.hook_add(UC_HOOK_CODE, instruction)
        cpu.hook_add(UC_HOOK_INTR, interrupt)
        cpu.emu_start(0x10000, 0x10000 + len(code), count=20 * len(text) + 100)
        assert exited, ("DOS exit not reached", text)
        assert cpu.reg_read(UC_X86_REG_DS) == 0x2000
        assert cpu.reg_read(UC_X86_REG_SP) == 0x100
        assert min(depths) == 0x100 - 2 * len(text)
        expected = struct.pack("<H", len(text)) + text[::-1]
        actual = bytes(cpu.mem_read(0x20000 - 16, 16 + len(payload) + 16))
        assert actual == b"\xA5" * 16 + expected + b"\x5A" * 16, text

    print(f"PASS: {len(cases)} strings; reversal, bounds, N, DS, stack depth/balance, DOS exit.")


if __name__ == "__main__":
    main()
