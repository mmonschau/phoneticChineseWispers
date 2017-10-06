# coding=utf-8
import json
from os import path

from flask import Flask, request, render_template, url_for, abort, make_response, redirect

import analyse
import compare
import storage.userInputCache
import util

path_root = path.dirname(path.abspath(__file__))
template_root = path.join(path_root, "templates")
data_root = path.join(path_root, "data")
app = Flask(__name__)
storage.userInputCache.create_DB(app.debug)


# method for union of get an post-data (post overrides get)
def getAllRequestData():
    result = dict(request.args)
    result.update(dict(request.form))
    return result


def getUUID():
    uuid = request.cookies.get('UUID')
    if not uuid:
        uuid = request.form.get('uuid')
        if not uuid:
            uuid = util.unique_prefix(util.create_alphabet_from_ascii())
    return uuid


@app.route('/id')
def id_page():
    uuid = getUUID()
    resp = make_response(
        render_template('TokenShow.html', hackcss=url_for('static', filename='css/hack.min.css'), token=uuid,
                        fontsize="large"))
    resp.set_cookie('UUID', uuid)
    return resp


@app.route('/')
def index_page():
    """

    :return:
    """
    uuid = getUUID()
    resp = make_response(render_template('Index.html'))
    resp.set_cookie('UUID', uuid)
    return resp


@app.route('/input')
def input_all():
    """

    :return:
    """
    return render_template('InputView.html')


@app.route('/input_single', methods=['POST', 'GET'])
def input_single():
    raw_input_data = getAllRequestData()
    token = raw_input_data.get("token")
    if token:
        uuid = getUUID()
        resp = make_response(render_template("InputSingle.html", token=token[0], UUID=uuid))
        resp.set_cookie('UUID', uuid)
        return resp
    return abort(400)


@app.route('/submit_single', methods=['POST', 'GET'])
def single_submission_handle():
    raw_input_data = getAllRequestData()
    if raw_input_data:
        heard = raw_input_data.get('heared')
        row_number = raw_input_data.get('row_number')
        token = raw_input_data.get('token')
        if heard and row_number and token:
            storage.userInputCache.insert_user_entry(getUUID(), token[0], row_number[0], heard[0])
            return redirect(url_for('id_page'))
    return abort(400)


@app.route('/admin')
def admin_page():
    tokens = storage.userInputCache.get_tokens()
    return render_template('admin.html', tokens=tokens)


@app.route('/organizeInput', methods=['POST', 'GET'])
def reorder_user_input():
    raw_input_data = getAllRequestData()
    token = raw_input_data.get("token")
    if token:
        userinput = storage.userInputCache.get_user_entries_by_token(token[0])
        return render_template('SingleInputJoin.html', userinput=userinput)
    return abort(400)


@app.route('/createToken')
def create_token_page():
    token = util.gen_token()
    storage.userInputCache.insert_token(token)
    return render_template('TokenShow.html', hackcss=url_for('static', filename='css/hack.min.css'), token=token)


@app.route('/save_data', methods=['POST', 'GET'])
def save_data():
    raw_data = getAllRequestData()
    if raw_data:
        data = []
        if raw_data.get('joined_input'):
            for i, v in enumerate(raw_data.get('userinput[]')):
                if raw_data['useable[]'][i] == "on":
                    data.append({'no': int(raw_data['inputno[]'][i]), 'word': v})
            data = sorted(data, key=lambda x: x['no'])
            data = list(map(lambda x: x['word'], data))
            data = raw_data.get('original') + data
        elif raw_data.get('total_input'):
            data = raw_data['whispers'][0].split("\n")
        data = list(filter(lambda x: x, map(lambda x: x.strip(), data)))
        d_id = util.unique_prefix()
        with open(path.join(path.join(data_root, "input"), d_id + ".json"), "w") as writer:
            json.dump(data, writer)
        results = compare.mult_full_compare(data)
        combined_results=[]
        for k, v in results[0].items():
                stat_data=analyse.analyse_row(v)
                stat_data.update({'algorithm': k, 'results': v})
                combined_results.append(stat_data)
        filtered_data = results[0]
        while len(filtered_data) > 10:
            filtered_data = analyse.filter_mult_for_high_values(filtered_data)
        results = {'results': combined_results, 'encoding': results[1] , 'high_value_algorithms':list(filtered_data.keys())}
        with open(path.join(path.join(data_root, "results"), d_id + ".json"), "w") as writer:
            json.dump(results, writer, indent="\t",sort_keys=True)
        return d_id
    return abort(400)


# noinspection PyPep8Naming
@app.route('/result', methods=['POST', 'GET'])
def result():
    """

    :return:
    """
    raw_input_data = getAllRequestData()
    if raw_input_data:
        input_data = raw_input_data['whispers'][0].split("\n")
        input_data = list(filter(lambda x: x, map(lambda x: x.strip(), input_data)))
        with open(path.join(data_root, util.unique_prefix() + ".json"), "w") as writer:
            json.dump(input_data, writer)
        results = compare.mult_full_compare(input_data)
        filtered_data = results[0]
        while len(filtered_data) > 10:
            filtered_data = analyse.filter_mult_for_high_values(filtered_data)
        if not len(filtered_data):
            filtered_data = results[0]
        processedData = []
        for k, v in filtered_data.items():
            row = {'label': k, 'data': list(map(lambda x: round(x, 3), v))}
            row.update({k1: round(v1, 3) for k1, v1 in analyse.analyse_row(v).items()})
            processedData.append(row)
        max_var = max(map(lambda x: x['variance'], processedData))
        max_integral = max(map(lambda x: x['norm_integral'], processedData))
        return render_template('ResultView.html', data=processedData,
                               chartjs=(url_for('static', filename='js/Chart.bundle.min.js')),
                               palettejs=(url_for('static', filename='js/palette.min.js')),
                               labels=input_data,
                               max_var=max_var,
                               max_integral=max_integral)


if __name__ == '__main__':
    app.run()
