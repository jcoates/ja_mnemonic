"""This file is to clean up some data in the wikinames exports."""

from pathlib import Path
from romaji.romaji_converter import romaji_to_hiragana


NOT_FOUND = "<not found>"
DATA_DIR = Path(__file__).parent.parent.parent / "data"

def replace_no_results(file_in, file_out):
    with open(file_in, 'r') as f_in:
        with open(file_out, 'w') as f_out:
            for line in f_in.readlines():
                elems = line.strip().split(',')
                if elems[2] == NOT_FOUND:
                    kana = romaji_to_hiragana(elems[0])
                    elems[2] = kana
                new_line = ','.join(elems)
                f_out.write(new_line + '\n')

def main():
    replace_no_results(DATA_DIR / 'wiki_surnames.csv', DATA_DIR / 'wiki_surnames_2.csv')
    replace_no_results(DATA_DIR / 'wiki_given_names.csv', DATA_DIR / 'wiki_given_names_2.csv')

if __name__ == '__main__':
    main()
