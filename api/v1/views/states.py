#!/usr/bin/python3
"""
"""
import models
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes = False)
def get_states():
    """ Retrieves the list of all State objects """
    states = models.storage.all(State)
    stateList = []
    for state in states.values():
        stateList.append(state.to_dict())
    return jsonify(stateList)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieve a state object by id """
    states = models.storage.all(State)
    for state in states.values():
        if state_id in state.to_dict().values():
            return jsonify(state.to_dict())
    abort(404)

@app_views.route('/states/', methods=['POST'])
def create_state():
    """ Create a new instance of state """
    if not request.json:
        abort(404, description='Not a JSON')
    if not 'name' in request.json:
        abort(404, description='Missing name')
    state = request.get_json()
    new_state = State(**state) # initialized as kwargs
    new_state.save()
    #return make_response(jsonify(new_state.to_dict()), 201)
    # both works 
    return (jsonify(new_state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates the attribute of a state object """
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(404, description='Not a JSON')
    stateAttr = request.get_json()
    for key, value in stateAttr.items():
        if key != 'id' or 'created_at' or 'updated_at':
            # for k, v in stateAttr.items():
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    return jsonify({})
