"""
A program that takes a name (or a single word in general) in romaji, and converts it to hiragana.
"""

SOKUON = 'xtsu'

def romaji_standardization(word: str) -> str:
    """This mostly makes nihon-shiki into hepburn, which is a loss of info technically."""

    res = ""
    lowered = word.lower()
    i = 0
    m_swaps = ['mm', 'mb', 'mp']
    two_swaps = {
        "si":"shi", "tu":"tsu", "ti":"chi", "hu":"fu", "zi":"ji",
        "dz":"d", "zy":"j", "jy":"j", "sy":"sh", "ty":"ch",
        "oh":"ou", # this is a long vowel but it's two letters long
        "sh":"sh" # this is to prevent making shu->sfu
    }
    # Technically ō could mean oo but we can't know that in this direction
    long_vowels = {
        "ō": "ou", "ô": "ou", "ū": "uu", "û": "uu", "ē": "ee", "ê":"ee",
        "ā": "aa", "â": "aa", "ī": "ii", "î":"ii" # I've never seen these used in names but for completeness sake
    }
    while i < len(lowered):
        if i+1 < len(lowered):
            first_two = lowered[i:i+2]
            if first_two in m_swaps:
                res += 'n'
                i += 1
                continue
            if first_two in two_swaps:
                res += two_swaps[first_two]
                i += 2
                continue
        if lowered[i] in long_vowels:
            res += long_vowels[lowered[i]]
        else:
            res += lowered[i]
        i += 1
    return res

def romaji_to_hiragana(word: str) -> str:
    """Given some romaji, turns it into hiragana"""
    clean = romaji_standardization(word)
    arr_clean = list(clean)
    i = 0
    by_char = []
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    CONSONANTS = ['k', 's', 't', 'n', 'h', 'f', 'v', 'm', 'y', 'r', 'g', 'z', 'j', 'z', 'd', 'b', 'p', 'w']
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