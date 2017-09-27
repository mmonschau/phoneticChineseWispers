import jellyfish


# converting hamming distance to similarity metric
def calc_similarity(w1, w2):
    return 1 - (jellyfish.hamming_distance(w1, w2) / float(max([len(w1), len(w2)])))
