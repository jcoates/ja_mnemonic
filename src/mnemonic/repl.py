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
            results = []
            options = converter.find_all_options(i)
            for l in [options.words, options.given_names, options.surnames, options.full_names]:
                if len(l) > 5:
                    results.extend(l[0:3])
                    results.extend(l[-3:])
            print(f"[{','.join(a for a in results)}]")
            if not results:
                print("NO MATCHING WORDS FOUND. YOUR WORD WOULD BE SOMETHING LIKE: " + converter.make_up_word(i))
        except ValueError:
            print(i + " IS NOT A NUMBER OR THE QUIT COMMAND, TRY AGAIN.")
            continue
    print("COMPLETE.")

if __name__ == '__main__':
    main()
