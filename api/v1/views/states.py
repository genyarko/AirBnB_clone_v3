#!/usr/bin/python3
"""
States view for API
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Gets all states"""
    states = [s.to_dict() for s in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Gets a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    return jsonify(s.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    storage.delete(s)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a state"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_state = state.State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Update a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(s, key, value)

    storage.save()
    return jsonify(s.to_dict()), 200
