#!/usr/bin/python3
""" Places CRUD Operations"""
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models import storage as s
from models.city import City
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieves all places"""
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    places = [p.to_dict() for p in c.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves place by Id
    """
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)
    return jsonify(pl.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes Place
    """
    pl = s.get(Place, place_id)
    if not pl:
        abort(404)
    s.delete(pl)
    s.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a place in City
    """
    city = s.get(City, city_id)
    if not city:
        abort(404)
    d = request.get_json()
    if not d:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in d:
        return jsonify({"error": "Missing user_id"}), 400
    user = s.get(User, d["user_id"])
    if not user:
        abort(404)
    if "name" not in d:
        return jsonify({"error": "Missing name"}), 400
    d["city_id"] = city_id
    pl = Place(**data)
    pl.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place
    """
    place = s.get(Place, place_id)
    if not place:
        abort(404)
    d = request.get_json()
    if not d:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in d.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(pl, key, value)
    pl.save()
    return jsonify(pl.to_dict()), 200


# Searching
@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """
    Search places
    """
    d = request.get_json()
    if d is None:
        abort(400, "Not a JSON")

   if not d or (not d.get("states") and not
                    d.get("cities") and not d.get("amenities")):
        pls = s.all(Place).values()
    else:
        pls = []
        if d.get("states"):
            pls.extend(get_places_from_states(d))

        if d.get("cities"):
            pls = get_places_from_cities(pls, d)

        if data.get("amenities"):
            if not pls:
                pls = s.all(Place).values()
            pls = filter_places_by_amenities(pls, d["amenities"])
    # resolving the unserialized amenities issue
    pls_dicts = [p.to_dict() for p in pls]
    for p_dt in pls_dicts:
        p_dt.pop('amenities', None)

    return jsonify(pls_dicts)


def get_places_from_states(data):
    pls = []
    for st_id in data["states"]:
        state = s.get(State, state_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    if place not in places:
                        places.append(place)
    return pls


def get_places_from_cities(places, data):
    for ct_id in data["cities"]:
        c = s.get(City, ct_id)
        if c:
            for p in city.places:
                if p not in places:
                    places.append(p)
    return places


def filter_places_by_amenities(places, amenity_ids):
    amenities = [s.get(Amenity, am_id)
                 for am_id in amenity_ids]
    return [
        place
        for place in places
        if all(am in place.amenities for am in amenities)
    ]
