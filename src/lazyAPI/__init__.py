from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object('lazyAPIconfig')
CORS(app)
mongo = PyMongo(app)

from lazyAPI.controllers import index, generate, general
