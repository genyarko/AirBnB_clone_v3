#!/usr/bin/python3
"""Place view for API."""

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
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
        places_list = storage.all(Place).values()
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
        for place in places_list:
            if all(amenity_id in place.amenity_ids for amenity_id in amenities):
                filtered_places.append(place)
        places_list = filtered_places

    return jsonify([place.to_dict() for place in places_list])

