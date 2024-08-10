"""
This file is for checking what coverage my dictionary has over the numbers I might want to remember
"""

from conversion import process_loanwords, process_jmdict

def coverage_check():
    print("LOADING DICTIONARY...")
    d1 = process_loanwords()
    d2 = process_jmdict()
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    total = 1000
    bucket_size = 100
    for dictionary, name in [(d1, "loan words"), (d2, "jmdict")]:
        print(f"Coverage of {name}")
        m_count = 0
        for i in range(0, (total/bucket_size)):
            print(i*bucket_size)
            print("".join((OKGREEN + "O" + ENDC if str(n) in dictionary else FAIL + "X" + ENDC for n in range(i*bucket_size, (i+1)*bucket_size))))
        for i in range(0, (total/bucket_size)):
            missing = []
            for n in range(i*bucket_size, (i+1)*bucket_size):
                if str(n) not in dictionary:
                    missing.append(n)
            print(f"MISSING NUMBERS: [{','.join(str (n) for n in missing)}]")
            m_count += len(missing)
        print(f"COVERAGE: ({total-m_count}/{total}) {((total-m_count)/total)*100}%")

if __name__ == '__main__':
    coverage_check()
