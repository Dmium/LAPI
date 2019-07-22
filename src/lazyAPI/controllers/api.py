"""
Handles generic JIT endpoints and db reset endpoint.

Changes *will not* remain after code generation but will remain in the JIT.
"""
from lazyAPI import app, mongo, csrf
from flask import Flask, jsonify, request, Response, render_template, send_from_directory
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general
from lazyAPI.models.User import User
from pymongo import ReturnDocument

#TODO - Check if belongs elsewhere
@app.route(app.config['API_ENDPOINT'] + '/get_types')
def get_types():
    return jsonify(general.get_types('api'))


@app.route(app.config['API_ENDPOINT'] + '/config/init')
def init_database():
    """
    resets the database
    """
    for coll in mongo.db.collection_names():
        mongo.db[coll].drop()
    mongo.db['users'].insert_one(
        {'_id': 'admin', 'phash': User.get_phash('password')})
    return 'Init complete'


def get_new_id(typex):
    """
    :param typex: typex is no longer needed. May depricate.
    gets a valid new sequential ID safely (avoids race conditions)
    """
    if mongo.db['meta'].find_one({'name': 'seqno'}) is None:
        mongo.db['meta'].insert_one({'name': 'seqno', 'seq': -1})
    return mongo.db['meta'].find_one_and_update(
        {'name': 'seqno'},
        {'$inc': {'seq': 1}},
        return_document=ReturnDocument.AFTER)['seq']


@app.route(app.config['API_ENDPOINT'] + '/<typex>', methods=['POST'])
@csrf.exempt
def create(typex):
    """
    CRUD Create. Matches POST request with json.

    :param typex: name of what will become the class name

    Returns new object with generated ID
    """
    print(request.headers)
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
    else:
        mongo.db['endpoints'].insert_one(
            {'name': typex, 'properties': propertydict, 'seq': 0})
        request_dict['_id'] = get_new_id(typex)
    newobjid = mongo.db['api/' +
                        str(typex)].insert_one(request_dict).inserted_id
    return Response(dumps(mongo.db['api/' + str(typex)].find_one({"_id": newobjid})), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<type>/<_id>', methods=['GET'])
def read(type, _id):
    """
    CRUD Read. Matches GET request of REST.

    :param _id: ID of the object to get

    Returns matching object
    """
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": int(_id)})), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<type>', methods=['GET'])
def read_all(type):
    """
    Matches CRUD Read again.

    Returns all objects of a specified type
    """
    request_dict = request.get_json()
    if(request_dict == None):
        return Response(dumps(mongo.db['api/' + str(type)].find()), status=200, mimetype='application/json')
    else:
        return Response(dumps(mongo.db['api/' + str(type)].find(request_dict)), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<type>/<_id>', methods=['PUT'])
def update(type, _id):  # replace appropriate fields
    """
    Matches CRUD Update and REST PUT

    :param _id: ID of the object to edit

    Returns edited object
    """
    request_dict = request.get_json()
    mongo.db['api/' +
             str(type)].update_one({'_id': int(_id)}, {"$set": request_dict})
    return Response(dumps(mongo.db['api/' + str(type)].find_one({"_id": int(_id)})), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<type>/<_id>', methods=['DELETE'])
def delete(type, _id):
    """
    CRUD Delete. REST DELETE.

    :param _id: ID of the object to be deleted

    Returns "OK" in a json array for some reason.
    """
    mongo.db['api/' + str(type)].delete_one({'_id': int(_id)})
    return jsonify(["ok"])
