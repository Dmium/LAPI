"""
Generates a project based on contents on the mongo database and developer settings
"""
from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
import shutil

@app.route('/generate', methods=['GET'])
def generate():
    path = "../projects/src/"
    if(os.path.exists(path)):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    os.makedirs(path + "/models/")
    for coll in mongo.db.collection_names():
        if coll.startswith('api'):
            modelname = coll[(coll.find("/")+1):]
            f = open(path + "/models/" + modelname + ".py", "w+")
            f.write("from "+ " import db, ma\n\n")
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
    generate_controllers('api')
    generate_configs()
    return "ok"

def generate_controllers(project):
    path = "../projects/src/"
    os.makedirs(path+ "/controllers/")
    for coll in mongo.db.collection_names():
        if coll.startswith(project):
            modelname = coll[(coll.find("/")+1):]
            f = open(path+ "/controllers/" + modelname + ".py", "w+")
            f.write("from "+ " import db, ma, app\n")
            f.write("from flask import jsonify, request, make_response\n")
            f.write("from "+ ".models." + modelname + " import " + modelname + ", " + modelname + "_schema, " + modelname + "_schemas\n\n")
            f.write("@app.route('/"+ "/" + modelname + "', methods=['POST'])\n")
            f.write("def create_" + modelname + "():\n")
            f.write("    tempmodel = " + modelname + "(**request.get_json())\n")
            f.write("    db.session.add(tempmodel)\n")
            f.write("    db.session.commit()\n")
            f.write("    return jsonify(" + modelname + "_schema.dump(tempmodel).data)\n\n")
            f.write("@app.route('/"+ "/" + modelname + "', methods=['GET'])\n")
            f.write("def read_" + modelname + "():\n")
            f.write("    return jsonify(" + modelname + "_schemas.dump(" + modelname + ".query.all()).data)\n\n")
            f.write("@app.route('/"+ "/" + modelname + "/<id>', methods=['GET'])\n")
            f.write("def read_single_" + modelname + "(id):\n")
            f.write("    return jsonify(" + modelname + "_schema.dump(" + modelname + ".query.filter_by(id = id).first()))\n\n")
            f.write("@app.route('/"+ "/" + modelname + "/<id>', methods=['DELETE'])\n")
            f.write("def delete_" + modelname + "(id):\n")
            f.write("    rdict = request.get_json()\n")
            f.write("    db.session.delete(" + modelname + ".query.filter_by(id = rdict['id']).first())\n")
            f.write("    db.session.commit()\n")
            f.write("    return jsonify(['ok'])\n\n")
            f.close()

def generate_configs():
    path = "../projects/src/"
    f = open(path + "setup.bat", "w+")
    f.write("set FLASK_APP="+ "\npip install -e .\nflask run\n")
    f.close()
    f = open(path + "setup.sh", "w+")
    f.write("export FLASK_APP="+ "\nexport FLASK_ENV=development\nsudo pip3 install -e .\nflask run\n")
    f.close()
    f = open(path + "setup.py", "w+")
    f.write("from setuptools import setup\nsetup(\n    name='"+ "',\n    packages=['"+ "',\n              '"+ ".controllers'],\n    include_package_data=True,\n    install_requires=[\n        'flask',\n        'flask-cors',\n        'flask-sqlalchemy',\n        'flask-marshmallow',\n        'marshmallow-sqlalchemy'\n    ],\n)")
    f.close()
    f = open(path+ "config.py", "w+")
    f.write('DEBUG = True\nSQLALCHEMY_DATABASE_URI = "postgresql://dom@localhost/'+ '"\nSQLALCHEMY_TRACK_MODIFICATIONS = True\nDATABASE_CONNECT_OPTIONS = {}\nTHREADS_PER_PAGE = 2\n')
    f.close()
    path = "../projects/src/"+ "/"+ "/"
    f = open(path + "__init__.py", "w+")
    # TODO Add Entities
    f.write("from flask import Flask\nfrom flask_sqlalchemy import SQLAlchemy\nfrom flask_marshmallow import Marshmallow\nfrom flask_cors import CORS\n\napp = Flask(__name__)\napp.config.from_object('"+ "config')\nCORS(app)\ndb = SQLAlchemy(app)\nma = Marshmallow(app)\n\nfrom "+ ".controllers import index")
    tempstr = ""
    for coll in mongo.db.collection_names():
        if coll.startswith('api'):
            modelname = coll[(coll.find("/")+1):]
            tempstr += (modelname + ", ")
            f.write(", " + modelname)
    f.write("\n")
    f.close()
    path = "../projects/src/"+ "/"+ "/controllers/"
    f = open(path + "__init__.py", "w+")
    f.write("from "+ " import app\n")
    f.close()
    f = open(path + "index.py", "w+")
    # TODO Add Entities
    f.write("from "+ " import app, db\nfrom "+ ".models import ")
    print('"+ "', tempstr)
    f.write(tempstr[:-2] + "\nfrom flask import jsonify\n\n@app.route('/config/init/')\ndef init_database():\n    db.drop_all()\n    db.create_all()\n    db.session.commit()\n    return jsonify(['ok'])\n")
    f.close()
    path = "../projects/src/"+ "/"+ "/models/"
    f = open(path + "__init__.py", "w+")
    f.write("from "+ " import app\n")
    f.close()
