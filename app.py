from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db


@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to Algoapp! I am running inside {} pod!".format(hostname)
    )


@app.route("/names")
def get_all_names():
    #stri=db.test.find_one({'name':'allo'})
    stri=db.dev.find()
    return str(stri)

@app.route("/name", methods=["POST"])
def create_name():
    posts=db.deb
    data = request.get_json(force=True)
    posts.insert_one({"name": data["name"]})
    return "Name saved successfully!"
    


@app.route("/name/<id>", methods=["PUT"])
def update_name(id):
    data = request.get_json(force=True)["name"]
    response = db.name.update_one({"_id": ObjectId(id)}, {"$set": {"name": data}})
    if response.matched_count:
        message = "Name updated successfully!"
    else:
        message = "No Name found!"
    return jsonify(
        message=message
    )


@app.route("/name/<id>", methods=["DELETE"])
def delete_name(id):
    response = db.name.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Name deleted successfully!"
    else:
        message = "No Name found!"
    return jsonify(
        message=message
    )


@app.route("/name/delete", methods=["POST"])
def delete_all_names():
    db.name.remove()
    return jsonify(
        message="All Names deleted!"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
