"""
This file is used for converting from numbers to text and vice versa.
"""

from typing import List, Optional

from mnemonic.kana_mapper import digit_to_random_katakana
from mnemonic.loaders import process_jmdict, process_jmnedict_names, process_jmnedict_other, process_loanwords, process_wiki_names
from mnemonic.tenkeydict import TenKeyDict

class Converter():

    def __init__(self, words: TenKeyDict=TenKeyDict(), surnames: TenKeyDict=TenKeyDict(), given_names: TenKeyDict=TenKeyDict()):
        self.words = words
        self.surnames = surnames
        self.given_names = given_names

    @staticmethod
    def build_default():
        """A factory method that just always loads the "expected" set of dictionaries."""
        wiki_surnames, wiki_given_names = process_wiki_names()
        jmne_surnames, jmne_given_names = process_jmnedict_names()
        loanwords_dict = process_loanwords()
        jmdict = process_jmdict()
        jmnedict = process_jmnedict_other()
        surnames = TenKeyDict.merge_dicts(wiki_surnames, jmne_surnames)
        given_names = TenKeyDict.merge_dicts(wiki_given_names, jmne_given_names)
        words = TenKeyDict.merge_dicts(loanwords_dict, jmdict, jmnedict)
        return Converter(words,surnames,given_names)

    def find_any_name(self, number: str) -> Optional[str]:
        """Given a number, try to return a name for it.

        We'll try to match the number to a name. Surname or Given.
        Then we'll try every length split we can to make it from a
        surname followed by a given name.
        """
        if number in self.given_names:
            return self.given_names[number][0]
        if number in self.surnames:
            return self.surnames[number][0]
        for i in range(1, len(number)):
            sur = number[:i]
            giv = number[i:]
            if sur in self.surnames and giv in self.given_names:
                return self.surnames[sur][0]+" "+self.given_names[giv][0]
        return None

    def find_any_option(self, n: str) -> Optional[str]:
        """Tries to see if we can get any matches for a number.

        First we'll try the dictionary. Then the names. If we get nothing we return nothing.

        Currently, this just returns results in order by words>given names>surnames> combos > Nothing. We have no sense of frequency.

        TODO: Add a frequency?
        """
        if n in self.words:
            return self.words[n][0]

        return self.find_any_name(n)

    def find_all_names(self, number: str) -> List[str]:
        """Given a number, try to return all names for it.

        We'll try to match the number to a name. Surname or Given.
        Then we'll try every length split we can to make it from a
        surname followed by a given name.
        """
        results = []
        if number in self.given_names:
            results.extend(g for g in self.given_names[number])
        if number in self.surnames:
            results.extend(s for s in self.surnames[number])
        for i in range(1, len(number)):
            sur = number[:i]
            giv = number[i:]
            if sur in self.surnames and giv in self.given_names:
                for s in self.surnames[sur]:
                    for g in self.given_names[giv]:
                        new_name = s+" "+g
                        if new_name not in results:
                            results.append(new_name)
        return results

    def find_all_options(self, n) -> List[str]:
        """Finds all the matches for a number.

        First we'll try the dictionary. Then the names. If we get nothing we return nothing.

        Currently, this just returns results in order by words>given names>surnames> combos. We have no sense of frequency.

        TODO: Add a frequency
        """
        results = []
        if n in self.words:
            results.extend(self.words[n])
        results.extend(self.find_all_names(n))
        return results

    @staticmethod
    def make_up_word(i: str) -> str:
        """Given a string which is an int, return an arbitrary katakana string matching encoding."""
        return "".join(digit_to_random_katakana(d) for d in i)
