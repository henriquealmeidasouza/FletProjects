import os
import json
from flask import Flask, jsonify

app = Flask(__name__)
WD = os.path.dirname(os.path.abspath(__file__))

def load_database() -> list[dict]:
    path = os.path.join(WD, 'data.json')
    with open(path, 'r', encoding='utf-8') as djson:
        ddict = json.load(djson)
    return ddict
@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!', 200

@app.route('/fetch/<code>', methods=['GET'])
def fetch_pokefruit(code:str):
    data = load_database()
    res = {}
    for d in data:
        if d['code'] == code:
            res = d
            break
    return jsonify(res)