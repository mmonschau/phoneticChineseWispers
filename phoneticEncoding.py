# coding=utf-8
import json
from os import path, listdir

from flask import Flask, request, render_template, url_for, abort, make_response, redirect

import logic.analyse as analyse
import logic.compare as compare
import logic.phonetics as phonetics
import logic.util as util
import storage.userInputCache

path_root = path.dirname(path.abspath(__file__))
template_root = path.join(path_root, "templates")
data_root = path.join(path_root, "data")
input_storage = path.join(data_root, "input")
data_storage = path.join(data_root, "results")
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


@app.route('/index')
@app.route('/home')
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
    check_access_permission()
    tokens = storage.userInputCache.get_tokens()
    return render_template('admin.html', tokens=tokens)


@app.route('/organizeInput', methods=['POST', 'GET'])
def reorder_user_input():
    check_access_permission()
    raw_input_data = getAllRequestData()
    token = raw_input_data.get("token")
    if token:
        userinput = storage.userInputCache.get_user_entries_by_token(token[0])
        return render_template('SingleInputJoin.html', userinput=userinput)
    return abort(400)


@app.route('/createToken')
def create_token_page():
    check_access_permission()
    token = util.gen_token()
    storage.userInputCache.insert_token(token)
    return render_template('TokenShow.html', hackcss=url_for('static', filename='css/hack.min.css'), token=token,
                           hostname=str(request.host))


@app.route('/save_data', methods=['POST', 'GET'])
def save_data():
    check_access_permission()
    raw_data = getAllRequestData()
    if raw_data:
        data = []
        if raw_data.get('joined_input'):
            print(raw_data)
            for i, v in enumerate(raw_data.get('userinput')):
                if raw_data['useable'][i] == "on":
                    data.append({'no': int(raw_data['inputno'][i]), 'word': v})
            data = sorted(data, key=lambda x: x['no'])
            data = list(map(lambda x: x['word'], data))
            data = raw_data.get('original') + data
        elif raw_data.get('total_input'):
            data = raw_data['whispers'][0].split("\n")
        data = list(filter(lambda x: x, map(lambda x: x.strip(), data)))
        d_id = util.unique_prefix()
        with open(path.join(input_storage, d_id + ".json"), "w") as writer:
            json.dump(data, writer)
        results = compare.mult_full_compare(data)
        combined_results = []
        for k, v in results[0].items():
            stat_data = analyse.analyse_row(v)
            stat_data.update({'algorithm': k, 'results': v})
            combined_results.append(stat_data)
        filtered_data = results[0]
        while len(filtered_data) > 10:
            filtered_data = analyse.filter_mult_for_high_values(filtered_data)
        results = {'results': combined_results, 'encoding': results[1],
                   'high_value_algorithms': list(filtered_data.keys()), 'src': data}
        with open(path.join(data_storage, d_id + ".json"), "w") as writer:
            json.dump(results, writer, indent="\t", sort_keys=True)
        return render_template('SaveSuccess.html', data_id=d_id)
    return abort(400)


# noinspection PyPep8Naming
@app.route('/result', methods=['POST', 'GET'])
def result():
    """

    :return:
    """
    raw_input_data = getAllRequestData()
    if raw_input_data:
        d_id = raw_input_data.get('data_id')
        if d_id:
            d_id = d_id[0] + ".json"
            if d_id in listdir(data_storage):
                data = json.load(open(path.join(data_storage, d_id)))
                displayed_data = data['results']
                if data.get('high_value_algorithms'):
                    displayed_data = list(
                        filter(lambda x: x['algorithm'] in data.get('high_value_algorithms'), displayed_data))
                for i, row in enumerate(displayed_data[:]):
                    new_row = row
                    new_row['label'] = row['algorithm']
                    new_row['data'] = row['results']
                    displayed_data[i] = new_row
                max_var = max(map(lambda x: x['variance'], displayed_data))
                max_integral = max(map(lambda x: x['norm_integral'], displayed_data))
                return render_template('ResultView.html', data=displayed_data,
                                       chartjs=(url_for('static', filename='js/Chart.bundle.min.js')),
                                       palettejs=(url_for('static', filename='js/palette.min.js')),
                                       labels=data['src'],
                                       max_var=max_var,
                                       max_integral=max_integral)
    return abort(400)


@app.route('/result_overview')
def result_overview():
    data = listdir(data_storage)
    data = list(map(lambda x: ".".join(x.split(".")[:-1]), data))
    return render_template("PreviousRuns.html", data=data)


@app.route('/phon_demo')
def phonetic_demo():
    raw_input_data = getAllRequestData()
    if raw_input_data:
        unencoded_str = raw_input_data.get("unencoded")
        if unencoded_str:
            phonetic = phonetics.encPhoneVariants(unencoded_str[0])
            return render_template("PhoneticDemo.html", phonetic=phonetic, unencoded=unencoded_str[0].strip())
    return render_template("PhoneticDemo.html")


def check_access_permission():
    print(request.host)
    if not str(request.host).split(":")[0] in ["0.0.0.0","127.0.0.1","localhost"]:
        return abort(400)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
