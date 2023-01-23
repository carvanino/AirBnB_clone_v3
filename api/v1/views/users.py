#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models import storage
from flask import make_response, request, jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """return all users"""
    users = storage.all(User)

    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """return the a aparticular amenity amenities"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a particular amenity"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/user', methods=['POST'], strict_slashes=False)
def new_user():
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")

    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a amenity"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    for k, v in update.items():
        if k != id or k != "created_at" or k != "updated_at" or k != "email":
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

