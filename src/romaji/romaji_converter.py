"""
A program that takes a name (or a single word in general) in romaji, and converts it to hiragana.
"""

SOKUON = 'xtsu'

def romaji_standardization(word: str) -> str:
    """This mostly makes nihon-shiki into hepburn, which is a loss of info technically."""

    res = ""
    arr_word = list(word.lower())
    i = 0
    while i < len(arr_word):
        match arr_word[i:]:
            case ['s', 'i', *rest]:
                res += "shi"
                i += 2
            case ['t', 'u', *rest]:
                res += "tsu"
                i += 2
            case ['t', 'i', *rest]:
                res += "chi"
                i += 2
            case ['h', 'u', *rest]:
                res += "fu"
                i += 2
            case ['z', 'i', *rest]:
                res += "ji"
                i += 2
            case ['d', 'z', *rest]:
                res += 'd'
                i += 2
            case ['z', 'y', *rest]:
                res += "j"
                i += 2
            case ['j', 'y', *rest]:
                res += "j"
                i += 2
            case ['s', 'y', *rest]:
                res += "sh"
                i += 2
            case ['t', 'y', *rest]:
                res += "ch"
                i += 2
            case ['ô', *rest]:
                res += "ou"
                i += 1
            case ['ō', *rest]:
                res += "ou"
                i += 1
            case ['û', *rest]:
                res += "uu"
                i += 1
            case ['ū', *rest]:
                res += "uu"
                i += 1
            case [c, peek, *rest] if c == 'm' and peek not in ['a', 'e', 'i', 'o', 'u', 'y']:
                res += 'n'
                i += 1
            case _:
                res += arr_word[i]
                i += 1
    return res

def romaji_to_hiragana(word: str) -> str:
    """Given some romaji, turns it into hiragana"""
    clean = romaji_standardization(word)
    arr_clean = list(clean)
    i = 0
    by_char = []
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    CONSONANTS = ['k', 's', 't', 'n', 'h', 'f', 'v', 'm', 'y', 'r', 'g', 'z', 'j', 'z', 'd', 'b', 'p']
    while i < len(arr_clean):
        match arr_clean[i:]:
            case [vowel, *rest] if vowel in VOWELS:
                by_char.append(vowel)
                i += 1
            case ['c','h',vowel,*rest]:
                by_char.append("ch" + vowel)
                i += 3
            case ['s','h',vowel,*rest]:
                by_char.append("sh" + vowel)
                i += 3
            case ['t','s','u',*rest]:
                by_char.append("tsu")
                i += 3
            case ['n', "'",*rest]:
                by_char.append('n')
                i += 2
            case [consonant, 'y', vowel, *rest] if consonant in CONSONANTS and vowel in VOWELS:
                by_char.append(consonant + 'y' + vowel)
                i += 3
            case [consonant, vowel, *rest] if consonant in CONSONANTS and vowel in VOWELS:
                by_char.append(consonant + vowel)
                i += 2
            case [c1, c2, *rest] if c1 in CONSONANTS and c1 == c2:
                by_char.append(SOKUON)
                i += 1
            case ['n', *rest]:
                by_char.append('n')
                i += 1
            case c:
                raise ValueError(f"can not turn {word} into kana at position {i}")
    res = ""
    for c in by_char:
        res += char_to_hiragana(c)
    return res

def char_to_hiragana(c: str) -> str:
    lookup = {
        "a": "あ",  "i": "い", 	"u": "う", 	"e": "え", 	"o": "お",
        "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",   "kya":"きゃ", 	  "kyu":"きゅ", 	  "kyo":"きょ",
        "sa":"さ",  "shi":"し", "su":"す", 	"se":"せ", 	"so":"そ", 	  "sha":"しゃ", 	  "shu":"しゅ", 	  "sho":"しょ",
        "ta":"た", 	"chi":"ち", "tsu":"つ", "te":"て", 	"to":"と", 	  "cha":"ちゃ", 	  "chu":"ちゅ", 	  "cho":"ちょ",
        "na":"な", 	"ni":"に", 	"nu":"ぬ", 	"ne":"ね", 	"no":"の", 	  "nya":"にゃ", 	  "nyu":"にゅ", 	  "nyo":"にょ",
        "ha":"は", 	"hi":"ひ", 	"fu":"ふ", 	"he":"へ", 	"ho":"ほ", 	  "hya":"ひゃ", 	  "hyu":"ひゅ", 	  "hyo":"ひょ",
        "ma":"ま", 	"mi":"み", 	"mu":"む", 	"me":"め", 	"mo":"も", 	  "mya":"みゃ", 	  "myu":"みゅ", 	  "myo":"みょ",
        "ya":"や", 	            "yu":"ゆ", 		        "yo":"よ",
        "ra":"ら", 	"ri":"り", 	"ru":"る" ,	"re":"れ" ,	"ro":"ろ", 	  "rya":"りゃ", 	  "ryu":"りゅ", 	  "ryo":"りょ",
        "wa":"わ", 	 	                               "wo":"を",
	    "n": "ん",
        "ga":"が", 	"gi":"ぎ", 	"gu":"ぐ", 	"ge":"げ", 	"go":"ご", 	  "gya":"ぎゃ", 	  "gyu":"ぎゅ", 	  "gyo":"ぎょ",
        "za":"ざ", 	"ji":"じ", 	"zu":"ず", 	"ze":"ぜ", 	"zo":"ぞ", 	  "ja":"じゃ", 	      "ju":"じゅ", 	      "jo":"じょ",
        # The ぢ characters are all basically unrecoverable in this romanization
        "da":"だ", 	"di":"ぢ", 	"zu":"づ", 	"de":"で", 	"do":"ど", 	  "dya":"ぢゃ", 	  "dyu":"ぢゅ",       "dyo":"ぢょ",
        "ba":"ば", 	"bi":"び", 	"bu":"ぶ", 	"be":"べ", 	"bo":"ぼ", 	  "bya":"びゃ", 	  "byu":"びゅ", 	  "byo":"びょ",
        "pa":"ぱ", 	"pi":"ぴ", 	"pu":"ぷ", 	"pe":"ぺ", 	"po":"ぽ", 	  "pya":"ぴゃ", 	  "pyu":"ぴゅ", 	  "pyo":"ぴょ",
        SOKUON: "っ",
        "va": "ゔぁ", "vi":"ゔぃ", "vu": "ゔ", "ve": "ゔぇ", "vo":"ゔぉ",
        "dzu":"づ",
    }
    return lookup[c]