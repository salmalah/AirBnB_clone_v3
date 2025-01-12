#!/usr/bin/python3
"""Api cities"""
from models import storage as s
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves all cities by their state IDs"""
    state = s.get(State, state_id)
    if not state:
        abort(404)
    cities = [c.to_dict() for c in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves city object with ID"""
    city = s.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city by its ID"""
    city = s.get(City, city_id)
    if not city:
        abort(404)
    s.delete(city)
    s.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city in a State"""
    state = s.get(State, state_id)
    if not state:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in js_data:
        return jsonify({"error": "Missing name"}), 400
    js_data["state_id"] = state_id
    city = City(**js_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """UpdateS an existing city by its ID"""
    city = s.get(City, city_id)
    if not city:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in js_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
