"""
This file is used for converting from numbers to text and vice versa.
"""

from typing import Dict, List, Tuple
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"



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
    with open(DATA_DIR / "loanwords_garaigo_merged.csv", 'r') as f:
        for line in f:
            (english, japanese, _) = line.strip().split(",")
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
    with open(DATA_DIR / "jmdict_reading_list.txt", 'r') as f:
        for line in f:
            word = line.strip()
            index = kana_word_to_number(word)
            results[index].append(word)
        return results

def process_wiki_names() -> Tuple[Dict[int, List[str]], Dict[int, List[str]]]:
    """Parses two wiki name exports into two dictionaries.

    Returns: (LastNameDict, FirstNameDict)

    The idea is to be able to split a number into a last name and a first name
    """
    surnames = defaultdict(list)
    # NB: Longest Surname was 9 characters long
    with open(DATA_DIR / "wiki_surnames_clean.csv", 'r') as f:
        for line in f:
            (english, _kanji, kana) = line.strip().split(",")
            index = kana_word_to_number(kana)
            surnames[index].append((kana, english))
    given_names = defaultdict(list)
    # NB: Longest Given Name was 8 characters long
    with open(DATA_DIR / "wiki_given_names_clean.csv", 'r') as f:
        for line in f:
            (english, _kanji, kana) = line.strip().split(",")
            index = kana_word_to_number(kana)
            given_names[index].append((kana, english))
    return (surnames,given_names)

def num_to_name(number: str, surnames: Dict[str, List[str]], given_names: Dict[str, List[str]]) -> List[str]:
    """Given a number, try to return a name for it.

    We'll try to match the number to a name. Surname or Given.
    Then we'll try every length split we can to make it from a
    surname followed by a given name.
    """
    results = []
    if number in given_names:
        results.extend(g[0] for g in given_names[number])
    if number in surnames:
        results.extend(s[0] for s in surnames[number])
    for i in range(1, len(number)):
        sur = number[:i]
        giv = number[i:]
        if sur in surnames and giv in given_names:
            for s in surnames[sur]:
                for g in given_names[giv]:
                    new_name = s[0]+" "+g[0]
                    if new_name not in results:
                        results.append(new_name)
    return results

def num_to_options(n, words_dict: Dict[str, List[str]], surnames: Dict[str, List[str]], given_names: Dict[str, List[str]]) -> List[str]:
    """Tries to see if we can get any matches for a number.

    First we'll try the dictionary. Then the names. If we get nothing we return nothing.

    Currently, this just returns results in order by words>given names>surnames> combos. We have no sense of frequency.

    TODO: Add a frequency? Add a way to generate a bogus japanese word.
    """
    results = []
    if n in words_dict:
        results.extend(words_dict[n])
    results.extend(num_to_name(n, surnames, given_names))
    return results