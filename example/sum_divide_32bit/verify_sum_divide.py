"""Check the supplied arithmetic and reproduce its DIV error in 16-bit x86."""

from pathlib import Path
import os
import re
import struct
import subprocess
import tempfile

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_CX, UC_X86_REG_DX, UC_X86_REG_SI,
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_SP, UC_X86_REG_EFLAGS,
)

ROOT = Path(__file__).resolve().parent


def assemble(source, directory):
    lines = ['format MZ', 'entry code_seg:MAIN', 'stack 100h']
    variables = re.findall(r'^(\w+)\s+DW\b', source, re.M)
    for raw in source.splitlines():
        line = raw.split(';', 1)[0].strip()
        if not line or line.startswith(('.MODEL', '.STACK')):
            continue
        if line == '.DATA':
            line = 'segment data_seg'
        elif line == '.CODE':
            line = 'segment code_seg'
        elif line == 'MAIN PROC':
            line = 'MAIN:'
        elif line in ('MAIN ENDP', 'END MAIN'):
            continue
        elif not re.search(r'\bDW\b', line) and not line.endswith(':'):
            line = line.replace('@DATA', 'data_seg')
            for name in variables:
                line = re.sub(r'\b' + name + r'\b', '[' + name + ']', line)
        lines.append(line)
    path = directory / 'sum_divide_fasm.asm'
    exe = directory / 'sum_divide.exe'
    path.write_text('\n'.join(lines) + '\n', encoding='ascii')
    subprocess.run([os.environ.get('FASM', 'fasm'), str(path), str(exe)],
                   check=True, capture_output=True, timeout=30)
    return exe.read_bytes()


def load_exe(exe):
    header = struct.unpack_from('<14H', exe)
    magic, _, _, relocations, paragraphs, _, _, ss, sp, _, ip, cs, table, _ = header
    assert magic == 0x5a4d
    load_segment = 0x2000
    image = bytearray(exe[paragraphs * 16:])
    for i in range(relocations):
        offset, segment = struct.unpack_from('<HH', exe, table + i * 4)
        position = segment * 16 + offset
        value = struct.unpack_from('<H', image, position)[0]
        struct.pack_into('<H', image, position, (value + load_segment) & 0xffff)
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    cpu.mem_write(load_segment * 16, bytes(image))
    for register in (UC_X86_REG_DS, UC_X86_REG_ES):
        cpu.reg_write(register, load_segment - 0x10)
    cpu.reg_write(UC_X86_REG_CS, load_segment + cs)
    cpu.reg_write(UC_X86_REG_SS, load_segment + ss)
    cpu.reg_write(UC_X86_REG_SP, sp)
    return cpu, (load_segment + cs) * 16 + ip


def main():
    source = (ROOT / 'sum_divide.asm').read_text(encoding='ascii')
    data = source.split('NUMBERS DW', 1)[1].split('DIVISOR', 1)[0]
    words = [int(x, 16) for x in re.findall(r'\b([0-9A-F]+)h\b', data)]
    assert len(words) == 8
    numbers = [words[i] | (words[i + 1] << 16) for i in range(0, 8, 2)]
    assert numbers == [0x20e010a0, 0x40f030b0, 0x600050c0, 0x800070d0]
    assert sum(numbers) == 0x141d102e0 > 0xffffffff
    stored = sum(numbers) & 0xffffffff
    assert stored == 0x41d102e0
    assert divmod(stored, 1000) == (1104216, 800)
    assert stored // 1000 > 0xffff

    rows, faults, div_inputs, low_carry, high_carry = [], [], [], [], []
    pending_loop = []
    with tempfile.TemporaryDirectory() as temporary:
        cpu, entry = load_exe(assemble(source, Path(temporary)))

        def word(offset):
            address = cpu.reg_read(UC_X86_REG_DS) * 16 + offset
            return int.from_bytes(cpu.mem_read(address, 2), 'little')

        def instruction(current, address, size, _):
            if pending_loop:
                rows[-1]['cx'] = current.reg_read(UC_X86_REG_CX)
                pending_loop.clear()
            code = bytes(current.mem_read(address, size))
            if code == b'\x8b\x44\x02':
                low_carry.append(current.reg_read(UC_X86_REG_EFLAGS) & 1)
            elif code in (b'\x83\xc6\x04', b'\x81\xc6\x04\x00'):
                high_carry.append(current.reg_read(UC_X86_REG_EFLAGS) & 1)
            elif code[0] == 0xe2:
                rows.append({'low': word(18), 'high': word(20),
                             'ax': current.reg_read(UC_X86_REG_AX),
                             'si': current.reg_read(UC_X86_REG_SI)})
                pending_loop.append(True)
            elif code == b'\xf7\xf1':
                div_inputs.append((current.reg_read(UC_X86_REG_DX),
                                   current.reg_read(UC_X86_REG_AX),
                                   current.reg_read(UC_X86_REG_CX)))

        def interrupt(current, number, _):
            faults.append(number)
            current.emu_stop()

        cpu.hook_add(UC_HOOK_CODE, instruction)
        cpu.hook_add(UC_HOOK_INTR, interrupt)
        cpu.emu_start(entry, 0x100000, count=1000)
        assert [(r['high'], r['low'], r['ax'], r['si'], r['cx']) for r in rows] == [
            (0x20e0, 0x10a0, 0x20e0, 4, 3),
            (0x61d0, 0x4150, 0x40f0, 8, 2),
            (0xc1d0, 0x9210, 0x6000, 12, 1),
            (0x41d1, 0x02e0, 0x8000, 16, 0),
        ], rows
        assert low_carry == [0, 0, 0, 1], low_carry
        assert high_carry == [0, 0, 0, 1], high_carry
        assert div_inputs == [(0x41d1, 0x02e0, 1000)], div_inputs
        assert faults == [0], faults
        assert word(18) == 0x02e0 and word(20) == 0x41d1
        assert word(22) == 0 and word(24) == 0
    for i, row in enumerate(rows, 1):
        print(f"Loop {i}: SUM={row['high']:04X}:{row['low']:04X}, "
              f"AX={row['ax']:04X}, SI=NUMBERS+{row['si']}, CX={row['cx']}, "
              f'low carry={low_carry[i-1]}, high carry={high_carry[i-1]}')
    print('PASS: full sum, stored sum, four machine-code loop traces, carry flags, '
          'DX:AX division input, divide-error interrupt 0, and unreached quotient stores.')


if __name__ == '__main__':
    main()
