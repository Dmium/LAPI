from lazyAPI import app, mongo, login_manager
from flask import Flask, jsonify, request, Response, render_template, send_from_directory, abort
from lazyAPI.models.User import User
from flask_login import login_required, login_user, logout_user
import flask

@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)


# TODO Avoid timing attacks
@app.route('/login', methods=["POST", "GET"])
def login():
    request_dict = request.get_json()
    user = load_user(request_dict['id'])
    if user:
        if user.check_password(request_dict['password']):
            login_user(user, remember=True)
            return jsonify(success=True)
    return flask.abort(404)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(success=True)
