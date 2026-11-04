"""Assemble and execute the agreed 8086 COM solution with FASM and Unicorn."""

from pathlib import Path
import os
import re
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
    UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_IP,
)


SOURCE = Path(__file__).with_name('nonzero_average.asm').read_text(encoding='ascii')
CASES = [
    ('supplied array', [1, 2, -3, 0, 4]),
    ('C caller example', [1, 3, 5, -1, 0, 2]),
    ('all zeros', [0, 0, 0]),
    ('empty array', []),
    ('negative fraction', [-5, 0, 2]),
    ('positive fraction', [2, 0, 3]),
    ('negative average', [-3, 0, -5]),
    ('minimum byte', [-128]),
    ('maximum byte', [127]),
    ('cancellation', [-128, 127, 1]),
    ('minimum sum', [-128] * 256),
    ('maximum sum', [127] * 258 + [1]),
]


def assemble(values, directory):
    source = re.sub(r'^ARR db .*$', 'ARR db ' + ', '.join(map(str, values or [0])),
                    SOURCE, flags=re.M)
    source = re.sub(r'^N\s+dw .*$', f'N dw {len(values)}', source, flags=re.M)
    lines = ['format binary', 'use16']
    for raw in source.splitlines():
        line = raw.split(';', 1)[0].strip()
        if line and not re.search(r'\b(?:db|dw)\b', line):
            line = re.sub(r'\b(tong|dem|N)\b', r'[\1]', line)
            line = line.replace('ARR[si]', '[ARR + si]')
        lines.append(line)
    assembly = directory / 'check.asm'
    binary = directory / 'check.com'
    assembly.write_text('\n'.join(lines) + '\n', encoding='ascii')
    result = subprocess.run([os.environ.get('FASM', 'fasm'), str(assembly), str(binary)],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    return binary.read_bytes()


def check(values, binary):
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    segment = 0x2000
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        cpu.reg_write(register, segment)
    cpu.reg_write(UC_X86_REG_SP, 0xfffe)
    entry = segment * 16 + 0x100
    cpu.mem_write(entry, binary)
    assert binary[-1] == 0xc3, 'Expected the final 16-bit RET'
    stop = entry + len(binary) - 1
    cpu.emu_start(entry, stop, count=20 * len(values) + 100)
    assert cpu.reg_read(UC_X86_REG_IP) == stop - segment * 16, 'RET not reached'
    assert cpu.reg_read(UC_X86_REG_SP) == 0xfffe, 'Unexpected stack change'

    total = sum(values)
    count = sum(value != 0 for value in values)
    expected = (abs(total) // count) * (-1 if total < 0 else 1) if count else 0
    assert cpu.reg_read(UC_X86_REG_AX) == expected & 0xffff
    assert binary[0] in (0xeb, 0xe9), 'Expected the initial jump over the data'
    data = entry + (2 if binary[0] == 0xeb else 3)
    array_size = max(1, len(values))
    assert cpu.mem_read(data, array_size) == bytes(v & 0xff for v in values or [0])
    assert int.from_bytes(cpu.mem_read(data + array_size + 2, 2), 'little', signed=True) == total
    assert int.from_bytes(cpu.mem_read(data + array_size + 4, 2), 'little') == count


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as temporary:
        for name, values in CASES:
            check(values, assemble(values, Path(temporary)))
            print(f'PASS: {name}')
    print(f'PASS: {len(CASES)} assembled 16-bit machine-code cases; AX, sum, count and array checked.')
