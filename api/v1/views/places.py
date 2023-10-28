#!/usr/bin/python3
"""Places CRUD Operations"""
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models import storage as s
from models.city import City
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views

class DataManager:
    @staticmethod
    def get_object_or_abort(model, obj_id):
        obj = s.get(model, obj_id)
        if not obj:
            abort(404)
        return obj

    @staticmethod
    def create_place(city_id, data):
        city = DataManager.get_object_or_abort(City, city_id)
        user_id = data.get("user_id")
        user = DataManager.get_object_or_abort(User, user_id)
        if "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        data["city_id"] = city_id
        data["user_id"] = user_id
        place = Place(**data)
        place.save()
        return place

    @staticmethod
    def filter_places_by_amenities(places, amenity_ids):
        amenities = [s.get(Amenity, am_id) for am_id in amenity_ids]
        return [place for place in places if all(am in place.amenities for am in amenities)]

    @staticmethod
    def get_places_from_states(state_ids):
        result_places = []
        for state_id in state_ids:
            state = DataManager.get_object_or_abort(State, state_id)
            for city in state.cities:
                for place in city.places:
                    if place not in result_places:
                        result_places.append(place)
        return result_places

    @staticmethod
    def get_places_from_cities(city_ids):
        result_places = []
        for city_id in city_ids:
            city = DataManager.get_object_or_abort(City, city_id)
            for place in city.places:
                if place not in result_places:
                    result_places.append(place)
        return result_places

data_manager = DataManager()

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """Retrieves all places"""
    city = DataManager.get_object_or_abort(City, city_id)
    places = [p.to_dict() for p in city.places]
    return jsonify(places)

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves place by Id"""
    place = DataManager.get_object_or_abort(Place, place_id)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes Place"""
    place = DataManager.get_object_or_abort(Place, place_id)
    s.delete(place)
    s.save()
    return jsonify({}), 200

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates a place in City"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    place = data_manager.create_place(city_id, data)
    return jsonify(place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = DataManager.get_object_or_abort(Place, place_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """Search places"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    places = s.all(Place).values()
    if data and ("states" in data or "cities" in data or "amenities" in data):
        if "states" in data:
            places = data_manager.get_places_from_states(data["states"])
        if "cities" in data:
            places = data_manager.get_places_from_cities(data["cities"])
        if "amenities" in data:
            places = data_manager.filter_places_by_amenities(places, data["amenities"])

    places_data = [p.to_dict() for p in places]
    for p_dt in places_data:
        p_dt.pop('amenities', None)

    return jsonify(places_data)
