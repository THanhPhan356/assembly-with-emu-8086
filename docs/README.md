# Study notes

Self-contained learning and revision documents for Intel 8086/8088 architecture and assembly programming with emu8086.

| Note | Language | Topics |
| --- | --- | --- |
| [note_01.html](note_01.html) | English | Session 1, both parts: number representation, architecture, segmented memory, flags, MOV, addressing modes and worked machine-code encodings, including direction bits and signed displacement. |
| [note_02.html](note_02.html) | English | Session 2, both parts: MOV encoding, data transfer, pointers, stacks, port I/O, XLAT and ADD with all six status flags, signed interpretation and the four lecture sums. |
| [note_03.html](note_03.html) | English | Session 3: ADC, SUB, MUL/IMUL, DIV/IDIV, unary and logical operations, CMP/TEST, rotations/shifts, jumps, loops, calls, returns and interrupt frames. |
| [Read note_04 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_04.html) | English | Session 4: x86 register evolution, protected-mode selectors and descriptors, segment bounds, paging concepts, and revision of addresses, stacks, flags, loops and binary32. |
| [Read note_05 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_05.html) | English | Session 5: statements, declarations and arrays, COM/EXE startup, selection and loops, DOS services, character/case conversion, editable line input, stack reversal and decimal length output. |

## How to use

[Read note_01 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_01.html) through GitHub Pages.

[Read note_02 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_02.html) through GitHub Pages.

[Read note_03 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_03.html) through GitHub Pages.

[Read note_04 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_04.html) through GitHub Pages. Its standalone source file is [note_04.html](note_04.html).

[Read note_05 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_05.html) through GitHub Pages. Its standalone source file is [note_05.html](note_05.html).

Download any HTML file and open it in a browser. GitHub's file view displays the source rather than the lesson.

Each note contains its own styles and interactive tools, so no installation, internet connection or companion files are needed. Select an illustration to view its original resolution. Use the contents to navigate, try the worked exercises and quiz, and select **Print / save PDF** for a printable version with answers.

## Sources and scope

The notes include original slide illustrations embedded in each HTML file: 14 in `note_01`, 10 in `note_02`, and 12 each in `note_03`, `note_04` and `note_05`. Explanations and captions are in English; original figure labels, including Vietnamese, are preserved. Each figure cites its supplied deck/PDF page or its lecture timestamp and on-screen slide number.

`note_01` covers session 1 (16/03), [part 1](https://www.youtube.com/watch?v=zt21WRo_gIo) and [part 2](https://www.youtube.com/watch?v=V-i9OKeEW3A), using the supplied Part1/Part2 slides and emu8086 tutorials as supporting sources. Section 10 completes the MOV encoding examples, including reversed direction, register mode, displacement byte order and the signed `+0F3h` correction. The chapter has 15 sections, 14 worked exercises, 2 calculators and an 8-question quiz.

`note_02` covers session 2 (23/03), [part 1](https://www.youtube.com/watch?v=OOrzonM5nbE) and [part 2](https://www.youtube.com/watch?v=5ZYxHLq4Ylk). It contains 16 sections, 14 worked exercises, 4 short programs, 3 calculators and a 10-question quiz. Section 11 develops ADD, two's complement, CF versus OF, and the four sums from part 2: `3488h+2212h`, `87h+DDh`, `38h+DDh` and `4687h+4A9Eh`.

`note_03` covers [session 3 (30/03)](https://www.youtube.com/watch?v=5Lq03LyloGw). It contains 21 sections, 16 worked exercises, 5 short programs, an arithmetic/flag calculator, a bit-movement tracer and a 12-question quiz. It distinguishes signed overflow from borrow, defines implicit arithmetic registers and undefined flags, and traces both far-call and interrupt stack frames. The closing string/coprocessor topics are a brief overview, matching the lecture's scope.

`note_04` covers [session 4 (06/04)](https://www.youtube.com/watch?v=XJhnzRMaJh4). It contains 20 sections, 18 worked exercises, 5 short programs, a selector/segment-bound calculator, a binary32 decoder and a 12-question quiz. It distinguishes register widths, selector lookup, inclusive segment limits, and logical/linear/physical addresses. The revision examples explicitly state their inputs rather than reconstructing incomplete on-screen questions from captions. Protected-mode access policies and paging are explained conceptually; its executable programs stay in 8086 real mode.

`note_05` covers [session 5 (13/04)](https://www.youtube.com/watch?v=TgxFa8CcUIM). It contains 20 sections, 18 worked exercises, 5 complete applications, COM/EXE Hello templates, a DOS line-buffer inspector, an unsigned-decimal conversion tracer and a 12-question quiz. Nine illustrations are cropped from the actual lecture recording because the matching assembly deck was absent from the supplied files; three control-flow illustrations come from the supplied Part3 PDF. It corrects the input-buffer header, preservation of live AL, dollar-terminated versus counted output, empty-input stack loops and clearing DX before every decimal-conversion division.

Topic coverage and approximate timestamps were checked against Vietnamese automatic captions. Each chapter lists the roles of the lecture, slides, emu8086 documentation and Intel manual; `note_05` also cites Microsoft's MASM and DOS manuals. The chapters explain the material by topic rather than reproducing the transcripts. Figures use original supplied slides or inspected on-screen slides, with their source and any retained annotations identified.

The practice programs focus on the original 8086/8088 and classic IBM PC model; `note_04` additionally introduces later x86 memory-management concepts. The calculators and quizzes have been checked in a browser. The four `note_02` programs, ADD flags and encoding examples, and the five programs in each of `note_03` and `note_04` were checked separately with a 16-bit assembler/emulator; they have not been stepped through in the emu8086 application. The seven complete `note_05` listings were assembled and executed with a focused DOS-service harness, including empty/full buffers, embedded dollars and multi-digit conversion; the EXE template was also compiled with the installed emu8086 compiler. Its browser decimal tracer was checked for all 65,536 unsigned-word inputs. These checks do not replace a full interactive DOS session or real keyboard editing/redirection. The `note_01` practice listings still need emulator verification. Real protected-mode startup/table loading, hardware I/O and original processor timing are outside these checks. Rights to the original lecture and slides remain with their respective authors.
