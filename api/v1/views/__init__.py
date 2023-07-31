#!/usr/bin/python3
"""
Initializes views module
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import view modules
from api.v1.views.index import *
from api.v1.views.states import *
# Import other view modules

# Register view functions with the Blueprint
app_views.add_url_rule('/stats', 'get_stats', get_stats, methods=['GET'])
app_views.add_url_rule('/states', 'get_all_states', get_all_states, methods=['GET'])
app_views.add_url_rule('/states/<state_id>', 'get_state', get_state, methods=['GET'])
app_views.add_url_rule('/states/<state_id>', 'delete_state', delete_state, methods=['DELETE'])
app_views.add_url_rule('/states', 'create_state', create_state, methods=['POST'])
app_views.add_url_rule('/states/<state_id>', 'update_state', update_state, methods=['PUT'])
# Add other view functions and rules
