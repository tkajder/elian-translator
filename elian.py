#!/usr/bin/env python3

import argparse

'''
Elian Characters Display Form:

─╮ ─╮  ╷ ╭─╮ ╭─╮ ╷ ╷ ╭─ ╭─ ╷
 ╵ ─╯ ─╯ ╵ ╵ ╰─╯ ╰─╯ ╵  ╰─ ╰─
─╮ ─╮  ╷ ╭─╮   ╷   ╷ ╭─ ╭─ ╷
 │  │  │ │ ╵ ╭─┤ ╷ │ │  │  │
 ╵ ─╯ ─╯ ╵   ╰─╯ ╰─╯ ╵  ╰─ ╰─
─╮ ─╮  ╷ ╭─╮  .╷   ╷ ╭─ ╭─ ╷
·│ ·│ ·│ │·╵ ╭─┤ ╷·│ │· │· │·
 ╵ ─╯ ─╯ ╵   ╰─╯ ╰─╯ ╵  ╰─ ╰─
'''


class ElianScript(object):

    def __init__(self):
        self.characters = []

    def append(self, character):
        self.characters.append(character)

    def _chunk_words(self):
        space = characters.get(' ')

        word_start = 0

        for i, elian_char in enumerate(self.characters):
            if elian_char == space:
                word = self.characters[word_start:i]
                if word:
                    yield word
                else:
                    yield space

                word_start = i + 1

        yield self.characters[word_start:]

    def _chunk_lines(self, line_char_limit=70):
        words = self._chunk_words()

        line = []
        line_char_len = 0

        for word in words:
            word_char_len = sum([1 + len(elian_char) for elian_char in word])

            if line_char_len + word_char_len > line_char_limit:
                yield line

                if len(word) == 1 and word[0] == space:
                    line = []
                    line_char_len = 0
                else:
                    line = [word]
                    line_char_len = word_char_len
            else:
                line.append(word)
                line_char_len += word_char_len

        yield line

    def __str__(self):
        lines = self._chunk_lines()

        char_space_divider = ' '
        word_space_divider = '    '

        elian_strs = []
        for line in lines:
            upper_line, middle_line, lower_line = '', '', ''

            for word in line:
                upper_line += char_space_divider.join(
                    elian_char.upper for elian_char in word)
                middle_line += char_space_divider.join(
                    elian_char.middle for elian_char in word)
                lower_line += char_space_divider.join(
                    elian_char.lower for elian_char in word)

                upper_line += word_space_divider
                middle_line += word_space_divider
                lower_line += word_space_divider

            elian_strs.append(upper_line)
            elian_strs.append(middle_line)
            elian_strs.append(lower_line)

        return '\n'.join(elian_strs)


class ElianCharacter(object):

    def __init__(self, upper, middle, lower):
        self.upper = upper
        self.middle = middle
        self.lower = lower
        assert len(self.upper) == len(self.middle) == len(self.lower)

    def __len__(self):
        return len(self.upper)

    def __eq__(self, other):
        return (self.upper == other.upper
                and self.middle == other.middle
                and self.lower == other.lower)

    def __str__(self):
        return '{upper}\n{middle}\n{lower}'.format(
            upper=self.upper,
            middle=self.middle,
            lower=self.lower)

characters = {
    'A': ElianCharacter('  ', '─╮', ' ╵'),
    'B': ElianCharacter('  ', '─╮', '─╯'),
    'C': ElianCharacter('  ', ' ╷', '─╯'),
    'D': ElianCharacter('   ', '╭─╮', '╵ ╵'),
    'E': ElianCharacter('   ', '╭─╮', '╰─╯'),
    'F': ElianCharacter('   ', '╷ ╷', '╰─╯'),
    'G': ElianCharacter('  ', '╭─', '╵ '),
    'H': ElianCharacter('  ', '╭─', '╰─'),
    'I': ElianCharacter('  ', '╷ ', '╰─'),
    'J': ElianCharacter('─╮', ' │', ' ╵'),
    'K': ElianCharacter('─╮', ' │', '─╯'),
    'L': ElianCharacter(' ╷', ' │', '─╯'),
    'M': ElianCharacter('╭─╮', '│ ╵', '╵  '),
    'N': ElianCharacter('  ╷', '╭─┤', '╰─╯'),
    'O': ElianCharacter('  ╷', '╷ │', '╰─╯'),
    'P': ElianCharacter('╭─', '│ ', '╵ '),
    'Q': ElianCharacter('╭─', '│ ', '╰─'),
    'R': ElianCharacter('╷ ', '│ ', '╰─'),
    'S': ElianCharacter('─╮', '·│', ' ╵'),
    'T': ElianCharacter('─╮', '·│', '─╯'),
    'U': ElianCharacter(' ╷', '·│', '─╯'),
    'V': ElianCharacter('╭─╮', '│·╵', '╵  '),
    'W': ElianCharacter(' ·╷', '╭─┤', '╰─╯'),
    'X': ElianCharacter('  ╷', '╷·│', '╰─╯'),
    'Y': ElianCharacter('╭─', '│·', '╵ '),
    'Z': ElianCharacter('╭─', '│·', '╰─'),
    'UNUSED': ElianCharacter('╷ ', '│·', '╰─'),
    ' ': ElianCharacter(' ', ' ', ' ')
}


def text_to_elian_script(text):
    script = ElianScript()

    for c in text.upper():
        elian_char = characters.get(c)
        if elian_char:
            script.append(elian_char)

    return script


def cli():
    parser = argparse.ArgumentParser(
        description='Generate the elian script representation'
        ' of ascii text using unicode box characters')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-t', '--text', type=str, help='the text to convert'
        ' into elian script')
    group.add_argument('-f', '--file', type=argparse.FileType('r'),
                       help='the file containing ascii'
                       ' text to convert into elian script')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        help='a file to write the elian'
                        ' script representaion to')
    args = parser.parse_args()
    return args


def main():
    args = cli()

    if args.file:
        text = text_to_elian_script(args.file.read())
        args.file.close()
    elif args.text:
        text = text_to_elian_script(args.text)
    else:
        raise AttributeError('Need input of text or file to convert to elian.')

    if args.output:
        args.output.write(str(text))
        args.output.close()
    else:
        print(text)

if __name__ == '__main__':
    main()
