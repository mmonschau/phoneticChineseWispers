# coding=utf-8
import json
from os import path
from string import Template

from flask import Flask, request, render_template

import analyse
import compare
from util import unique_prefix

path_root = path.dirname(path.abspath(__file__))
template_root = path.join(path_root, "templates")
data_root = path.join(path_root, "data")
app = Flask(__name__)


def procc_template(template_file, inserts={}):
    template = Template(open(template_file, "r").read())
    return template.safe_substitute(inserts)


@app.route('/')
def hello_world():
    """

    :return:
    """
    return 'Hello World!'


@app.route('/input')
def input_all():
    page = procc_template(path.join(template_root, "Header.html"), {'title': "PyChineseWhispers Input"})
    page += procc_template(path.join(template_root, "Input.html"))
    page += procc_template(path.join(template_root, "Footer.html"))
    return page


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        raw_data = request.form
        data = dict(raw_data)['whispers'][0].split("\n")
        data = list(filter(lambda x: x, map(lambda x: x.strip(), data)))
        with open(path.join(data_root, unique_prefix() + ".json"), "w") as writer:
            json.dump(data, writer)
        results = compare.mult_full_compare(data)
        filtered_data = analyse.filter_mult(results)
        for k, v in results.items():
            print(v)
            results[k] = list(map(lambda x: round(x, 3), v))
        return render_template('ResultView.html', data=[[k] + v for k, v in results.items()])


if __name__ == '__main__':
    app.run()
