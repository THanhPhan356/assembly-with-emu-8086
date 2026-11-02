"""Compile C and a FASM-compatible copy of the emu8086 source; compare outputs."""

from pathlib import Path
import os
import random
import re
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_SP, UC_X86_REG_AX, UC_X86_REG_AH, UC_X86_REG_AL,
    UC_X86_REG_DL,
)

ROOT = Path(__file__).resolve().parent


def expected(typed):
    values = [int(c) for c in typed if '0' <= c <= '9'][:8]
    assert len(values) == 8
    groups = [
        [x for x in values if x % 3 == 0],
        [x for x in values if x % 2 != 0 and x % 3 != 0],
        [x for x in values if x % 2 == 0 and x % 3 != 0],
    ]
    result = [n for g in groups for n in
              (len(g), sum(g), max(g, default=0), min(g, default=0))]
    return values, result, ' '.join(map(str, result)) + '\n'


def assemble(directory):
    source = (ROOT / 'group_a_statistics.asm').read_text(encoding='utf-8')
    variables = re.findall(r'^(\w+) db', source, re.M)
    lines = ['use16']
    for raw in source.splitlines():
        line = raw.split(';', 1)[0].strip()
        if not line:
            continue
        if line == 'ARR db 8 dup(?)':
            line = 'ARR db 8 dup(165)'
        elif ' db ' not in line and not line.endswith(':'):
            line = line.replace('ARR[si]', '[ARR+si]')
            for name in variables:
                if name != 'ARR':
                    line = re.sub(r'\b' + re.escape(name) + r'\b', '[' + name + ']', line)
        lines.append(line)
    path = directory / 'statistics_fasm.asm'
    binary_path = directory / 'statistics.com'
    path.write_text('\n'.join(lines) + '\n', encoding='ascii')
    subprocess.run([os.environ.get('FASM', 'fasm'), str(path), str(binary_path)],
                   check=True, capture_output=True, timeout=30)
    binary = binary_path.read_bytes()
    data_address = 0x10100 + binary.index(bytes([165]) * 8)
    return binary, data_address


def run_assembly(binary, data_address, typed):
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x20000)
    for reg in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        cpu.reg_write(reg, 0x1000)
    cpu.reg_write(UC_X86_REG_SP, 0xfffe)
    cpu.mem_write(0x10100, binary)
    characters = iter(typed)
    output = []
    exited = []

    def dos(current, number, _):
        assert number == 0x21, f'Unexpected interrupt {number:x}'
        ah = current.reg_read(UC_X86_REG_AH)
        if ah == 7:
            character = next(characters, None)
            assert character is not None, 'Input exhausted before eight digits'
            current.reg_write(UC_X86_REG_AL, ord(character))
        elif ah == 2:
            character = current.reg_read(UC_X86_REG_DL)
            output.append(chr(character))
            current.reg_write(UC_X86_REG_AL, character)
        elif ah == 0x4c:
            assert current.reg_read(UC_X86_REG_AL) == 0
            exited.append(True)
            current.emu_stop()
        else:
            raise AssertionError(f'Unexpected DOS function {ah:x}')

    def check_write(current, access, address, size, value, _):
        in_data = data_address <= address and address + size <= data_address + 20
        in_stack = 0x1ff00 <= address and address + size <= 0x20000
        assert in_data or in_stack, f'Out-of-bounds write at {address:x}'

    cpu.hook_add(UC_HOOK_INTR, dos)
    cpu.hook_add(UC_HOOK_MEM_WRITE, check_write)
    cpu.emu_start(0x10100, 0x20000, count=20000)
    assert exited, 'Program did not terminate'
    assert cpu.reg_read(UC_X86_REG_SP) == 0xfffe, 'Unbalanced stack'
    values, result, text = expected(typed)
    assert bytes(cpu.mem_read(data_address, 20)) == bytes(values + result), typed
    actual = ''.join(output)
    assert actual == text.replace('\n', '\r\n'), (typed, actual, text)
    return text


def main():
    cases = ['12345678', '03699912', '24824824', '12457812',
             '1234567890', ' 1 2\n3\t4,5;6x7!8', 'abc12345678',
             '88000011', '00000001', '55555550']
    cases += [str(i) * 8 for i in range(10)]
    rng = random.Random(0)
    cases += [''.join(str(rng.randrange(10)) for _ in range(8)) for _ in range(100)]
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        exe = directory / ('statistics.exe' if os.name == 'nt' else 'statistics')
        subprocess.run([os.environ.get('CC', 'gcc'), '-std=c11', '-Wall', '-Wextra',
                        '-Werror', '-pedantic', str(ROOT / 'group_a_statistics.c'),
                        '-o', str(exe)], check=True, timeout=30)
        binary, data_address = assemble(directory)
        for typed in cases:
            text = run_assembly(binary, data_address, typed)
            actual = subprocess.run([str(exe)], input=typed, text=True,
                                    capture_output=True, timeout=5, check=True)
            assert actual.stdout == text and not actual.stderr, (typed, actual)
        for typed in ('', '123', 'abc'):
            actual = subprocess.run([str(exe)], input=typed, text=True,
                                    capture_output=True, timeout=5)
            assert actual.returncode == 1 and not actual.stdout and actual.stderr
    print(f'PASS: {len(cases)} cases in C and assembled 16-bit x86; '
          'exact output, data/write bounds, balanced stack, and 3 C EOF cases.')


if __name__ == '__main__':
    main()
