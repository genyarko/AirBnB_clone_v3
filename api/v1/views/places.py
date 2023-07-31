#!/usr/bin/python3
"""Places"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place, city, user


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city_obj = storage.get(city.City, city_id)
    if city_obj is None:
        abort(404)
    places = [place.to_dict() for place in city_obj.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city_obj = storage.get(city.City, city_id)
    if city_obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")

    user_id = s.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    user_obj = storage.get(user.User, user_id)
    if user_obj is None:
        abort(404)

    if "name" not in s.keys():
        abort(400, "Missing name")

    s["city_id"] = city_id
    new_place = place.Place(**s)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")

    for k, v in s.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, k, v)

    storage.save()
    return jsonify(place_obj.to_dict()), 200
