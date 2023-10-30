from myapp import app, mongo

from flask import render_template, request, jsonify

from bson.objectid import ObjectId

@app.route("/")
def display_template():
	return "<h1>HOMEPAGE</h1>"
	# return render_template("index.html")

@app.route("/users", methods=["POST"])
def create_user():
	name = request.json["name"]
	lastname = request.json["lastname"]
	try:
		user = {"name": name, "lastname": lastname}
		dbResponse = mongo.db.users.insert_one(user)
		# for attr in dir(dbResponse):
		# 	print(attr)
		return jsonify({"message": "user created", "_id": f"{dbResponse.inserted_id}"}), 201
	except Exception as ex:
		return jsonify({"message": "unable to create"}), 500

@app.route("/users", methods=["GET"])
def get_users():
	try:
		data = list(mongo.db.users.find({}))
		for user in data:
			user["_id"] = str(user["_id"])
		return jsonify(data), 200
	except Exception as ex:
		return jsonify({"message": "Cannot get users"}), 500
	
@app.route("/users/<userId>", methods=["PATCH"])
def update_user(userId):
	name = request.json["name"]
	lastname = request.json["lastname"]
	try:
		dbResponse = mongo.db.users.update_one({"_id": ObjectId(userId)}, {"$set": {"name": name, "lastname": lastname}})
		# for attr in dir(dbResponse):
			# print(attr)
		if dbResponse.modified_count == 1:
			return jsonify({"message": "user updated"}), 200
		return jsonify({"message": "nothing to update"}), 200	
	except Exception as ex:
		return jsonify({"message": "cannot update user"}), 500
	
@app.route("/users/<userId>", methods=["DELETE"])
def delete_user(userId):
	try:
		dbResponse = mongo.db.users.delete_one({"_id": ObjectId(userId)})
		# for attr in dir(dbResponse):
			# print(attr)
		if dbResponse.deleted_count == 1:	
			return jsonify({"message": "user deleted"}), 200
		return jsonify({"message": "user not found", "_id": f"{userId}"}), 400
	except Exception as ex:
		return jsonify({"message": "cannot delete user"}), 500