#!/usr/bin/python3
"""Retrieves number for each type"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns status"""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each object by type"""
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    stats = {cls: storage.count(eval(cls)) for cls in classes}
    return jsonify(stats)
