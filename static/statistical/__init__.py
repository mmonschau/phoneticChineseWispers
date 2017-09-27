import static.statistical.bag_distance
import static.statistical.damerau_levenshtein
import static.statistical.dice_coefficient
import static.statistical.hamming
import static.statistical.jaccard
import static.statistical.jaro
import static.statistical.jaro_winkler
import static.statistical.lcsubstring
import static.statistical.levenshtein
import static.statistical.sequence

distance_metrics = {"Bag Distance": bag_distance.calc_similarity,
                    "Damerau Levenshtein Distance": damerau_levenshtein.calc_similarity,
                    "Dice Coefficient": dice_coefficient.calc_similarity,
                    "Hamming Distance": hamming.calc_similarity,
                    "Jaccard Index:": jaccard.calc_similarity,
                    "Jaro Distance": jaro.calc_similarity,
                    "Jaro Winkler Distance": jaro_winkler.calc_similarity,
                    "Longest common substring": lcsubstring.calc_similarity,
                    "Levenshtein Distance": levenshtein.calc_similarity,
                    "Sequence Matching": sequence.calc_similarity
                    }
