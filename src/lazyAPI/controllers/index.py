from lazyAPI import app, mongo
from flask import Flask, jsonify, request, Response, render_template
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general

@app.route('/get_projects')
def get_projects():
    return jsonify(general.get_projects())

@app.route('/get_types/<project>')
def get_types(project):
    return jsonify(general.get_types(project))

@app.route('/')
def index():
    get_projects()
    return render_template("index.html")

@app.route('/config/init/<project>')
def init_database(project):
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            mongo.db[coll].drop()
    return 'Init complete'

@app.route('/<project>/<type>', methods=['POST'])
def create(project, type):
    request_dict = request.get_json()
    newobjid = mongo.db[str(project) + '/' + str(type)].insert_one(request_dict).inserted_id
    return Response(dumps(mongo.db[str(project) + '/' + str(type)].find_one({"_id": newobjid})), status=200, mimetype='application/json')

@app.route('/<project>/<type>/<oid>', methods=['GET'])
def read(project, type, oid):
    print(oid)
    return Response(dumps(mongo.db[str(project) + '/' + str(type)].find_one({"_id": ObjectId(str(oid))})), status=200, mimetype='application/json')

@app.route('/<project>/<type>', methods=['GET'])
def read_all(project, type):
    request_dict = request.get_json()
    if(request_dict == None):
        return Response(dumps(mongo.db[str(project) + '/' + str(type)].find()), status=200, mimetype='application/json')
    else:
        return Response(dumps(mongo.db[str(project) + '/' + str(type)].find(request_dict)), status=200, mimetype='application/json')

@app.route('/<project>/<type>/<oid>', methods=['PUT'])
def update(project, type, oid): # replace appropriate fields
    request_dict = request.get_json()
    mongo.db[str(project) + '/' + str(type)].update_one({'_id':ObjectId(str(oid))}, {"$set": request_dict})
    return Response(dumps(mongo.db[str(project) + '/' + str(type)].find_one({"_id": ObjectId(str(oid))})), status=200, mimetype='application/json')

@app.route('/<project>/<type>/<oid>', methods=['DELETE'])
def delete(project, type, oid):
    mongo.db[str(project) + '/' + str(type)].delete_one({'_id':ObjectId(str(oid))})
    return jsonify(["ok"]);
