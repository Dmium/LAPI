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
            f.write("@app.route('/api/" + modelname + "', methods=['POST'])\n")
            f.write("def create_" + modelname + "():\n")
            f.write("  db.session.add(" + modelname + "(**request.get_json()))\n")
            f.write("  db.session.commit()\n")
            f.write("  return jsonify(['ok'])\n\n")
            f.write("@app.route('/api/" + modelname + "', methods=['GET'])\n")
            f.write("def read_" + modelname + "():\n")
            f.write("  return jsonify(" + modelname + ".query.all())\n\n")
            f.close()
