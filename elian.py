#!/usr/bin/env python3

import argparse
import collections
import typing

'''
Elian Characters Display Form:
 a  b  c  d   e   f   g  h  i
─╮ ─╮  ╷ ╭─╮ ╭─╮ ╷ ╷ ╭─ ╭─ ╷
 ╵ ─╯ ─╯ ╵ ╵ ╰─╯ ╰─╯ ╵  ╰─ ╰─

 j  k  l  m   n   o   p  q  r
─╮ ─╮  ╷ ╭─╮   ╷   ╷ ╭─ ╭─ ╷
 │  │  │ │ ╵ ╭─┤ ╷ │ │  │  │
 ╵ ─╯ ─╯ ╵   ╰─╯ ╰─╯ ╵  ╰─ ╰─

 s  t  u  v   w   x   y  z
─╮ ─╮  ╷ ╭─╮  .╷   ╷ ╭─ ╭─ ╷
·│ ·│ ·│ │·╵ ╭─┤ ╷·│ │· │· │·
 ╵ ─╯ ─╯ ╵   ╰─╯ ╰─╯ ╵  ╰─ ╰─
'''


ElianCharacter = typing.NamedTuple(
    'ElianCharacter', [('upper', str), ('middle', str), ('lower', str)])
ListOfWords = typing.List[typing.List[ElianCharacter]]

CHARACTERS = {
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
SPACE = CHARACTERS[' ']


class ElianScript(collections.MutableSequence):

    def __init__(self, text: str = ''):
        self._characters = []
        self.extend_str(text)

    def __len__(self):
        return len(self._characters)

    def __getitem__(self, ii: int):
        return self._characters[ii]

    def __delitem__(self, ii: int):
        del self._characters[ii]

    def __setitem__(self, ii: int, val: ElianCharacter):
        self._characters[ii] = val

    def insert(self, ii: int, val: ElianCharacter):
        self._characters.insert(ii, val)

    def _str_to_elian_chars(self, text: str):
        '''Convert each character in text to matching elian character'''
        for char in text.upper():
            elian_char = CHARACTERS.get(char)

            # Ignore any characters not found in the elian dictionary standard
            if elian_char:
                yield elian_char

    def extend_str(self, val: str):
        '''Convert str to elian characters then extend normally'''
        self.extend(self._str_to_elian_chars(val))

    def _chunk_words(self):
        '''Yield grouped elian characters split on the elian space character'''
        word_start = 0

        for i, elian_char in enumerate(self._characters):
            if elian_char == SPACE:
                word = self._characters[word_start:i]

                # A slice[i:i] is empty which should only occur on space
                # character
                if word:
                    yield word
                else:
                    yield [SPACE]

                word_start = i + 1

        # Yield the remaining characters that were not broken by a space
        yield self._characters[word_start:]

    def _chunk_lines(self,
                     space_between_chars: int,
                     space_between_words: int,
                     line_char_limit: int = 70):
        '''Yield lines from words such that no line exceeds line_char_limit'''
        words = self._chunk_words()

        line = []
        line_char_len = 0

        for word in words:

            # Account for each characters text length and the space between in
            # each character
            word_char_len = sum(
                space_between_chars + len(elian_char.upper)
                for elian_char in word)

            total_word_len = word_char_len + space_between_words

            if line_char_len + total_word_len > line_char_limit:
                yield line

                # If the last character in a line is space, discard the space
                # from output instead of pushing to next line. If the word is a
                # space and the line is empty, discard the space.
                if len(word) == 1 and word[0] == SPACE:
                    line = []
                    line_char_len = 0
                else:
                    line = [word]
                    line_char_len = word_char_len
            elif line_char_len == 0 and len(word) == 1 and word[0] == SPACE:
                pass
            else:
                line.append(word)
                line_char_len += total_word_len

        # Yield the last line that did not pass the line_char_limit
        yield line

    def _word_to_upper_middle_lower(self, word: str, char_space_divider: str):
        '''Convert the word to characters upper, middle, lower text lines'''
        upper = char_space_divider.join(
            elian_char.upper for elian_char in word)
        middle = char_space_divider.join(
            elian_char.middle for elian_char in word)
        lower = char_space_divider.join(
            elian_char.lower for elian_char in word)

        return upper, middle, lower

    def _line_to_upper_middle_lower(self,
                                    line: ListOfWords,
                                    word_space_divider: str,
                                    char_space_divider: str):
        '''Convert the list of words to upper, middle, and lower text lines'''
        upper_line, middle_line, lower_line = '', '', ''

        for word in line:
            upper_word, middle_word, lower_word = \
                self._word_to_upper_middle_lower(word, char_space_divider)

            # Append a word space divider if there are words on the line
            if upper_line:
                upper_line += word_space_divider
                middle_line += word_space_divider
                lower_line += word_space_divider

            upper_line += upper_word
            middle_line += middle_word
            lower_line += lower_word

        return upper_line, middle_line, lower_line

    def __str__(self):
        '''Return the lined elian representation of internal characters'''

        # Define the space between characters and space between words for
        # readability
        char_space_divider = ' '*1
        word_space_divider = ' '*4

        # Convert the list of characters into list of words (which are list of
        # characters split on spaces) such that each line's words do not exceed
        # the line character limit
        lines = self._chunk_lines(
            len(char_space_divider), len(word_space_divider))

        # Convert each line into corresponding upper, middle, and lower text
        # lines for output
        elian_lines = []
        for line in lines:
            elian_lines.extend(
                self._line_to_upper_middle_lower(
                    line, word_space_divider, char_space_divider))

        return '\n'.join(elian_lines)


def cli():
    '''Parse the command line arguments'''
    parser = argparse.ArgumentParser(
        description='Generate the elian script representation'
        ' of ascii text using unicode box characters')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-t', '--text', type=str, help='the text to convert'
        ' into elian script')
    group.add_argument('-f', '--file', type=argparse.FileType('r'),
                       help='the file containing text to'
                       ' convert into elian script')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        help='a file to write the elian'
                        ' script representaion to')
    args = parser.parse_args()
    return args


def main():
    args = cli()

    if args.file:
        script = ElianScript(args.file.read())
        args.file.close()
    elif args.text:
        script = ElianScript(args.text)
    else:
        raise AttributeError('Need input of text or file to convert to elian.')

    if args.output:
        args.output.write(str(script))
        args.output.close()
    else:
        print(script)

if __name__ == '__main__':
    main()
