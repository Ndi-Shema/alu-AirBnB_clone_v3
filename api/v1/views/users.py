#!/usr/bin/python3
"""
This module defines routes for managing User objects using Flask.
"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        A JSON response containing the list of User objects.
    """
    users = storage.all(User).values()
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object.

    Args:
        user_id (str): The ID of the User object to retrieve.

    Returns:
        A JSON response containing the User object.

    Raises:
        404: If no User object with the given ID is found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.

    Args:
        user_id (str): The ID of the User object to delete.

    Returns:
        An empty JSON response.

    Raises:
        404: If no User object with the given ID is found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User object.

    Returns:
        A JSON response containing the created User object.

    Raises:
        400: If the request does not contain a valid JSON body, or if the JSON body is missing
             the required 'email' or 'password' fields.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    req_body = request.get_json()
    object = User(**req_body)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.

    Args:
        user_id (str): The ID of the User object to update.

    Returns:
        A JSON response containing the updated User object.

    Raises:
        404: If no User object with the given ID is found.
        400: If the request does not contain a valid JSON body.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "email", "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(user, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
