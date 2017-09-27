import jellyfish


def calc_similarity(w1, w2):
    jellyfish.jaro_winkler(w1,w2)
