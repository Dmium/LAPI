from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
import os

@app.route('/generate/<project>', methods=['POST'])
def generate(project):
    os.makedirs("../projects/src/" + project + "/" + project + "/models")
    return "ok"
