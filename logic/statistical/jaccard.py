# coding=utf-8


def calc_similarity(w1, w2):
    """

    :param w1:
    :param w2:
    :return:
    """
    return jaccard(w1, w2)


def jaccard(word1, word2):
    """

    :param word1:
    :param word2:
    :return:
    """
    l1 = set(word1.split())
    l2 = set(word2.split())
    return len(l1.intersection(l2)) / float(len(l1.union(l2)))

