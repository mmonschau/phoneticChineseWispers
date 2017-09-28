# coding=utf-8
import jellyfish


# switched levensthein to similarity metric
def calc_similarity(w1, w2):
    """

    :param w1:
    :param w2:
    :return:
    """
    return 1 - (jellyfish.levenshtein_distance(w1, w2) / float(max([len(w1), len(w2)])))
