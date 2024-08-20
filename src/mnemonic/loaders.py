"""Here is all our methods for loading dictionaries from csvs, data files, etc."""

from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from mnemonic.kana_mapper import kana_word_to_number
from mnemonic.tenkeydict import TenKeyDict


DATA_DIR = Path(__file__).parent.parent.parent / "data"

def process(file: str, line_to_kana: Callable[[str], str]) -> TenKeyDict:
    """Processes a file into a TenKeyDict

    Given a file and a way to turn a line of that file into kana, makes it into a TenKeyDict.
    """
    results = defaultdict(list)
    with open(DATA_DIR / file, 'r') as f:
        for line in f:
            kana = line_to_kana(line)
            index = kana_word_to_number(kana)
            if kana not in results[index]:
                results[index].append(kana)
    return TenKeyDict(results)

def process_loanwords() -> TenKeyDict:
    """Processes the file in data called loanwords_garaigo_merged

    file looks like: (third column always empty)
    TOBACCO,タバコ,
    """
    #NB: The longest word is 45 characters long
    return process("loanwords_garaigo_merged.csv", lambda x: x.strip().split(',')[1])

def process_jmdict() -> TenKeyDict:
    """Processes the file in data called jmdict_reading_list.txt

    Unlike the one above, this one doesn't have translations. It could, it
    comes from an xml file with them, but I wasn't using the definitions.

    File is a single kana reading per line


    TODO: Consider some means of ranking the words with the same number by popularity?
    """
    # NB: longest word is 37 characters long
    return process("jmdict_reading_list.txt", lambda x: x.strip())

def process_jmnedict_names() -> Tuple[TenKeyDict, TenKeyDict]:
    """Parses two jmnedict name exports into two dictionaries.

    Returns: (LastNameDict, FirstNameDict)

    file looks like:
    あしなの,芦奈野,Ashinano
    まさし,方志,Masashi

    The idea is to be able to split a number into a last name and a first name
    """
    # NB: Longest Surname was 23 characters long
    surnames = process("jmnedict_surnames.csv", lambda x: x.strip().split(',')[0])
    # NB: Longest Given Name was 13 characters long
    given_names = process("jmnedict_given_names.csv", lambda x: x.strip().split(',')[0])
    return (surnames,given_names)

def process_jmnedict_other() -> TenKeyDict:
    """Processes the file in data called jmnedict_other_names.csv

    This is other names, like companies, places, etc.

    Format looks like:
    まるた,丸太,Maruta
    """
    #NB: The longest word in this is 33 characters long
    return process("jmnedict_other_names.csv", lambda x: x.strip().split(',')[0])

def process_wiki_names() -> Tuple[TenKeyDict, TenKeyDict]:
    """Parses two wiki name exports into two dictionaries.

    Returns: (LastNameDict, FirstNameDict)

    The idea is to be able to split a number into a last name and a first name.

    The File Format looks like:
    Sumeragi,皇,すめらぎ
    Naomi,直実,なおみ
    """
    surnames = defaultdict(list)
    # NB: Longest Surname was 9 characters long
    surnames = process("wiki_surnames_clean.csv", lambda x: x.strip().split(',')[2])
    # NB: Longest Given Name was 8 characters long
    given_names = process("wiki_given_names_clean.csv", lambda x: x.strip().split(',')[2])
    return (surnames,given_names)
