"""
This file is used for converting from numbers to text and vice versa.
"""

from typing import Dict, List, Tuple
from collections import defaultdict

def kana_to_digit(k: str) -> str:
    """Given a kana character, convert it to a digit.

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

    if k in "アイウエオヴあいうえおゔ":
        return "1"
    elif k in "カキクケコガギグゲゴかきくけこがぎぐげご":
        return "2"
    elif k in "サシスセソザジズゼゾさしすせそざじずぜぞ":
        return "3"
    elif k in "タチツテトダヂヅデドたちつてとだぢづでど":
        return "4"
    elif k in "ナニヌネノなにぬねの":
        return "5"
    elif k in "ハヒフヘホバビブベボパピプペポはひふへほばびぶべぼぱぴぷぺぽ":
        return "6"
    elif k in "マミムメモまみむめも":
        return "7"
    elif k in "ヤユヨやゆよ":
        return "8"
    elif k in "ラリルレロらりるれろ":
        return "9"
    elif k in "ワンヲーわんを":
        return "0"
    else: # unsuspected characters, plus ッァィゥェォャュョっぁぃぅぇぉゃゅょ
        return ""

def kana_to_digit_with_small(k: str) -> str:
    """Given a kana character, convert it to a digit.

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

    if k in "アイウエオヴァィゥェォあいうえおゔぁぃぅぇぉ":
        return "1"
    elif k in "カキクケコガギグゲゴ":
        return "2"
    elif k in "サシスセソザジズゼゾさしすせそざじずぜぞ":
        return "3"
    elif k in "タチツテトダヂヅデドッたちつてとだぢづでどっ":
        return "4"
    elif k in "ナニヌネノなにぬねの":
        return "5"
    elif k in "ハヒフヘホバビブベボパピプペポはひふへほばびぶべぼぱぴぷぺぽ":
        return "6"
    elif k in "マミムメモまみむめも":
        return "7"
    elif k in "ヤユヨャュョやゆよゃゅょ":
        return "8"
    elif k in "ラリルレロらりるれろ":
        return "9"
    elif k in "ワンヲーわんを":
        return "0"
    else: # unsuspected characters
        return ""

def kana_word_to_number(カタカナ: str) -> str:
    """Given a word in kana, convert it into a string representation of an appropriate number.

    See: kana_to_digit
    """

    return "".join(kana_to_digit(k) for k in カタカナ)

def process_loanwords() -> Dict[int, List[Tuple[str, str]]]:
    """Processes the file in data called loanwords_garaigo_merged"""
    results = defaultdict(list)
    with open("data/loanwords_garaigo_merged.csv", 'r') as f:
        for line in f:
            (english, japanese, _) = line.split(",")
            index = kana_word_to_number(japanese)
            results[index].append((japanese, english))
    return results

def process_jmdict() -> Dict[int, List[str]]:
    """Processes the file in data called jmdict_reading_list.txt

    Unlike the one above, this one doesn't have translations. It could, it
    comes from an xml file with them, but I wasn't using the definitions.

    TODO: Consider some means of ranking the words with the same number by popularity?
    """

    results = defaultdict(list)
    with open("data/jmdict_reading_list.txt", 'r') as f:
        for line in f:
            word = line.strip()
            index = kana_word_to_number(word)
            results[index].append(word)
        return results
