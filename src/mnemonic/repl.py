"""
This file is used for converting from numbers to text in a repl way.
"""

from mnemonic.conversion import Converter


def main():
    """REPL the mnemonics"""
    print("LOADING DICTIONARIES...")
    converter = Converter.build_default()

    print("JA_MNEMONIC, ENTER NUMBERS. Q TO QUIT.")
    i = ""
    while True:
        i = input("> ")
        if i.lower() in ['q', 'exit', 'quit']:
            break
        try:
            if not i.isdigit():
                raise ValueError()
            result = converter.find_all_options(i)
            if len(result) > 10:
                result = result[0:5] + result[-5:]
            print(f"[{','.join(a for a in result)}]")
            if not result:
                print("NO MATCHING WORDS FOUND. YOUR WORD WOULD BE SOMETHING LIKE: " + converter.make_up_word(i))
        except ValueError:
            print(i + " IS NOT A NUMBER OR THE QUIT COMMAND, TRY AGAIN.")
            continue
    print("COMPLETE.")

if __name__ == '__main__':
    main()
