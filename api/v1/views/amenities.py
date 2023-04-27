#!/usr/bin/python3
"""
This module defines views for Amenity objects.
"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        A JSON response with a list of all Amenity objects in the database.
    """
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """
    Retrieves a specific Amenity object.

    Args:
        amenity_id (str): The ID of the Amenity object to retrieve.

    Returns:
        A JSON response with the specified Amenity object or a 404 error
        if the Amenity object doesn't exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a specific Amenity object.

    Args:
        amenity_id (str): The ID of the Amenity object to delete.

    Returns:
        An empty JSON response with a 200 status code if the deletion was
        successful, or a 404 error if the Amenity object doesn't exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.

    Returns:
        A JSON response with the newly created Amenity object and a 201
        status code, or a JSON response with an error message and a 400
        status code if the request body is invalid or missing a required
        field.
    """
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
    """
    Updates a specific Amenity object.

    Args:
        amenity_id (str): The ID of the Amenity object to update.

    Returns:
        A JSON response with the updated Amenity object and a 200 status
        code, or a 404 error if the Amenity object doesn't exist, or a
        JSON response with an error message and a 400 status code if the
        request body is invalid.
    """
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
