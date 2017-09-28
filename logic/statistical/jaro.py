# coding=utf-8
import jellyfish


def calc_similarity(w1, w2):
    """

    :param w1:
    :param w2:
    """
    jellyfish.jaro_distance(w1, w2)
