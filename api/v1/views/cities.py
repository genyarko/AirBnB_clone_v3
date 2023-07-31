#!/usr/bin/python3
"""
Cities view for API
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state, city


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Gets all cities by state ID"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)

    cities = [c.to_dict() for c in s.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """Gets a city"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a city"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)
    storage.delete(c)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a city"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    new_city = city.City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """Update a city"""
    c = storage.get("City", city_id)
    if c is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(c, key, value)

    storage.save()
    return jsonify(c.to_dict()), 200
