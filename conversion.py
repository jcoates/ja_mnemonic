"""
This file is used for converting from numbers to text and such.
"""

from typing import Dict, List, Tuple
from collections import defaultdict
from random import choice


def katakana_to_digit(k: str) -> str:
    """Given a katakana character, convert it to a digit.

    The rules are, more or less:
    アイウエオヴ - 1
    カキクケコガギグゲゴ - 2
    サシスセソザジズゼゾ - 3
    タチツテトダヂヅデド - 4
    ナニヌネノ - 5
    ハヒフヘホバビブベボパピプペポ - 6
    マミムメモ - 7
    ヤユヨ - 8
    ラリルレロ - 9
    ワンヲー - 0
    ッァィゥェォャュョ - ignored (?)

    We'll try this and also the version that uses small characters and see what happens.
    """

    if k in "アイウエオヴ":
        return "1"
    elif k in "カキクケコガギグゲゴ":
        return "2"
    elif k in "サシスセソザジズゼゾ":
        return "3"
    elif k in "タチツテトダヂヅデド":
        return "4"
    elif k in "ナニヌネノ":
        return "5"
    elif k in "ハヒフヘホバビブベボパピプペポ":
        return "6"
    elif k in "マミムメモ":
        return "7"
    elif k in "ヤユヨ":
        return "8"
    elif k in "ラリルレロ":
        return "9"
    elif k in "ワンヲー":
        return "0"
    else: # unsuspected characters, plus ッァィゥェォャュョ
        return ""

def katakana_to_digit_with_small(k: str) -> str:
    """Given a katakana character, convert it to a digit.

    The rules are, more or less:
    アイウエオヴァィゥェォ - 1
    カキクケコガギグゲゴ - 2
    サシスセソザジズゼゾ - 3
    タチツテトダヂヅデドッ - 4
    ナニヌネノ - 5
    ハヒフヘホバビブベボパピプペポ - 6
    マミムメモ - 7
    ヤユヨャュョ - 8
    ラリルレロ - 9
    ワンヲー - 0

    This is very similar to above, with _slightly_ better coverage at I think expense of memorability
    """

    if k in "アイウエオヴァィゥェォ":
        return "1"
    elif k in "カキクケコガギグゲゴ":
        return "2"
    elif k in "サシスセソザジズゼゾ":
        return "3"
    elif k in "タチツテトダヂヅデドッ":
        return "4"
    elif k in "ナニヌネノ":
        return "5"
    elif k in "ハヒフヘホバビブベボパピプペポ":
        return "6"
    elif k in "マミムメモ":
        return "7"
    elif k in "ヤユヨャュョ":
        return "8"
    elif k in "ラリルレロ":
        return "9"
    elif k in "ワンヲー":
        return "0"
    else: # unsuspected characters
        return ""

def katakana_word_to_number(カタカナ: str) -> str:
    """Given a word in katakana, convert it into a string representation of an appropriate number.
    
    See: katakana_to_digit
    """

    return "".join(katakana_to_digit(k) for k in カタカナ)

def digit_to_random_katanana(digit: str) -> str:
    """Given a string which is a digit, return a random matching katakana character

    This uses the mapping with small characters thrown in because going backwards ignoring those is harder.
    """
    if digit == "1":
        return choice(list("アイウエオヴァィゥェォ"))
    elif digit == "2":
        return choice(list("カキクケコガギグゲゴ"))
    elif digit == "3":
        return choice(list("サシスセソザジズゼゾ"))
    elif digit == "4":
        return choice(list("タチツテトダヂヅデドッ"))
    elif digit == "5":
        return choice(list("ナニヌネノ"))
    elif digit == "6":
        return choice(list("ハヒフヘホバビブベボパピプペポ"))
    elif digit == "7":
        return choice(list("マミムメモ"))
    elif digit == "8":
        return choice(list("ヤユヨャュョ"))
    elif digit == "9":
        return choice(list("ラリルレロ"))
    elif digit == "0":
        return choice(list("ワンヲー"))
    else:
        return ""


def make_up_word(i: str) -> str:
    """Given a string which is an int, return an arbitrary katakana string matching encoding."""
    return "".join(digit_to_random_katanana(d) for d in i)

    
def process_loanwords() -> Dict[int, List[Tuple[str, str]]]:
    """Processes the file in data called loanwords_garaigo_merged"""
    results = defaultdict(list)
    with open("data/loanwords_garaigo_merged.csv", 'r') as f:
        for line in f:
            (english, japanese, _) = line.split(",")
            index = katakana_word_to_number(japanese)
            results[index].append((japanese, english))
    return results

def main():
    """REPL the mnemonics"""
    print("LOADING DICTIONARY...")
    dictionary = process_loanwords()
    print("JA_MNEMONIC, ENTER NUMBERS. Q TO QUIT.")
    i = ""
    while True:
        i = input("> ")
        if i.lower() in ['q', 'exit', 'quit']: 
            break
        try:
            result = dictionary[i]
            [print("\t" + answer[0] + " - " + answer[1]) for answer in result]
            if not result:
                print("NO MATCHING WORDS FOUND. YOUR WORD WOULD BE SOMETHING LIKE: " + make_up_word(i))
        except ValueError:
            print(i + " IS NOT A NUMBER OR THE QUIT COMMAND, TRY AGAIN.")
            continue
    print("COMPLETE.")

def coverage_check():
    print("LOADING DICTIONARY...")
    dictionary = process_loanwords()
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    for i in range(0, 10):
        print(i*100)
        print("".join((OKGREEN + "O" + ENDC if str(n) in dictionary else FAIL + "X" + ENDC for n in range(i*100, (i+1)*100))))
    for i in range(0, 10):
        missing = []
        for n in range(i*100, (i+1)*100):
            if str(n) not in dictionary:
                missing.append(n)
        print("MISSING NUMBERS: " + missing)

if __name__ == '__main__':
    main()


    