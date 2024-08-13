"""
This file is for checking what coverage my dictionary has over the numbers I might want to remember
"""

from typing import Dict, List
from conversion import num_to_any_option, process_jmnedict_names, process_jmnedict_other, process_loanwords, process_jmdict, process_wiki_names

"""
Some Coverage Records:
1 digits: 100%
2 digits: 100%
3 digits: ~88%~ -> ~96.80%~ -> 100%
4 digits: ~68%~ -> ~86.84%~ -> 99.98% [missing only 9585,9588]
5 digits: 65.67% -> 98.83%
6 digits: 36.47% -> 91.13%
7 digits: 11.13% -> 65.39%
8 digits: 22.96% [this took around 3 minutes to run]
9 digits: 2.88% [Also this took nearly half an hour]
"""

def merge_dicts(*dicts: Dict[str, List[str]]) -> Dict[str, str]:
    """A helper that combines dictionaries of strings to lists of string."""
    keys = set()
    for d in dicts:
        keys = keys.union(d.keys())
    r = {}
    empty = []
    for k in keys:
        l = []
        for d in dicts:
            l += d.get(k, empty)
        r[k] = l
    return r

def coverage_check():
    print("LOADING DICTIONARIES...")
    wiki_surnames, wiki_given_names = process_wiki_names()
    jmne_surnames, jmne_given_names = process_jmnedict_names()
    loanwords_dict = process_loanwords()
    jmdict = process_jmdict()
    jmnedict = process_jmnedict_other()
    surnames = merge_dicts(wiki_surnames, jmne_surnames)
    given_names = merge_dicts(wiki_given_names, jmne_given_names)
    words_dict = merge_dicts(loanwords_dict, jmdict, jmnedict)
    def get_options(n):
        return num_to_any_option(n, words_dict, surnames, given_names)
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    total = 10000
    bucket_size = 200
    m_count = 0
    missings = []
    print("Checking Coverage...")
    for i in range(0, int(total/bucket_size)):
        missing = []
        print("["+str(i*bucket_size).zfill(len(str(total))-1)+"]", end='')
        s = ""
        for n in range(i*bucket_size, (i+1)*bucket_size):
            options = get_options(str(n).zfill(len(str(total))-1))
            if options:
                s += OKGREEN + "O" + ENDC
            else:
                s += FAIL + "X" + ENDC
                missing.append(n)
        print(s)
        missings.append(missing)
    for m in missings:
        if len(m) > 0:
            print(f"MISSING NUMBERS: [{','.join(str (n) for n in m)}]")
        m_count += len(m)
    print(f"COVERAGE: ({total-m_count}/{total}) {((total-m_count)/total)*100}%")

if __name__ == '__main__':
    coverage_check()
