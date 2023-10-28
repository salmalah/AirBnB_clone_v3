#!/usr/bin/python3
"""Amenity CRUD Operations"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage as s


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve all Amenities"""
    amets = s.all(Amenity).values()
    return jsonify([am.to_dict() for am in amets])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve amenity with Id"""
    amet = s.get(Amenity, amenity_id)
    if not amet:
        abort(404)
    return jsonify(amet.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity"""
    amet = s.get(Amenity, amenity_id)
    if not amet:
        abort(404)
    s.delete(amet)
    s.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create new aenity"""
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in js_data:
        return jsonify({"error": "Missing name"}), 400
    amet = Amenity(**js_data)
    amet.save()
    return jsonify(amet.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity"""
    amet = s.get(Amenity, amenity_id)
    if not amet:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in js_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amet, key, value)
    amet.save()
    return jsonify(amet.to_dict()), 200
