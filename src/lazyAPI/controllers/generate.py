from lazyAPI import app, mongo
from flask import jsonify, request, Response
from bson import Binary, Code
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
import shutil

@app.route('/generate/<project>', methods=['POST'])
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
            f.write("from " + project + " import db\n")
            f.write("from " + project + " import ma\n\n")
            f.write("class " + modelname.title() + "(db.Model):\n")
            f.write("    __tablename__ = \"" + modelname + "\"\n")
            f.write("    id = db.Column(db.Integer, primary_key = True)\n")
            attributes = []
            types = []
            for documentname in mongo.db[str(coll)].find():
                for key, value in documentname.items():
                    if not(key in attributes) and not(key == "_id"):
                        attributes.append(key)
                        types.append(type(value))
            print(attributes)
            print(types)
            for i in range(len(types)):
                if str(types[i]) == "<class 'str'>":
                    types[i] = "String(100)"
                elif str(types[i]) == "<class 'int'>":
                    types[i] = "Integer"

            for i in range(len(attributes)):
                f.write("    " + attributes[i] + " = db.Column(db." + str(types[i]) + ")\n")
            f.write("\nclass " + modelname.title() + "_Schema(ma.ModelSchema):")
            f.write("\n    class Meta:")
            f.write("\n        fields = ('id',)\n\n")
            f.write(modelname + "_schema" + " = " + modelname.title() + "_Schema()\n")
            f.write(modelname + "_schemas" + " = " + modelname.title() + "_Schema(many=True)\n")
    return "ok"
