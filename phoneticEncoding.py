# coding=utf-8
import json
from os import path

from flask import Flask, request, render_template, url_for

import analyse
import compare
from util import unique_prefix

path_root = path.dirname(path.abspath(__file__))
template_root = path.join(path_root, "templates")
data_root = path.join(path_root, "data")
app = Flask(__name__)


@app.route('/')
def hello_world():
    """

    :return:
    """
    return 'Hello World!'


@app.route('/input')
def input_all():
    """

    :return:
    """
    return render_template('InputView.html')


# noinspection PyPep8Naming
@app.route('/result', methods=['POST', 'GET'])
def result():
    """

    :return:
    """
    if request.method == 'POST':
        raw_data = request.form
        data = dict(raw_data)['whispers'][0].split("\n")
        data = list(filter(lambda x: x, map(lambda x: x.strip(), data)))
        with open(path.join(data_root, unique_prefix() + ".json"), "w") as writer:
            json.dump(data, writer)
        results = compare.mult_full_compare(data)
        filtered_data = analyse.filter_mult(results)
        print(filtered_data)
        processedData = []
        for k, v in filtered_data.items():
            row = {'label': k, 'data': list(map(lambda x: round(x, 3), v))}
            row.update({k1: round(v1, 3) for k1, v1 in analyse.analyse_row(v).items()})
            processedData.append(row)
        return render_template('ResultView.html', data=processedData,
                               chartjs=(url_for('static', filename='js/Chart.bundle.min.js')),
                               palettejs=(url_for('static', filename='js/palette.min.js')),
                               labels=data[1:])


if __name__ == '__main__':
    app.run()
