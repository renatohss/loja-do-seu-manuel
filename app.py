from flask import Flask, request, jsonify
from pymongo import MongoClient
from pprint import pprint
from helpers.jsonbuilder import JsonBuilder
from helpers.mongo_adapter import MongoConnect
import json

app = Flask(__name__)

client = MongoClient()
db = client.shopdata
products_coll = db.products
customers_coll = db.customers
orders_coll = db.orders

mc = MongoConnect()
jb = JsonBuilder()

@app.route('/product/get/<pk>', methods=['GET'])
def find_product(pk):

    params = {
        'id': int(pk)
    }

    job = mc.get(collection='products', params=params)
    return jsonify(job)


@app.route('/product/insert', methods=['POST'])
def insert_product():
    payload = request.get_json()

    job = mc.insert(collection='products', params=payload)
    return jsonify(job)


@app.route('/product/delete/<pk>', methods=['GET'])
def delete_product(pk):
    params = {
        'id': int(pk)
    }

    job = mc.delete(collection='products', params=params)
    return jsonify(job)


@app.route('/product/update/<pk>', methods=['POST'])
def update_product(pk):
    payload = request.get_json()
    update_doc = {}

    if len(payload) == 0:
        json_resp = jb.build(False, 'Update document cannot be empty')
        return jsonify(json_resp)
    
    id_check = products_coll.find_one({'id': pk})

    if not id_check:
        json_resp = jb.build(False, 'Product does not exist - Use /insert endpoint to insert it')
        return jsonify(json_resp)

    if 'id' in payload.keys():
        update_doc['id'] = payload['id']
    if 'name' in payload.keys():
        update_doc['name'] = payload['name']
    if 'description' in payload.keys():
        update_doc['description'] = payload['description']
    if 'price' in payload.keys():
        update_doc['price'] = payload['price']
    if 'stock' in payload.keys():
        update_doc['stock'] = payload['stock']
    if 'details' in payload.keys():
        update_doc['details'] = payload['details']

    job = mc.update(collection='product', pk=pk, params=update_doc)
    return 'Update product no. ' + pk
