"""
Some simple methods for lapi

may be depricated soon
"""
from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps

def get_projects():
    project = []
    for coll in mongo.db.collection_names():
        project.append(coll.split('/')[0])
    return project

def get_types(project):
    types = []
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            types.append(coll.split('/')[1])
    return types
