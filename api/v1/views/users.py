#!/usr/bin/python3
"""APi users"""
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage as s


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieves all users"""
    users = [u.to_dict() for u in s.all(User).values()]
    return jsonify(users)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates new user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves user by its id"""
    user = s.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes User by its id"""
    user = s.get(User, user_id)
    if user:
        s.delete(user)
        s.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates User"""
    user = s.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
