#!/usr/bin/python3
"""Flask Api index"""
from api.v1.views import app_views
from models.review import Review
from flask import jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.state import State


@app_views.route("/status", methods=["GET"])
def status_route():
    """Returns the status"""
    if request.method == "GET":
        return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def get_stats_route():
    """Retrieves the number of each objects by type"""
    if request.method == "GET":
        statistics = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
        }
        return jsonify(statistics)
