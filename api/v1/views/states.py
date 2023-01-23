#!/usr/bin/python
"""iew for State objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in all_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """return a single state passed"""
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state_id(state_id):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ Creates a State object """
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state_id(state_id):
    """ Updates a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    my_dict = request.get_json()
    if not my_dict:
        abort(400, "Not a JSON")
    for key, value in my_dict.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
