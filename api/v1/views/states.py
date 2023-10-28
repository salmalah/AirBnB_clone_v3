#!/usr/bin/python3
"""
CRUD Operations for States
"""
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage as s


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve a list of all State"""
    states = s.all(State).values()
    return jsonify([n.to_dict() for n in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieve a State object by its ID"""
    state = s.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object by its ID"""
    state = s.get(State, state_id)
    if not state:
        abort(404)
    s.delete(state)
    s.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new object State"""
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in js_data:
        return jsonify({"error": "Missing name"}), 400
    state = State(**js_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update a State object by its ID"""
    state = s.get(State, state_id)
    if not state:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in js_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
