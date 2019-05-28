from lazyAPI import app, mongo
from flask import Flask, jsonify, request, Response, render_template
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general

@app.route('/api/get_types')
def get_types():
    return jsonify(general.get_types('api'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/config/init')
def init_database():
    for coll in mongo.db.collection_names():
        if coll.startswith('api'):
            mongo.db[coll].drop()
    return 'Init complete'

@app.route('/api/<type>', methods=['POST'])
def create(type):
    request_dict = request.get_json()
    newobjid = mongo.db['api/' + str(type)].insert_one(request_dict).inserted_id
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": newobjid})), status=200, mimetype='application/json')

@app.route('/api/<type>/<oid>', methods=['GET'])
def read(type, oid):
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": ObjectId(str(oid))})), status=200, mimetype='application/json')

@app.route('/api/<type>', methods=['GET'])
def read_all(type):
    request_dict = request.get_json()
    if(request_dict == None):
        return Response(dumps(mongo.db['api/' + str(type)].find()), status=200, mimetype='application/json')
    else:
        return Response(dumps(mongo.db['api/' + str(type)].find(request_dict)), status=200, mimetype='application/json')

@app.route('/api/<type>/<oid>', methods=['PUT'])
def update(type, oid): # replace appropriate fields
    request_dict = request.get_json()
    mongo.db['api/' + str(type)].update_one({'_id':ObjectId(str(oid))}, {"$set": request_dict})
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": ObjectId(str(oid))})), status=200, mimetype='application/json')

@app.route('/api/<type>/<oid>', methods=['DELETE'])
def delete(type, oid):
    mongo.db['api/' + str(type)].delete_one({'_id':ObjectId(str(oid))})
    return jsonify(["ok"]);
