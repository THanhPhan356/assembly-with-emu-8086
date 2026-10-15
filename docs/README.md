# Study notes

Self-contained learning and revision documents for Intel 8086/8088 architecture and assembly programming with emu8086.

| Note | Language | Topics |
| --- | --- | --- |
| [note_01.html](note_01.html) | English | Number representation, little-endian, buses, BIU/EU, registers, segmented memory, flags, IBM PC memory and I/O, MOV, addressing modes and introductory instruction encoding. |
| [note_02.html](note_02.html) | English | MOV encoding and signed displacement, XCHG, LEA, LDS/LES, flag access, PUSH/POP, stack wraparound, preserving state, port I/O and XLAT. |

## How to use

[Read note_01 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_01.html) through GitHub Pages.

[Read note_02 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_02.html) through GitHub Pages.

Download either HTML file and open it in a browser. GitHub's file view displays the source rather than the lesson.

Each note contains its own styles and interactive tools, so no installation, internet connection or companion files are needed. Select an illustration to view its original resolution. Use the contents to navigate, try the worked exercises and quiz, and select **Print / save PDF** for a printable version with answers.

## Sources and scope

The notes include cropped illustrations from the supplied slides, embedded in each HTML file: 14 in `note_01` and 8 in `note_02`. Explanations and captions are in English; original figure labels, including Vietnamese, are preserved. Each figure cites its deck and slide number.

`note_01` is a study chapter based on Nguyễn Huy Hoàng's first microprocessor lecture, the supplied Part1/Part2 slides, and emu8086 tutorials. The note includes topic-level citations and a reference list explaining each source's role, with the Intel 8086 manual listed for further reading.

`note_02` covers [session 2 (23/03), part 1](https://www.youtube.com/watch?v=OOrzonM5nbE), using the video's Vietnamese automatic captions and the supplied Part2 slides. It contains 15 sections, 10 worked exercises, 3 short programs, 2 calculators and an 8-question quiz. Sources, approximate timestamps and corrections are listed inside the chapter, including the distinction between positive `+0F3h` and signed byte displacement `F3h`.

The notes focus on the original 8086/8088 and classic IBM PC model. Their calculators and quizzes have been checked in a browser. The three `note_02` programs and encoding examples were checked separately with a 16-bit assembler/emulator; they have not been stepped through in the emu8086 application. The `note_01` programs still need emulator verification. Hardware I/O and original processor timing are outside these checks. Rights to the original lecture and slides remain with their respective authors.
