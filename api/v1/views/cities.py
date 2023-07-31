#!/usr/bin/python3
"""
City view for API.
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.city import City


def get_state_or_404(state_id):
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return state


def get_city_or_404(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return city


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_for_state(state_id):
    """Returns JSON cities in a given state"""
    state = get_state_or_404(state_id)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns JSON city and id"""
    city = get_city_or_404(city_id)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city given the id"""
    city = get_city_or_404(city_id)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a city in a given state"""
    state = get_state_or_404(state_id)
    city_dict = request.get_json()
    if not city_dict:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in city_dict:
        return jsonify({'error': 'Missing name'}), 400

    city_dict['state_id'] = state.id
    city = City(**city_dict)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates an existing city"""
    city_dict = request.get_json()
    if not city_dict:
        return jsonify({'error': 'Not a JSON'}), 400
    city = get_city_or_404(city_id)
    city.name = city_dict.get('name', city.name)
    city.save()
    return jsonify(city.to_dict()), 200
