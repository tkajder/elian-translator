# unicode-elian

unicode-elian is an english alphabet to elian script translator. 

[Elian script](http://www.ccelian.com/ElianScriptFull.html) is a simple block cipher assigning letters of the alphabet to fragments of a grid (similar to the [pig-pen cipher](https://en.wikipedia.org/wiki/Pigpen_cipher)). The translator takes each alphabetic character and converts it into an elian script equivalent using unicode characters and a triple-line format.

Requirements
------------
unicode-elian relies on Python 3 for unicode in the source code and the `typing` type hinting module.

Examples
--------
```bash
./elian.py --help
usage: elian.py [-h] (-t TEXT | -f FILE) [-o OUTPUT]

Generate the elian script representation of ascii text using unicode box
characters

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  the text to convert into elian script
  -f FILE, --file FILE  the file containing text to convert into elian script
  -o OUTPUT, --output OUTPUT
                        a file to write the elian script representaion to
```

```bash
./elian.py -t "hello world"
        ╷  ╷   ╷     ·╷   ╷ ╷   ╷    
╭─ ╭─╮  │  │ ╷ │    ╭─┤ ╷ │ │   │ ╭─╮
╰─ ╰─╯ ─╯ ─╯ ╰─╯    ╰─╯ ╰─╯ ╰─ ─╯ ╵ ╵
```

```bash
# The contents of notes.txt are "welcome to new york".
./elian.py -f notes.txt 
 ·╷      ╷      ╷ ╭─╮        ─╮   ╷      ╷      ·╷
╭─┤ ╭─╮  │  ╷ ╷ │ │ ╵ ╭─╮    ·│ ╷ │    ╭─┤ ╭─╮ ╭─┤
╰─╯ ╰─╯ ─╯ ─╯ ╰─╯ ╵   ╰─╯    ─╯ ╰─╯    ╰─╯ ╰─╯ ╰─╯
╭─   ╷ ╷  ─╮
│· ╷ │ │   │
╵  ╰─╯ ╰─ ─╯
```

Notes
-----
For readability output is wrapped to a default of 70 characters, with 1 space between characters in words, and 4 spaces between words in a line. These defaults can be changed in the underlying class functions.

There is no formal definition of punctuation in the Elian script standard and none is defined here. 
