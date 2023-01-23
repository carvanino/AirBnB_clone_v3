#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models import storage
from models.city import City
from flask import make_response, request, jsonify, abort
from api.v1.views import app_views
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def state_cities(state_id):
    """return the states of a particulat city"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """return a particular city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """detees a city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def new_city(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    new_city = request.get_json()

    if not new_city:
        abort(400, "Not a JSON")

    if "name" not in new_city:
        abort(400, "Missing name")

    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    for k, v in update.items():
        if k != id or k != "created_at" or k != "updated_at" or k != "state_id":
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

