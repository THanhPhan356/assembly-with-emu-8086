"""Assemble the three COM templates with FASM and execute them with Unicorn.

Run with FASM on PATH (or set FASM) and the unicorn Python package available.
FASM syntax is substituted only for MASM-style declarations and operands.
"""
from pathlib import Path
import os
import random
import re
import struct
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_BP, UC_X86_REG_CS, UC_X86_REG_CX,
    UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SI, UC_X86_REG_SS,
    UC_X86_REG_SP,
)


def check(name, values, directory, n=None):
    n = len(values) if n is None else n
    source = Path(__file__).with_name(name).joinpath(name + ".asm").read_text(encoding="ascii")
    symbol = {"count_odd": "A", "sort_signed_words": "ARR", "reverse_string": "S"}[name]
    declaration = ("db " + ", ".join(map(str, values)) if name == "reverse_string"
                   else "dw " + ", ".join(map(str, values or [0])))
    source = re.sub(r"^N\s+dw .*", f"N dw {n}", source, flags=re.M | re.I)
    source = re.sub(rf"^{symbol}\s+d[bw] .*", symbol + " " + declaration,
                    source, flags=re.M | re.I)
    lines = ["format binary", "use16"]
    for raw in source.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line.endswith(" ENDP"):
            continue
        line = re.sub(r"^(\w+) PROC$", r"\1:", line)
        if line and not re.search(r"\b(?:db|dw)\b", line, re.I):
            line = re.sub(r"\bN\b", "word [N]", line)
            line = re.sub(rf"{symbol}\[([^]]+)\]", rf"[{symbol} + \1]", line)
            line = line.replace("offset ", "").replace("word ptr", "word")
        lines.append(line)
    assembly, binary = directory / "check.asm", directory / "check.com"
    assembly.write_text("\n".join(lines) + "\n", encoding="ascii")
    result = subprocess.run([os.environ.get("FASM", "fasm"), str(assembly), str(binary)],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    code = binary.read_bytes()
    assert code[0] in (0xEB, 0xE9), "Missing jump over COM data"
    data_offset = 2 if code[0] == 0xEB else 3
    original = (bytes(values) if name == "reverse_string"
                else struct.pack("<" + "h" * max(1, len(values)), *(values or [0])))
    assert code[data_offset:data_offset + 2 + len(original)] == struct.pack("<H", n) + original
    expected = bytearray(code)
    if name != "count_odd":
        output = (bytes(values[::-1]) if name == "reverse_string"
                  else struct.pack("<" + "h" * max(1, n), *(sorted(values) or [0])))
        expected[data_offset + 2:data_offset + 2 + len(output)] = output

    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    segment, base = 0x2000, 0x20000
    for reg in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        cpu.reg_write(reg, segment)
    preserved = {UC_X86_REG_BP: 0x1357, UC_X86_REG_CX: 0x2468, UC_X86_REG_SI: 0x369C}
    for reg, value in preserved.items():
        cpu.reg_write(reg, value)
    cpu.reg_write(UC_X86_REG_SP, 0xFFFE)
    cpu.mem_write(base, b"\xCD\x20")  # PSP's INT 20h; initial stack word is zero.
    cpu.mem_write(base + 0xFFFE, b"\0\0")
    entry = base + 0x100
    cpu.mem_write(entry - 16, b"\xA5" * 16 + code + b"\x5A" * 16)
    depths, exited = [], []

    def instruction(current, address, size, _):
        depths.append(current.reg_read(UC_X86_REG_SP))

    def interrupt(current, number, _):
        assert number == 0x20
        assert current.reg_read(UC_X86_REG_SP) == 0, "Unbalanced COM return stack"
        exited.append(True)
        current.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, instruction)
    cpu.hook_add(UC_HOOK_INTR, interrupt)
    cpu.emu_start(entry, base + 0x10000, count=60 * max(1, n) ** 2 + 200)
    assert exited, (name, values, "DOS exit not reached")
    assert cpu.reg_read(UC_X86_REG_DS) == segment
    actual = bytes(cpu.mem_read(entry - 16, len(code) + 32))
    assert actual == b"\xA5" * 16 + bytes(expected) + b"\x5A" * 16, (name, values)
    if name == "count_odd":
        assert cpu.reg_read(UC_X86_REG_AX) == sum(v & 1 for v in values[:n])
        assert all(cpu.reg_read(reg) == value for reg, value in preserved.items())
    if name == "reverse_string":
        assert min(depths[0:-1]) == 0xFFFE - max(2, 2 * n), "Wrong reversal stack depth"


def main():
    rng = random.Random(8086)
    arrays = [[], [5], [2, 1], [1, 2], [7, 7, 7],
              [7, -3, 12, 0, -8, 7], [-32768, 32767, -1, 0, 1],
              list(range(20)), list(range(20, 0, -1))]
    arrays += [[rng.randint(-32768, 32767) for _ in range(rng.randrange(32))]
               for _ in range(20)]
    strings = [b"hello", b"x", b"ab", b"abcd", b"aaaa", b"level",
               b"hello world", b"a\0b", bytes(range(100))]
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        for name in ("count_odd", "sort_signed_words"):
            for values in arrays:
                check(name, values, directory)
        check("count_odd", [2, 5, 8, 3], directory)
        check("count_odd", [2, 5, 8, 3], directory, n=2)
        check("count_odd", [2, 5, 8, 3], directory, n=0)
        for text in strings:
            check("reverse_string", text, directory)
    print(f"PASS: {2 * len(arrays) + 3 + len(strings)} COM cases; results, memory, stack, DOS exit.")


if __name__ == "__main__":
    main()
