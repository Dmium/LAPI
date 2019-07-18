"""
Handles the /lapi endpoint for developer settings/management
"""
from lazyAPI import app, mongo
from flask import Flask, jsonify, request, Response, render_template, send_from_directory, make_response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general
from pymongo import ReturnDocument
from flask_login import login_required
from flask_wtf.csrf import generate_csrf

# @app.after_request
# def set_xsrf_cookie(response):
#     response.set_cookie('X-CSRF', generate_csrf())
#     return response


@app.route('/lapi')
def lapi_index():
    """
    gets the meta index for lapi
    """
    response = make_response(render_template("lapi/index.html"))
    response.set_cookie('X-CSRF', generate_csrf())
    return response


@app.route('/lapi/<path:path>')
def get_lapi_gui(path):
    """
    gets sub-directories of meta lapi
    """
    return send_from_directory('views/lapi', path)


@app.route('/lapi/types')
def lapi_types():
    """
    gets all metadata on known types
    """
    return Response(dumps(mongo.db['endpoints'].find({})))


@app.route('/lapi/types/<name>')
def lapi_type_info(name):
    """
    gets information on a specific type
    """
    return Response(dumps(mongo.db['endpoints'].find_one({'name': name})), status=200, mimetype='application/json')


@app.route('/lapi/types/<typename>/property/<propertyname>', methods=['DELETE'])
def lapi_property_delete(typename, propertyname):
    """
    deletes a type's property
    
    returns the type's new state
    """
    return Response(dumps(mongo.db['endpoints'].find_one_and_update(
        {'name': typename},
        {'$unset': {'properties.' + propertyname: ''}},
        return_document=ReturnDocument.AFTER)), status=200, mimetype='application/json')


@app.route('/lapi/types/<typename>/property/merge/<propertyname>/<mergedpropertyname>', methods=['PUT'])
def lapi_property_merge(typename, propertyname, mergedpropertyname):
    """
    Will merge properites into other properties later. Currently just deletes a property
    """
    return lapi_property_delete(typename, mergedpropertyname)
