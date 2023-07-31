#!/usr/bin/python3
"""
User view for API.
"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Returns JSON of all User objects"""
    users = [user.to_dict() for user in storage.all('User').values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns JSON of a specific User object"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object given its ID"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing User object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get('User', user_id)
    if not user:
        abort(404)

    # Ignore keys: id, email, created_at, and updated_at
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
