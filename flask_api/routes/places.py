from flask import Blueprint, jsonify, request
from flask_api.database import Database
from flask_api.config import Config

bp = Blueprint('places', __name__)
db = Database()

@bp.route('/places', methods=['GET'])
def get_places():
    collection = db.get_collection(Config.COLLECTION_CLEAN)
    city = request.args.get('city')
    type_ = request.args.get('type')

    query = {}
    if city:
        query['address.addressLocality'] = city
    if type_:
        query['type'] = type_

    places = list(collection.find(query, {'_id': 0}).limit(20))
    return jsonify(places)


@bp.route('/places/<uuid>', methods=['GET'])
def get_place(uuid):
    collection = db.get_collection(Config.COLLECTION_CLEAN)
    place = collection.find_one({'uuid': uuid}, {'_id': 0})
    if not place:
        return jsonify({'error': 'not found'}), 404
    return jsonify(place)


@bp.route('/places/search', methods=['GET'])
def search_places():
    collection = db.get_collection(Config.COLLECTION_CLEAN)
    label = request.args.get('label', '')
    places = list(collection.find(
        {'label': {'$regex': label, '$options': 'i'}},
        {'_id': 0}
    ).limit(20))
    return jsonify(places)


@bp.route('/places/types', methods=['GET'])
def get_types():
    collection = db.get_collection(Config.COLLECTION_CLEAN)
    types = collection.distinct('type')
    return jsonify(types)


@bp.route('/places/cities', methods=['GET'])
def get_cities():
    collection = db.get_collection(Config.COLLECTION_CLEAN)
    cities = collection.distinct('address.addressLocality')
    return jsonify(cities)