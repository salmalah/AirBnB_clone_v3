#!/usr/bin/python3
""" Users CRUD Operations"""
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage as s 


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Retrieves all users"""
    users = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates new user"""
    d = request.get_json()
    if not d:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in d:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in d:
        return jsonify({"error": "Missing password"}), 400
    us = User(**d)
    us.save()
    return jsonify(us.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves user by id"""
    u = s.get(User, user_id)
    if u:
        return jsonify(u.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes User"""
    u = s.get(User, user_id)
    if user:
        s.delete(u)
        s.save()
        return jsonify({}), 200
    abort(404)



@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates User
    """
    us = s.get(User, user_id)
    if not us:
        abort(404)
    d = request.get_json()
    if not d:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in d.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(us, key, value)
    us.save()
    return jsonify(us.to_dict()), 200
