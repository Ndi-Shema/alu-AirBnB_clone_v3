#!/usr/bin/python3
"""Module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import make_response, abort, request
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    req_body = request.get_json()
    object = Amenity(**req_body)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(amenity, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
