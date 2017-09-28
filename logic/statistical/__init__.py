# coding=utf-8
import logic.statistical.bag_distance
import logic.statistical.damerau_levenshtein
import logic.statistical.dice_coefficient
import logic.statistical.hamming
import logic.statistical.jaccard
import logic.statistical.jaro
import logic.statistical.jaro_winkler
import logic.statistical.lcsubstring
import logic.statistical.levenshtein
import logic.statistical.sequence

distance_metrics = {"Bag Distance": bag_distance.calc_similarity,
                    "Damerau Levenshtein Distance": damerau_levenshtein.calc_similarity,
                    "Dice Coefficient": dice_coefficient.calc_similarity,
                    "Hamming Distance": hamming.calc_similarity,
                    # "Jaccard Index": jaccard.calc_similarity,
                    "Jaro Distance": jaro.calc_similarity,
                    "Jaro Winkler Distance": jaro_winkler.calc_similarity,
                    "Longest common substring": lcsubstring.calc_similarity,
                    "Levenshtein Distance": levenshtein.calc_similarity,
                    "Sequence Matching": sequence.calc_similarity
                    }
