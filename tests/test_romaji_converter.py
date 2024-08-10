import pytest
from romaji.romaji_converter import romaji_standardization, romaji_to_hiragana


@pytest.mark.parametrize("test_input,expected", [
    ("rômazi", "roumaji"), 
    ("Huzisan", "fujisan"), 
    ("otya", "ocha"),
    ("tizi", "chiji"),
    ("tuzuku", "tsuzuku"),
    ("kudzu", "kudu"),
    ("rōmaji", "roumaji"),
    ("Gumma", "gunma"),
    ("Shimbashi","shinbashi"),
    ("Syôzyôkôkantyô", "shoujoukoukanchou"),
    ("Jyousuke", "jousuke")
])
def test_romaji_normalizer(test_input,expected):
    res = romaji_standardization(test_input)
    assert res == expected


@pytest.mark.parametrize("test_input, expected",[
    ("Yūji", "ゆうじ"),
    ("Seiichi", "せいいち"),
    ("Ichirō","いちろう"),
    ("Jun'ichi", "じゅんいち"),
    ("Kōzō", "こうぞう"),
    ("Atsushi", "あつし"),
    ("Kyōko", "きょうこ")
])
def test_romaji_to_hiragana(test_input, expected):
    res = romaji_to_hiragana(test_input)
    assert res == expected