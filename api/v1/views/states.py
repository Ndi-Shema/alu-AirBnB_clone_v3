#!/usr/bin/python3

"""This module implements Flask API endpoints for managing State objects."""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrieve a list of all State objects.

    HTTP request: GET /api/v1/states
    Response: JSON format
    """
    states = storage.all(State).values()
    list_states = []
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """
    Retrieve a specific State object by its ID.

    HTTP request: GET /api/v1/states/<state_id>
    Response: JSON format
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Delete a State object by its ID.

    HTTP request: DELETE /api/v1/states/<state_id>
    Response: empty JSON object with status code 200
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new State object.

    HTTP request: POST /api/v1/states
    Response: JSON format with new State object and status code 201
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    req_body = request.get_json()
    object = State(**req_body)
    storage.new(object)
    storage.save()
    return make_response(jsonify(object.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(state, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
