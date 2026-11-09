"""Assemble both DOS EXE variants with FASM and execute them with Unicorn."""

from pathlib import Path
import os
import random
import re
import struct
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_DX, UC_X86_REG_CS, UC_X86_REG_DS,
    UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_SP,
)


def check(path, values, directory):
    source = path.read_text(encoding='ascii')
    source = re.sub(r'^(A|ARR)\s+dw .*$',
                    lambda m: m[1] + ' dw ' + ', '.join(map(str, values or [0])),
                    source, flags=re.M)
    source = re.sub(r'^N\s+(dw|equ) .*$',
                    lambda m: f'N {m[1]} {len(values)}', source, flags=re.M)
    variables = re.findall(r'^(\w+)\s+dw\b', source, re.M)
    lines = ['format MZ', 'entry code_seg:MAIN', 'stack 100h']
    for raw in source.splitlines():
        line = raw.split(';', 1)[0].strip()
        if not line or line.upper().startswith(('.MODEL', '.STACK', 'MAIN ENDP', 'END MAIN')):
            continue
        if line.upper() == '.DATA':
            line = 'segment data_seg'
        elif line.upper() == '.CODE':
            line = 'segment code_seg'
        elif line.upper() == 'MAIN PROC':
            line = 'MAIN:'
        elif not re.search(r'\b(dw|equ)\b', line, re.I):
            line = line.replace('@DATA', 'data_seg')
            line = re.sub(r'\b(A|ARR)\[([^]]+)\]', r'[\1 + \2]', line)
            for name in variables:
                if name not in ('A', 'ARR'):
                    line = re.sub(r'\b' + name + r'\b', r'word [' + name + ']', line)
        lines.append(line)
    assembly, binary = directory / 'check.asm', directory / 'check.exe'
    assembly.write_text('\n'.join(lines) + '\n', encoding='ascii')
    result = subprocess.run([os.environ.get('FASM', 'fasm'), str(assembly), str(binary)],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    exe = binary.read_bytes()
    magic, _, _, relocations, paragraphs, _, _, ss, sp, _, ip, cs, table, _ = struct.unpack_from('<14H', exe)
    assert magic == 0x5a4d and sp == 0x100
    load = 0x2000
    image = bytearray(exe[paragraphs * 16:])
    for i in range(relocations):
        offset, segment = struct.unpack_from('<HH', exe, table + 4 * i)
        position = segment * 16 + offset
        value = struct.unpack_from('<H', image, position)[0]
        struct.pack_into('<H', image, position, (value + load) & 0xffff)

    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    cpu.mem_write(load * 16, bytes(image))
    for register in (UC_X86_REG_DS, UC_X86_REG_ES):
        cpu.reg_write(register, load - 0x10)  # DOS initially points DS at the PSP.
    cpu.reg_write(UC_X86_REG_CS, load + cs)
    cpu.reg_write(UC_X86_REG_SS, load + ss)
    cpu.reg_write(UC_X86_REG_SP, sp)
    before_exit, exited = [], []

    def instruction(current, address, size, _):
        if bytes(current.mem_read(address, size)) == b'\xb4\x4c':
            before_exit.append((current.reg_read(UC_X86_REG_AX), current.reg_read(UC_X86_REG_DX)))

    def interrupt(current, number, _):
        assert number == 0x21 and current.reg_read(UC_X86_REG_AX) >> 8 == 0x4c
        exited.append(True)
        current.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, instruction)
    cpu.hook_add(UC_HOOK_INTR, interrupt)
    cpu.emu_start((load + cs) * 16 + ip, 0x100000, count=40 * len(values) + 100)
    assert exited and before_exit, 'DOS exit not reached'
    assert cpu.reg_read(UC_X86_REG_SP) == sp, 'Unbalanced stack'
    assert cpu.reg_read(UC_X86_REG_DS) == load, 'Data segment not initialized'
    data = load * 16
    original = struct.pack('<' + 'h' * max(1, len(values)), *(values or [0]))
    assert bytes(cpu.mem_read(data, len(original))) == original, 'Array changed'
    if '_v2_' in path.name:
        pos1, pos2 = struct.unpack('<hh', cpu.mem_read(data + len(original), 4))
        maxima = before_exit[-1]
    else:
        n, max1, max2, pos1, pos2 = struct.unpack('<Hhhhh', cpu.mem_read(data + len(original), 10))
        assert n == len(values), 'Length changed'
        maxima = (max1 & 0xffff, max2 & 0xffff)
    if len(values) < 2:
        assert (pos1, pos2) == (-1, -1), (values, pos1, pos2)
    else:
        first, second = sorted(range(len(values)), key=lambda i: (-values[i], i))[:2]
        assert (pos1, pos2) == (first, second), (values, pos1, pos2)
        assert maxima == (values[first] & 0xffff, values[second] & 0xffff)


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
    total = 0
    with tempfile.TemporaryDirectory() as temporary:
        for name in ('two_largest_positions_exe.asm', 'two_largest_positions_v2_exe.asm'):
            count = 0
            for values in cases:
                if '_v2_' in name and len(values) < 2:
                    continue  # The one-pass COM and EXE variants require N >= 2.
                check(Path(__file__).with_name(name), values, Path(temporary))
                count += 1
            print(f'PASS: {name}: {count} MZ EXE cases.')
            total += count
    print(f'PASS: {total} DOS EXE runs; positions, values, array, DS, stack and exit checked.')
