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


def get_new_id(modelname):
    """
    :param modelname: modelname is no longer needed due to globally sequential IDs. May depricate.
    gets a valid new sequential ID safely (avoids race conditions)
    """
    if mongo.db['meta'].find_one({'name': 'seqno'}) is None:
        mongo.db['meta'].insert_one({'name': 'seqno', 'seq': -1})
    return mongo.db['meta'].find_one_and_update(
        {'name': 'seqno'},
        {'$inc': {'seq': 1}},
        return_document=ReturnDocument.AFTER)['seq']

def match_relationships(record, modelname, depth=2):
    cmodel = mongo.db['endpoints'].find_one({'name': modelname})
    record['_link'] = {
        'self': {
            'href': '/api/' + modelname + '/' + str(record['_id'])
        }
    }
    record['_embedded'] = {}
    if 'relationships' in cmodel:
        for fieldname, relmodelname in cmodel['relationships'].items():
            record['_embedded'][fieldname] = mongo.db[relmodelname].find_one({'_id': record[fieldname]['_id']})
            record['_link'][fieldname] = {
                'href': '/' + relmodelname + '/' + str(record[fieldname]['_id'])
            }
    if depth >= 0:
        if 'impliedrelationships' in cmodel:
            for relationship in cmodel['impliedrelationships']:
                if 'fieldname' in relationship:
                    record['_embedded'][relationship['fieldname']] = group_match_relationships(mongo.db['api/' + relationship['relmodelname']].find({relationship['relfieldname']: {'_id': record['_id']}}), relationship['relmodelname'], depth)
                    record['_link'][relationship['fieldname']] = []
                    for item in record['_embedded'][relationship['fieldname']]:
                        record['_link'][relationship['fieldname']].append({'href': '/api/' +relationship['relmodelname'] + '/' + str(item['_id'])})
        if record['_embedded'] == {}:
            del(record['_embedded'])
    return record

def group_match_relationships(group, modelname, depth=2):
    resolved_records = []
    for record in group:
        resolved_records.append(match_relationships(record, modelname, depth=depth - 1))
    return resolved_records

def handle_relationship(rel_dict, modelname, cmodel, fieldname):
    if 'relationships' not in cmodel:
        cmodel['relationships'] = {}
    if fieldname not in cmodel['relationships']:
        cmodel['relationships'][fieldname] =  general.search_by_id(rel_dict['_id'])
        relmodel = mongo.db['endpoints'].find_one({'name': cmodel['relationships'][fieldname].split('api/')[1]})
        if 'impliedrelationships' not in relmodel:
            relmodel['impliedrelationships'] = []
        relmodel['impliedrelationships'].append({
            'relmodelname': modelname,
            'relfieldname': fieldname
        })
        mongo.db['endpoints'].find_one_and_update({"_id": relmodel['_id']}, 
                                 {"$set": {"impliedrelationships": relmodel['impliedrelationships']}})
        

def handle_properties(request_dict, modelname):
    """
    :param request_dict:
    :param modelname:
    Stores information about properties of a model for later code generation
    """
    # Get known info about a model
    cmodel = mongo.db['endpoints'].find_one({'name': modelname})

    # Format a dictionary to match the endpoints info
    propertydict = {}
    relationshipdict = {}
    for name, value in request_dict.items():
        propertytype = str(type(value))
        if propertytype == str(type({})):
            relationshipdict[name] = value
        else:
            propertydict[name] = str(type(value))

    if cmodel is None:
        # If no info is known create a new endpoint
        mongo.db['endpoints'].insert_one(
            {'name': modelname, 'properties': propertydict, 'seq': 0})
        request_dict['_id'] = get_new_id(modelname)
    cmodel = mongo.db['endpoints'].find_one({'name': modelname})
    for name, value in relationshipdict.items():
        handle_relationship(value, modelname, cmodel, name)
    # Otherwise update the previous endpoint with any new information
    cid = cmodel['_id']
    cmodel['properties'].update(propertydict)
    mongo.db['endpoints'].replace_one({'_id': cid}, cmodel)
    request_dict['_id'] = get_new_id(modelname)

@app.route(app.config['API_ENDPOINT'] + '/<modelname>', methods=['POST'])
@csrf.exempt
def create(modelname):
    """
    CRUD Create. Matches POST request with json.

    :param modelname: name of what will become the class name

    Returns new object with generated ID
    """
    request_dict = request.get_json()
    handle_properties(request_dict, modelname)
    newobjid = mongo.db['api/' +
                        str(modelname)].insert_one(request_dict).inserted_id
    
    return Response(dumps(match_relationships(mongo.db['api/' + str(modelname)].find_one({"_id": newobjid}), modelname)), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<modelname>/<_id>', methods=['GET'])
def read(modelname, _id):
    """
    CRUD Read. Matches GET request of REST.

    :param _id: ID of the object to get

    Returns matching object
    """
    return Response(dumps(match_relationships(mongo.db['api/' + str(modelname)].find_one({"_id": int(_id)}), modelname)), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<modelname>', methods=['GET'])
def read_all(modelname):
    """
    Matches CRUD Read again.

    Returns all objects of a specified type
    """
    for arg in request.args:
         print(arg + ':', request.args[arg])
    request_dict = request.get_json()
    if(request_dict is None):
        return Response(dumps(group_match_relationships(mongo.db['api/' + str(modelname)].find(), modelname, depth=1)), status=200, mimetype='application/json')
    else:
        return Response(dumps(group_match_relationships(mongo.db['api/' + str(modelname)].find(request_dict), modelname, depth=1)), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<modelname>/<_id>', methods=['PUT'])
def update(modelname, _id):  # replace appropriate fields
    """
    Matches CRUD Update and REST PUT

    :param _id: ID of the object to edit

    Returns edited object
    """
    request_dict = request.get_json()
    mongo.db['api/' +
             str(modelname)].update_one({'_id': int(_id)}, {"$set": request_dict})
    return Response(dumps(match_relationships(mongo.db['api/' + str(modelname)].find_one({"_id": int(_id)}), modelname)), status=200, mimetype='application/json')


@app.route(app.config['API_ENDPOINT'] + '/<modelname>/<_id>', methods=['DELETE'])
def delete(modelname, _id):
    """
    CRUD Delete. REST DELETE.

    :param _id: ID of the object to be deleted

    Returns "OK" in a json array for some reason.
    """
    mongo.db['api/' + str(modelname)].delete_one({'_id': int(_id)})
    return jsonify(["ok"])
