#!/usr/bin/python3
"""Defines views for the Review resource."""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieve a list of all Review objects associated with a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]

    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review object associated with a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    if "user_id" not in req_body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user_id = req_body["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "text" not in req_body:
        return make_response(jsonify({"error": "Missing text"}), 400)

    req_body["place_id"] = place.id
    req_body["user_id"] = user.id
    new_review = Review(**req_body)
    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object by ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req_body = request.get_json()
    exempt = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in req_body.items():
        if key not in exempt:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
