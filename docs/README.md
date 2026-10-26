# Study notes

Self-contained learning and revision documents for Intel 8086/8088 architecture and assembly programming with emu8086.

| Note | Language | Topics |
| --- | --- | --- |
| [note_01.html](note_01.html) | English | Session 1, both parts: number representation, architecture, segmented memory, flags, MOV, addressing modes and worked machine-code encodings, including direction bits and signed displacement. |
| [note_02.html](note_02.html) | English | Session 2, both parts: MOV encoding, data transfer, pointers, stacks, port I/O, XLAT and ADD with all six status flags, signed interpretation and the four lecture sums. |

## How to use

[Read note_01 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_01.html) through GitHub Pages.

[Read note_02 online](https://thanhphan356.github.io/assembly-with-emu-8086/note_02.html) through GitHub Pages.

Download either HTML file and open it in a browser. GitHub's file view displays the source rather than the lesson.

Each note contains its own styles and interactive tools, so no installation, internet connection or companion files are needed. Select an illustration to view its original resolution. Use the contents to navigate, try the worked exercises and quiz, and select **Print / save PDF** for a printable version with answers.

## Sources and scope

The notes include cropped illustrations from the supplied slides, embedded in each HTML file: 14 in `note_01` and 10 in `note_02`. Explanations and captions are in English; original figure labels, including Vietnamese, are preserved. Each figure cites its deck and slide number.

`note_01` covers session 1 (16/03), [part 1](https://www.youtube.com/watch?v=zt21WRo_gIo) and [part 2](https://www.youtube.com/watch?v=V-i9OKeEW3A), using the supplied Part1/Part2 slides and emu8086 tutorials as supporting sources. Section 10 completes the MOV encoding examples, including reversed direction, register mode, displacement byte order and the signed `+0F3h` correction. The chapter has 15 sections, 14 worked exercises, 2 calculators and an 8-question quiz.

`note_02` covers session 2 (23/03), [part 1](https://www.youtube.com/watch?v=OOrzonM5nbE) and [part 2](https://www.youtube.com/watch?v=5ZYxHLq4Ylk). It contains 16 sections, 14 worked exercises, 4 short programs, 3 calculators and a 10-question quiz. Section 11 develops ADD, two's complement, CF versus OF, and the four sums from part 2: `3488h+2212h`, `87h+DDh`, `38h+DDh` and `4687h+4A9Eh`.

Topic coverage and approximate timestamps were checked against Vietnamese automatic captions. Each chapter lists the roles of the lecture, slides, emu8086 documentation and Intel manual. The chapters explain the material by topic rather than reproducing the transcripts. The figures come from the original supplied slides, not inferred video annotations.

The notes focus on the original 8086/8088 and classic IBM PC model. Their calculators and quizzes have been checked in a browser. The four `note_02` programs, ADD flags and encoding examples were checked separately with a 16-bit assembler/emulator; they have not been stepped through in the emu8086 application. The `note_01` practice listings still need emulator verification. Hardware I/O and original processor timing are outside these checks. Rights to the original lecture and slides remain with their respective authors.
