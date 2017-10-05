# coding=utf-8
# noinspection PyCompatibility
import statistics

import numpy as np


def analyse_single_pair(data):
    """

    :param data:
    :return:
    """
    result = {"best match": max(data.values())}
    result["best match algorithms"] = [k for k, v in data.items() if v == result["best match"]]
    result["worst match"] = min(data.values())
    result["worst match algorithms"] = [k for k, v in data.items() if v == result["worst match"]]
    result["avarage match"] = statistics.mean(data.values())
    result["median match"] = statistics.mean(data.values())
    return result


def analyse_row(data):
    result = {}
    result['max'] = max(data)
    result['min'] = min(data)
    result['integral'] = approx_integral(data)
    result['norm_integral'] = result['integral'] / len(data)
    np_data = np.array(list(data))
    result['mean'] = np.mean(np_data)
    result['median'] = np.median(np_data)
    result['variance'] = np.var(np_data)
    return result

def filter_mult(data):
    """

    :param data:
    :return:
    """
    data_matrix = np.array(list(data.values()))
    selected_keys = list(data.keys())
    d2 = {k: np.array(v) for k, v in data.items()}
    if len(selected_keys) > 10:
        # Streiche alle algorithmen mit schlechterem als mittlerem Median
        selected_keys = [k for k, v in d2.items() if np.median(v) >= np.median(data_matrix)]
    if len(selected_keys) > 10:
        # Streiche von den Verbleibenden Algorithmen alle schlechter als der durchschnitt
        selected_keys = [k for k, v in d2.items() if k in selected_keys and np.mean(v) >= np.mean(data_matrix)]
    if  len(selected_keys) > 10:
        # Streiche von den Verbleibenden Algorithmen alle mit einer größeren Standartabweichung als der Durchschnitt
        avg_var = np.mean(np.array(list(map(lambda x: np.var(np.array(x)), list(data.values())))))
        selected_keys = [k for k, v in d2.items() if k in selected_keys and np.var(v) <= avg_var]
    if len(selected_keys) > 10:
        # Streiche von den verbleibenden Werte alle die weniger "Fläche" als der median aller Flächen einschließt ( Integralmethode)
        d_integral = {k: approx_integral(data[k]) for k in selected_keys}
        selected_keys = [k for k, v in d_integral.items() if v >= np.mean(np.array(list(d_integral.values())))]
    return {k: data[k] for k in selected_keys}




def approx_integral(datum, integral_length=1):
    """

    :param datum:
    :param integral_length:
    :return:
    """
    datum = list(datum)
    result = 0
    for pair in list(zip(datum, datum[1:])):
        result += (min(pair) + abs(pair[0] - pair[1]) / 2) * integral_length
    return result
