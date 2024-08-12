"""
This file is for checking what coverage my dictionary has over the numbers I might want to remember
"""

from conversion import num_to_options, process_loanwords, process_jmdict, process_wiki_names

"""
Some Coverage Records:
1 digits: 100%
2 digits: 100%
3 digits: ~88%~ -> 96.8 (0-filled)
4 digits: ~68%~ -> 86.84% (0-filled)
5 digits: 65.67% (0-filled)
6 digits: 36.47% (0-filled)
7 digits: 11.13% (0-filled)
"""

def coverage_check():
    print("LOADING DICTIONARIES...")
    surnames, given_names = process_wiki_names()
    loanwords_dict = process_loanwords()
    jmdict = process_jmdict()
    empty = []
    words_dict = {k:[l[0] for l in loanwords_dict.get(k, empty)] + jmdict.get(k, empty) for k in set(loanwords_dict.keys()).union(jmdict.keys())}
    def get_options(n):
        return num_to_options(n, words_dict, surnames, given_names)
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    total = 10000000
    bucket_size = 250
    print(f"Coverage of names")
    m_count = 0
    missings = []
    for i in range(0, int(total/bucket_size)):
        missing = []
        print(i*bucket_size)
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
        # print(f"MISSING NUMBERS: [{','.join(str (n) for n in m)}]")
        m_count += len(m)
    print(f"COVERAGE: ({total-m_count}/{total}) {((total-m_count)/total)*100}%")

if __name__ == '__main__':
    coverage_check()
