# coding=utf-8
# noinspection PyCompatibility
import statistics

import numpy as np
from svg.charts import line

from logic.util import unique_prefix


def analyse_single(data):
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


def analyse_mult(data):
    data_matrix = np.array(list(data.values()))
    d2 = {k: np.array(v) for k, v in data.items()}
    # Streiche alle algorithmen mit schlechterem als mittlerem Median
    d2medians = {k: np.median(v) for k, v in d2.items() if np.median(v) >= np.median(data_matrix)}
    # Streiche von den Verbleibenden Algorithmen alle schlechter als der durchschnitt
    d3mean = {k: np.mean(v) for k, v in d2medians.items() if
              k in set(d2medians.keys()) and np.mean(v) >= np.mean(data_matrix)}
    # Streiche von den Verbleibenden Algorithmen alle mit einer größeren Standartabweichung als der Durchschnitt
    avg_var = np.mean(np.array(list(map(lambda x: np.var(np.array(x)), list(data.values())))))
    d4var = {k: np.var(v) for k, v in d3mean.items() if np.var(v) <= avg_var}
    selected_keys = list(set(d4var.keys()))
    return {k: data[k] for k in selected_keys}


def draw_graph_mult(data, title=""):
    """

    :param data:
    :return:
    """
    g = line.Line()
    options = dict(
        scale_integers=True,
        area_fill=False,
        width=800,
        height=500,
        fields=list(map(lambda x: str(x), list(range(0, len(list(data.values())[0]))))),
        graph_title=title,
        show_graph_title=True,
        no_css=True,
    )
    g.__dict__.update(options)
    for k, v in data.items():
        g.add_data({'data': list(v), 'title': str(k)})
    flnm = ("comparison." + unique_prefix() + ".py.svg")
    res = g.burn()
    with open(flnm, "w") as writer:
        writer.write(res)
    return flnm
