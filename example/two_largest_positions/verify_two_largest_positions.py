"""Assemble the two-pass COM program with FASM and execute it with Unicorn."""

from pathlib import Path
import os
import random
import re
import struct
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
from unicorn.x86_const import (
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_SP, UC_X86_REG_IP,
)


SOURCE = Path(__file__).with_name('two_largest_positions.asm').read_text(encoding='ascii')


def check(values, directory):
    source = re.sub(r'^A\s+dw .*$', 'A dw ' + ', '.join(map(str, values or [0])),
                    SOURCE, flags=re.M)
    source = re.sub(r'^N\s+dw .*$', f'N dw {len(values)}', source, flags=re.M)
    lines = ['format binary', 'use16']
    for raw in source.splitlines():
        line = raw.split(';', 1)[0].strip()
        if line and not re.search(r'\b(?:db|dw)\b', line):
            line = re.sub(r'\b(N|max1|max2|pos1|pos2)\b', r'word [\1]', line)
            line = re.sub(r'A\[([^]]+)\]', r'[A + \1]', line)
        lines.append(line)
    assembly = directory / 'check.asm'
    binary = directory / 'check.com'
    assembly.write_text('\n'.join(lines) + '\n', encoding='ascii')
    result = subprocess.run([os.environ.get('FASM', 'fasm'), str(assembly), str(binary)],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    code = binary.read_bytes()

    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    segment = 0x2000
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        cpu.reg_write(register, segment)
    cpu.reg_write(UC_X86_REG_SP, 0xfffe)
    entry = segment * 16 + 0x100
    cpu.mem_write(entry, code)
    assert code[-1] == 0xc3, 'Expected the final RET'
    stop = entry + len(code) - 1
    cpu.emu_start(entry, stop, count=40 * len(values) + 100)
    assert cpu.reg_read(UC_X86_REG_IP) == stop - segment * 16, 'RET not reached'
    assert cpu.reg_read(UC_X86_REG_SP) == 0xfffe, 'Unbalanced stack'

    assert code[0] in (0xeb, 0xe9), 'Expected a jump over the data'
    data = entry + (2 if code[0] == 0xeb else 3)
    original = struct.pack('<' + 'h' * max(1, len(values)), *(values or [0]))
    assert bytes(cpu.mem_read(data, len(original))) == original, 'Array changed'
    n, max1, max2, pos1, pos2 = struct.unpack('<Hhhhh', cpu.mem_read(data + len(original), 10))
    assert n == len(values), 'Length changed'
    if len(values) < 2:
        assert (pos1, pos2) == (-1, -1), (values, pos1, pos2)
    else:
        first, second = sorted(range(len(values)), key=lambda i: (-values[i], i))[:2]
        assert (pos1, pos2) == (first, second), (values, pos1, pos2)
        assert (max1, max2) == (values[first], values[second])


if __name__ == '__main__':
    cases = [
        [-7, 12, 5, 12, -2], [], [7], [1, 2], [2, 1], [0, 0],
        [-7, -2, -9, -3], [9, 9, 9], [-32768, -32768],
        [32767, -32768], [-32768, 0, 32767, 32767, -1],
        [1, 2, 3, 4], [4, 3, 2, 1],
    ]
    rng = random.Random(8086)
    cases += [[rng.choice([-32768, -1, 0, 1, 32767]) for _ in range(rng.randrange(25))]
              for _ in range(50)]
    with tempfile.TemporaryDirectory() as temporary:
        for values in cases:
            check(values, Path(temporary))
    print(f'PASS: {len(cases)} assembled 16-bit machine-code cases; positions, values and array checked.')
