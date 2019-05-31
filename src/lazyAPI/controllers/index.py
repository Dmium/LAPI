from lazyAPI import app, mongo
from flask import Flask, jsonify, request, Response, render_template, send_from_directory
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general
from pymongo import ReturnDocument

@app.route('/api/get_types')
def get_types():
    return jsonify(general.get_types('api'))

@app.route('/lapi')
def lapi_index():
    return render_template("lapi/index.html")

@app.route('/lapi/<path:path>')
def get_lapi_gui(path):
    return send_from_directory('views/lapi', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('views/img', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('views/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('views/css', path)

@app.route('/')
def get_index():
    return render_template("index.html")

@app.route('/api/config/init')
def init_database():
    for coll in mongo.db.collection_names():
        if coll.startswith('api'):
            mongo.db[coll].drop()
    return 'Init complete'

def get_new_id(typex):
    return mongo.db['endpoints'].find_one_and_update(
    { 'name': typex },
    { '$inc': { 'seq': 1 } },
    return_document=ReturnDocument.AFTER)['seq']


@app.route('/api/<typex>', methods=['POST'])
def create(typex):
    request_dict = request.get_json()
    ctype = mongo.db['endpoints'].find_one({'name': typex})
    propertydict = {}
    for name, value in request_dict.items():
        propertydict[name] = str(type(value))
    if ctype != None:
        cid = ctype['_id']
        ctype['properties'].update(propertydict)
        mongo.db['endpoints'].replace_one({'_id': cid}, ctype)
        request_dict['_id'] = get_new_id(typex)
    else :
        mongo.db['endpoints'].insert_one({'name': typex, 'properties': propertydict, 'seq': 0})
        request_dict['_id'] = get_new_id(typex)
    newobjid = mongo.db['api/' + str(typex)].insert_one(request_dict).inserted_id
    return Response(dumps(mongo.db['api/' + str(typex)].find_one({"_id": newobjid})), status=200, mimetype='application/json')

@app.route('/api/<type>/<_id>', methods=['GET'])
def read(type, _id):
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": int(_id)})), status=200, mimetype='application/json')

@app.route('/api/<type>', methods=['GET'])
def read_all(type):
    request_dict = request.get_json()
    if(request_dict == None):
        return Response(dumps(mongo.db['api/' + str(type)].find()), status=200, mimetype='application/json')
    else:
        return Response(dumps(mongo.db['api/' + str(type)].find(request_dict)), status=200, mimetype='application/json')

@app.route('/api/<type>/<_id>', methods=['PUT'])
def update(type, _id): # replace appropriate fields
    request_dict = request.get_json()
    mongo.db['api/' + str(type)].update_one({'_id':int(_id)}, {"$set": request_dict})
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": int(_id)})), status=200, mimetype='application/json')

@app.route('/api/<type>/<_id>', methods=['DELETE'])
def delete(type, _id):
    mongo.db['api/' + str(type)].delete_one({'_id': int(_id)})
    return jsonify(["ok"]);
