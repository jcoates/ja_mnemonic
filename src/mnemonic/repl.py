"""
This file is used for converting from numbers to text in a repl way.
"""

from random import choice
from conversion import num_to_options, process_jmdict, process_loanwords, process_wiki_names

def digit_to_random_katakana(digit: str) -> str:
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
    return "".join(digit_to_random_katakana(d) for d in i)

def main():
    """REPL the mnemonics"""
    print("LOADING DICTIONARY...")
    surnames, given_names = process_wiki_names()
    loanwords_dict = process_loanwords()
    jmdict = process_jmdict()
    empty = []
    words_dict = {k:[l[0] for l in loanwords_dict.get(k, empty)] + jmdict.get(k, empty) for k in set(loanwords_dict.keys()).union(jmdict.keys())}
    def get_options(n):
        return num_to_options(n, words_dict, surnames, given_names)

    print("JA_MNEMONIC, ENTER NUMBERS. Q TO QUIT.")
    i = ""
    while True:
        i = input("> ")
        if i.lower() in ['q', 'exit', 'quit']: 
            break
        try:
            result = get_options(i)
            # [print("\t" + answer[0] + " - " + answer[1]) for answer in result]
            if len(result) > 10:
                result = result[0:5] + result[-5:]
            print(f"[{','.join(a for a in result)}]")
            if not result:
                print("NO MATCHING WORDS FOUND. YOUR WORD WOULD BE SOMETHING LIKE: " + make_up_word(i))
        except ValueError:
            print(i + " IS NOT A NUMBER OR THE QUIT COMMAND, TRY AGAIN.")
            continue
    print("COMPLETE.")

if __name__ == '__main__':
    main()
