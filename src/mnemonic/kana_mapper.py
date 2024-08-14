"""This includes the methods which map between kana and digits."""

from random import choice


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

def digit_to_random_katakana(digit: str) -> str:
    """Given a string which is a digit, return a random matching katakana character

    This uses the mapping without small characters thrown in because the logic for using those
    and maintaing reasonable word shape is harder than pure random and this isn't for anything really.
    """
    if digit == "1":
        return choice(list("アイウエオヴ"))
    elif digit == "2":
        return choice(list("カキクケコガギグゲゴ"))
    elif digit == "3":
        return choice(list("サシスセソザジズゼゾ"))
    elif digit == "4":
        return choice(list("タチツテトダヂヅデド"))
    elif digit == "5":
        return choice(list("ナニヌネノ"))
    elif digit == "6":
        return choice(list("ハヒフヘホバビブベボパピプペポ"))
    elif digit == "7":
        return choice(list("マミムメモ"))
    elif digit == "8":
        return choice(list("ヤユヨ"))
    elif digit == "9":
        return choice(list("ラリルレロ"))
    elif digit == "0":
        return choice(list("ワンヲー"))
    else:
        return ""