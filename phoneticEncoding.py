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
        raw_input_data = request.form
        input_data = dict(raw_input_data)['whispers'][0].split("\n")
        input_data = list(filter(lambda x: x, map(lambda x: x.strip(), input_data)))
        with open(path.join(data_root, unique_prefix() + ".json"), "w") as writer:
            json.dump(input_data, writer)
        results = compare.mult_full_compare(input_data)
        filtered_data = analyse.filter_mult(results)
        processedData = []
        for k, v in filtered_data.items():
            row = {'label': k, 'data': list(map(lambda x: round(x, 3), v))}
            row.update({k1: round(v1, 3) for k1, v1 in analyse.analyse_row(v).items()})
            processedData.append(row)
        max_var = max(map(lambda x: x['variance'],processedData))
        max_integral = max(map(lambda x: x['norm_integral'], processedData))
        return render_template('ResultView.html', data=processedData,
                               chartjs=(url_for('static', filename='js/Chart.bundle.min.js')),
                               palettejs=(url_for('static', filename='js/palette.min.js')),
                               labels=input_data,
                               max_var=max_var,
                               max_integral=max_integral)


if __name__ == '__main__':
    app.run()
