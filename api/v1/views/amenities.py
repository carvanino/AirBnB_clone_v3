#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from models import storage
from flask import make_response, request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def amenities():
    """return amenities"""
    amenities = storage.all(Amenity)

    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_id(amenity_id):
    """return the a aparticular amenity amenities"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a particular amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_amenity():
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")

    if "name" not in new_amenity:
        abort(400, "Missing name")

    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    for k, v in update.items():
        if k != id or k != "created_at" or k != "updated_at":
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
