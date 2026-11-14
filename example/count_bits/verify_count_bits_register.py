"""Assemble Count with FASM and check real 16-bit instructions using Unicorn.

Run: python verify_count_bits_register.py
Requires: fasm on PATH (or FASM set to its executable), and pip install unicorn.
The COM harness tests the procedure; open the EXE source in emu8086 separately.
"""

import os
from pathlib import Path
import random
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CX, UC_X86_REG_DX,
    UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP, UC_X86_REG_SP,
    UC_X86_REG_IP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
    UC_X86_REG_SS,
)


def main():
    source = Path(__file__).with_name("count_bits_register_exe.asm").read_text()
    procedure = source.split("Count PROC\n", 1)[1].split("Count ENDP", 1)[0]
    # Stop before HLT, after CALL and RET have both executed.
    harness = "format binary\nuse16\norg 100h\ncall Count\nhlt\nCount:\n" + procedure
    with tempfile.TemporaryDirectory() as directory:
        assembly = Path(directory) / "check.asm"
        binary = Path(directory) / "check.com"
        assembly.write_text(harness, encoding="ascii")
        subprocess.run([os.environ.get("FASM", "fasm"), str(assembly), str(binary)],
                       check=True, capture_output=True, timeout=30)
        machine_code = binary.read_bytes()

    assert machine_code[0] == 0xE8 and machine_code[3] == 0xF4
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x10000)
    cpu.mem_write(0x100, machine_code)
    rng = random.Random(0)
    cases = [0, 1, 13, 0x7FFF, 0x8000, 0xFFFF, 0xAAAA, 0x5555]
    cases += [1 << bit for bit in range(16)]
    cases += [rng.randrange(0x10000) for _ in range(256)]
    preserved = (UC_X86_REG_BX, UC_X86_REG_CX, UC_X86_REG_DX,
                 UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP)

    for value in cases:
        for register in (UC_X86_REG_CS, UC_X86_REG_DS,
                         UC_X86_REG_ES, UC_X86_REG_SS):
            cpu.reg_write(register, 0)
        for index, register in enumerate(preserved):
            cpu.reg_write(register, 0x1234 + index)
        cpu.reg_write(UC_X86_REG_SP, 0xFFFE)
        cpu.reg_write(UC_X86_REG_AX, value)
        cpu.emu_start(0x100, 0x103, count=256)
        assert cpu.reg_read(UC_X86_REG_IP) == 0x103, "Return not reached"
        assert cpu.reg_read(UC_X86_REG_AX) == value.bit_count(), hex(value)
        assert cpu.reg_read(UC_X86_REG_SP) == 0xFFFE, "Stack not balanced"
        for index, register in enumerate(preserved):
            assert cpu.reg_read(register) == 0x1234 + index, register

    print(f"PASS: {len(cases)} cases; AX result, preserved registers and SP.")


if __name__ == "__main__":
    main()
