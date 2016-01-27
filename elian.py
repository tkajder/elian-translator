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

    def __str__(self):
        word_start = 0
        words = []
        space = characters[' ']

        for idx, elian_char in enumerate(self.characters):
            if elian_char == space:
                word = self.characters[word_start:idx]
                word_start = idx + 1
                if word:
                    words.append(word)

        final_word = self.characters[word_start:]
        words.append(final_word)

        line = []
        lines = []
        line_len = 0
        for word in words:
            word_len = sum([1 + len(elian_char) for elian_char in word])
            if line_len + word_len > 70:
                lines.append(line)
                line = [word]
                line_len = word_len
            else:
                line.append(word)
                line_len += word_len + 4

        lines.append(line)

        str_lines = []
        for line in lines:
            upper_line = ''
            middle_line = ''
            lower_line = ''
            for word in line:
                for elian_char in word:
                    upper_line += elian_char.upper + ' '
                    middle_line += elian_char.middle + ' '
                    lower_line += elian_char.lower + ' '
                upper_line += '    '
                middle_line += '    '
                lower_line += '    '

            str_lines.append(upper_line)
            str_lines.append(middle_line)
            str_lines.append(lower_line)

        return '\n'.join(str_lines)


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
    parser = argparse.ArgumentParser(description='Generate the elian script representation of ascii text using unicode box characters')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', type=str, help='the text to convert into elian script')
    group.add_argument('-f', '--file', type=argparse.FileType('r'), help='the file containing ascii text to convert into elian script')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='a file to write the elian script representaion to')
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
