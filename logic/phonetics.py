# coding=utf-8
import re

import jellyfish


def normalizeWord(word):
    """

    :param word:
    :return:
    """
    return re.sub("[^\w]", "", word.upper()).strip()


def encPhone(english_word):
    """

    :param english_word:
    :return:
    """
    english_word = normalizeWord(english_word)
    # print(english_word)
    encoded = {'origin': english_word, 'metaphone': jellyfish.metaphone(english_word),
               'soundex': jellyfish.soundex(english_word), 'nysiis': jellyfish.nysiis(english_word),
               'match_rating_codex': jellyfish.match_rating_codex(english_word)}
    return encoded


def encPhonePerWord(english_sentence):
    """

    :param english_sentence:
    :return:
    """
    words = list(map(normalizeWord, english_sentence.split()))
    encoded = {'origin': " ".join(words)}
    encoded['metaphone'] = " ".join(map(jellyfish.metaphone, words))
    encoded['soundex'] = " ".join(map(jellyfish.soundex, words))
    encoded['nysiis'] = " ".join(map(jellyfish.nysiis, words))
    encoded['match_rating_codex'] = " ".join(map(jellyfish.match_rating_codex, words))
    return encoded


def encPhoneVariants(english_sth):
    """

    :param english_sth:
    :return:
    """
    e1 = encPhone(english_sth)
    e2 = encPhonePerWord(english_sth)
    result = {}
    for k, v in e1.items():
        result["full_" + k] = v
    for k, v in e2.items():
        result["per_word_" + k] = v
    return result
