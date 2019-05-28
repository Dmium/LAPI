from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__, static_folder="views", template_folder="views")
app.config.from_object('lazyAPIconfig')
mongo = PyMongo(app)

from lazyAPI.controllers import index, generate, general
