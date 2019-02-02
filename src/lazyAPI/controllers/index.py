from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps

@app.route('/config/init/')
def init_database():
    print("Creating tables")
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Init complete'


@app.route('/<project>/<type>', methods=['POST'])
def create(project, type):
    request_dict = request.get_json()
    newobjid = mongo.db[str(project) + '/' + str(type)].insert_one(request_dict).inserted_id
    return Response(dumps(mongo.db[str(project) + '/' + str(type)].find_one({"_id": newobjid})), status=200, mimetype='application/json')

@app.route('/<project>/<type>/<oid>', methods=['GET'])
def read(project, type, oid):
    return Response(dumps(mongo.db[str(project) + '/' + str(type)].find_one({"_id": oid})), status=200, mimetype='application/json')

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
