from flask import Flask, request, jsonify
from pprint import pprint
from helpers.jsonbuilder import JsonBuilder
from helpers.mongo_adapter import MongoConnect
from helpers.order_manager import OrderManager
import json

app = Flask(__name__)

mc = MongoConnect()
jb = JsonBuilder()
om = OrderManager()

@app.route('/get/', methods=['GET'])
def find_object():
    id = request.args.get('id')
    collection = request.args.get('type')
    params = {
        'id': int(id)
    }

    job = mc.get(collection=collection, params=params)
    return jsonify(job)


@app.route('/new/', methods=['POST'])
def insert_object():
    collection = request.args.get('type')
    payload = request.get_json()

    if len(payload) == 0:
        json_resp = jb.build(False, 'JSON cannot be empty')
        return jsonify(json_resp)

    if collection == 'orders':
        job = om.validate_new_order(order=payload)
        return jsonify(job)

    elif collection == 'products':
        job = mc.insert(collection=collection, params=payload)
        return jsonify(job)


@app.route('/delete/', methods=['GET'])
def delete_object(pk):
    id = request.args.get('id')
    collection = request.args.get('type')
    params = {
        'id': int(id)
    }

    job = mc.delete(collection=collection, params=params)
    return jsonify(job)


@app.route('/update/', methods=['POST'])
def update_object():
    id = request.args.get('id')
    collection = request.args.get('type')
    payload = request.get_json()

    if len(payload) == 0:
        json_resp = jb.build(False, 'JSON cannot be empty')
        return jsonify(json_resp)

    job = mc.update(collection=collection, pk=int(id), params=payload)
    return jsonify(job)

@app.route('/get_ticket/', methods=['GET'])
def get_ticket():
    ticket = om.calculate_ticket()
    print('Average Ticket:', ticket)
    return jsonify(ticket)