from flask import Blueprint, jsonify
from flask_api.database import Database
from flask_api.config import Config

bp = Blueprint('ratings', __name__)
db = Database()

@bp.route('/ratings/<uuid>', methods=['GET'])
def get_ratings(uuid):
    collection = db.get_collection(Config.COLLECTION_RATINGS)
    ratings = list(collection.find({'uuid': uuid}, {'_id': 0}))
    if not ratings:
        return jsonify({'error': 'no ratings found'}), 404
    return jsonify(ratings)