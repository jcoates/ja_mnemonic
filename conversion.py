"""
This file is used for converting from numbers to text and such.
"""

from typing import Dict, List, Tuple
from collections import defaultdict


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


def katakana_word_to_number(カタカナ: str) -> str:
    """Given a word in katakana, convert it into a string representation of an appropriate number.
    
    See: katakana_to_digit
    """

    return "".join(katakana_to_digit(k) for k in カタカナ)
    
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
        except ValueError:
            print(i + " IS NOT A NUMBER OR THE QUIT COMMAND, TRY AGAIN.")
            continue
    print("COMPLETE.")

if __name__ == '__main__':
    main()


    