"""
This file is for checking what coverage my dictionary has over the numbers one might want to remember
"""

from mnemonic.conversion import Converter

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

def coverage_check():
    print("LOADING DICTIONARIES...")
    converter = Converter.build_default()
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
            maybe_name = converter.find_any_option(str(n).zfill(len(str(total))-1))
            if maybe_name:
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
