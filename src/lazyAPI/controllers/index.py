from lazyAPI import app
from flask import Flask, render_template, send_from_directory

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
