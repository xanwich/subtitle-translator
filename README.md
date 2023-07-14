# subtitle-translator

Live translation with screen capture and OCR for translating subtitles. Every specified number of seconds, it will take a picture of part of your screen, scan for words on it, and translate those into a language of your choice. This is really a proof of concept program - the OCR is not dialed in and will often gives semi-nonsensical results in addition to the real text if the window size is too large, and this technology exists (for example in google translate on mobile) but I couldn't find anything quite like it for desktop. I built this so I could watch the TV show ["Danmarks næste klassiker"](https://www.dr.dk/drtv/saeson/danmarks-naeste-klassiker_83127) with English subtitles.

## Installation

Make sure you have `python 3.10` and `pip` installed. Then run `pip install requirements.txt`.
If you want to translate from languages other than English, install Tesseract's other languages with instructions [here](https://tesseract-ocr.github.io/tessdoc/Installation.html) or by running `brew install tesseract-lang` on mac OSX.

## Usage

Currently this program uses the [translate](https://github.com/terryyin/translate-python) package, which requires internet access to make translations. Likely in the future this will be swapped out for an offline translation method.

```
usage: python subtitle_translator.py [-h] [-f {en,da,de,es}] [-t {en,da,de,es}] [-w WAIT_TIME]

Live translation with screen capture and OCR

options:
  -h, --help            show this help message and exit
  -f {en,da,de,es}, --from-lang {en,da,de,es}
                        Two-letter language code of origin language (default 'da')
  -t {en,da,de,es}, --to-lang {en,da,de,es}
                        Two-letter language code of desired result languagen (default 'en')
  -w WAIT_TIME, --wait-time WAIT_TIME
                        Time in seconds to wait between screen captures (default 3)
```

### Quitting

Right now there's no "exit" button, so you just have to press `cmd-q` to quit the program :disappointed:.
