from lazyAPI import app, mongo
from flask import Flask, jsonify, request, Response, render_template, send_from_directory
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from lazyAPI.controllers import general
from pymongo import ReturnDocument

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
