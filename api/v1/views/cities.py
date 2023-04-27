#!/usr/bin/python3
"""Flask module containing routes for CRUD operations on City objects."""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_of_state(state_id):
    """
    Retrieves a list of City objects that belong to a specific State object based on the provided state_id.

    If the state does not exist, a 404 error will be returned.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    list_cities = []
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """
    Retrieves a specific City object based on the provided city_id.

    If the city does not exist, a 404 error will be returned.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a specific City object based on the provided city_id.

    If the city does not exist, a 404 error will be returned.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object and assigns it to a specific State object based on the provided state_id.

    If the state does not exist, a 404 error will be returned.
    If the request does not contain a JSON object or is missing required fields, a 400 error will be returned.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    req_body = request.get_json()
    req_body["state_id"] = state.id

    # Create a new City object
    city_obj = City(**req_body)
    storage.new(city_obj)
    storage.save()

    return make_response(jsonify(city_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates an existing City object based on the provided city_id.

    If the city does not exist, a 404 error will be returned.
    If the request does not contain a JSON object or is missing required fields, a 400 error will be returned.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "state_id" "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(city, key, value)
        else:
            pass

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
