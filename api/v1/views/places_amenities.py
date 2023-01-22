#!/usr/bin/python3
"""
Place and Amenity api Module
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_placeAmenities(place_id):
    """ Retrieves all Amenities in a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    amenityList = []
    for amenity in amenities:
        amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity(place_id, amenity_id):
    """ Link an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    if amenities is None:
        abort(404)
    for amenity in amenities:
        # print(amenity.to_dict())
        if amenity_id in amenity.to_dict().values():
            # print("YESS!")
            return jsonify(amenity.to_dict()), 200
    amenity = storage.get(Amenity, amenity_id)
    amenities.append(amenity)  # place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        'places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_placeamenity(place_id, amenity_id):
    """ Deletes an Amenity from a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities
    for amenity in amenities:
        if amenity_id in amenity.to_dict().values():
            del amenity
            storage.save()
            return jsonify({})
    abort(404)
