#!/usr/bin/python3
"""Places"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getallplaces(city_id=None):
    """Gets all places"""
    if city_id is None:
        abort(404)

    res = []
    for i in storage.all("Place").values():
        res.append(i.to_dict())

    return jsonify(res)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getplaces(place_id=None):
    """Gets a place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(place_id=None):
    """Deletes a place"""
    s = storage.get("Place", place_id)
    if s is None:
        abort(404)
    else:
        storage.delete(s)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createplaces(city_id=None):
    """Create a place"""
    checker = set()
    for i in storage.all("City").values():
        finder.add(i.id)
    if city_id not in checker:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")

    user = s.get("user_id")
    if user is None:
        abort(400, "Missing user_id")
    checker = set()
    for i in storage.all("User").values():
        checker.add(i.id)
    if user not in checker:
        abort(404)

    if "name" not in s.keys():
        abort(400, "Missing name")

    s["city_id"] = city_id
    new_s = place.Place(**s)
    storage.new(new_s)
    storage.save()
    return jsonify(new_s.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updateplaces(place_id=None):
    """Update a place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200


@app_views.route('/api/v1/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on the JSON in the request body"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places_list = []

    if not states and not cities:
        places_list = storage.all(place.Place).values()
    else:
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                places_list.extend(state.cities)
        for city_id in cities:
            city = storage.get('City', city_id)
            if city:
                places_list.extend(city.places)

    if amenities:
        filtered_places = []
        for place_obj in places_list:
            if all(amenity_id in place_obj.amenity_ids for amenity_id in amenities):
                filtered_places.append(place_obj)
        places_list = filtered_places

    return jsonify([place_obj.to_dict() for place_obj in places_list])
