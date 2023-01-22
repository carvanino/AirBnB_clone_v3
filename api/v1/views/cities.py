#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models import storage
from models.city import city
from flask import make_response, request, jsonify, abort
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def state_cities(state_id):
    """return the states of a particulat city"""

