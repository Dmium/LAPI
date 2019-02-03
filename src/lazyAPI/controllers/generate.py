from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
import shutil

@app.route('/generate/<project>', methods=['GET'])
def generate(project):
    path = "../projects/src/" + project + "/"
    if(os.path.exists(path)):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    os.makedirs(path + project + "/models/")
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            modelname = coll[(coll.find("/")+1):]
            f = open(path + project + "/models/" + modelname + ".py", "w+")
            f.write("from " + project + " import db, ma\n\n")
            f.write("class " + modelname + "(db.Model):\n")
            f.write("    __tablename__ = \"" + modelname + "\"\n")
            f.write("    id = db.Column(db.Integer, primary_key = True)\n")
            attributes = []
            types = []
            for documentname in mongo.db[str(coll)].find():
                for key, value in documentname.items():
                    if not(key in attributes) and not(key == "_id"):
                        attributes.append(key)
                        types.append(type(value))
            for i in range(len(types)):
                if str(types[i]) == "<class 'str'>":
                    types[i] = "Text"
                elif str(types[i]) == "<class 'int'>":
                    types[i] = "Integer"
                elif str(types[i]) == "<class 'float'>":
                    types[i] = "Float"
                elif str(types[i]) == "<class 'bool'>":
                    types[i] = "Boolean"

            for i in range(len(attributes)):
                f.write("    " + attributes[i] + " = db.Column(db." + str(types[i]) + ")\n")
            f.write("\nclass " + modelname + "_Schema(ma.ModelSchema):")
            f.write("\n    class Meta:")
            f.write("\n        model = " + modelname + "\n\n")
            f.write(modelname + "_schema" + " = " + modelname.title() + "_Schema()\n")
            f.write(modelname + "_schemas" + " = " + modelname.title() + "_Schema(many=True)\n")
            f.close()
    generate_controllers(project)
    generate_configs(project)
    return "ok"

def generate_controllers(project):
    path = "../projects/src/" + project + "/"
    os.makedirs(path + project + "/controllers/")
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            modelname = coll[(coll.find("/")+1):]
            f = open(path + project + "/controllers/" + modelname + ".py", "w+")
            f.write("from " + project + " import db, ma, app\n")
            f.write("from flask import jsonify, request, make_response\n")
            f.write("from " + project + ".models." + modelname + " import " + modelname + ", " + modelname + "_schema, " + modelname + "_schemas\n\n")
            f.write("@app.route('/" + project + "/" + modelname + "', methods=['POST'])\n")
            f.write("def create_" + modelname + "():\n")
            f.write("    db.session.add(" + modelname + "(**request.get_json()))\n")
            f.write("    db.session.commit()\n")
            f.write("    return jsonify(['ok'])\n\n")
            f.write("@app.route('/" + project + "/" + modelname + "', methods=['GET'])\n")
            f.write("def read_" + modelname + "():\n")
            f.write("    return jsonify(" + modelname + "_schemas.dump(" + modelname + ".query.all()))\n\n")
            f.close()

def generate_configs(project):
    path = "../projects/src/" + project + "/"
    f = open(path + "setup.bat", "w+")
    f.write("set FLASK_APP=" + project + "\npip install -e .\nflask run\n")
    f.close()
    f = open(path + "setup.sh", "w+")
    f.write("export FLASK_APP=" + project + "\nexport FLASK_ENV=development\nsudo pip3 install -e .\nflask run\n")
    f.close()
    f = open(path + "setup.py", "w+")
    f.write("from setuptools import setup\nsetup(\n    name='" + project + "',\n    packages=['" + project + "',\n              '" + project + ".controllers'],\n    include_package_data=True,\n    install_requires=[\n        'flask',\n        'flask-cors',\n        'flask-sqlalchemy',\n        'flask-marshmallow',\n        'marshmallow-sqlalchemy'\n    ],\n)")
    f.close()
    f = open(path + project + "config.py", "w+")
    f.write('DEBUG = True\nSQLALCHEMY_DATABASE_URI = "postgresql://dom@localhost/' + project + '"\nSQLALCHEMY_TRACK_MODIFICATIONS = True\nDATABASE_CONNECT_OPTIONS = {}\nTHREADS_PER_PAGE = 2\n')
    f.close()
    path = "../projects/src/" + project + "/" + project + "/"
    f = open(path + "__init__.py", "w+")
    # TODO Add Entities
    f.write("from flask import Flask\nfrom flask_sqlalchemy import SQLAlchemy\nfrom flask_marshmallow import Marshmallow\nfrom flask_cors import CORS\n\napp = Flask(__name__)\napp.config.from_object('" + project + "config')\nCORS(app)\ndb = SQLAlchemy(app)\nma = Marshmallow(app)\n\nfrom test.controllers import index")
    tempstr = ""
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            modelname = coll[(coll.find("/")+1):]
            tempstr += (modelname + ", ")
            f.write(", " + modelname)
    f.write("\n")
    f.close()
    path = "../projects/src/" + project + "/" + project + "/controllers/"
    f = open(path + "__init__.py", "w+")
    f.write("from test import app\n")
    f.close()
    f = open(path + "index.py", "w+")
    # TODO Add Entities
    f.write("from " + project + " import app, db\nfrom " + project + ".models import ")
    print('test', tempstr)
    f.write(tempstr[:-2] + "\nfrom flask import jsonify\n\n@app.route('/config/init/')\ndef init_database():\n    db.drop_all()\n    db.create_all()\n    db.session.commit()\n    return jsonify(['ok'])\n")
    f.close()
    path = "../projects/src/" + project + "/" + project + "/models/"
    f = open(path + "__init__.py", "w+")
    f.write("from test import app\n")
    f.close()
