"""
Example index controller. Can be changed by the developer.
"""
from lazyAPI import app
from flask import Flask, render_template, send_from_directory, make_response
from flask_login import login_required
from flask_wtf.csrf import generate_csrf

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('views/img', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('views/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('views/css', path)

@app.route('/_static/<path:path>')
def send_static(path):
    return send_from_directory('views/html/_static', path)

@app.route('/')
@login_required
def get_index():
    response = make_response(render_template("html/index.html"))
    response.set_cookie('X-CSRF', generate_csrf())
    return response
