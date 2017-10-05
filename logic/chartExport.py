from svg.charts import line

from logic.util import unique_prefix


def draw_graph_mult(data, title=""):
    """

    :param title:
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
