from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
#from flask_talisman import Talisman

login_manager = LoginManager() # TODO consider hooking for this
app = Flask(__name__, static_folder="views", template_folder="views")
app.config.from_object('lazyAPIconfig')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager.init_app(app)
#Talisman(app)

from lazyAPI.controllers import lapi_meta, custom_hooks, api, generate, general
