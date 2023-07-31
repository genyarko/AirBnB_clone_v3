#!/usr/bin/python3
"""
Place view for API.
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches for Place objects based on JSON request"""
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    states_list = data.get('states', [])
    cities_list = data.get('cities', [])
    amenities_list = data.get('amenities', [])

    places = []

    if not states_list and not cities_list:
        # Retrieve all places if no states or cities specified
        places = storage.all(Place).values()
    else:
        for state_id in states_list:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
        for city_id in cities_list:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    # Filter places based on amenities
    filtered_places = []
    for place in places:
        if all(storage.get(Amenity, amenity_id) in place.amenities for amenity_id in amenities_list):
            filtered_places.append(place)

    result = [place.to_dict() for place in filtered_places]
    return jsonify(result)
