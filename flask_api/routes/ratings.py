from flask import Blueprint, jsonify
from flask_api.database import Database
from flask_api.config import Config

bp = Blueprint('ratings', __name__)
db = Database()

@bp.route('/ratings/<uuid>', methods=['GET'])
def get_ratings(uuid):
    """
    Récupère les avis (ratings) associés à un lieu.

    Args:
        uuid (str): identifiant unique du lieu

    Returns:
        JSON: liste des avis ou erreur 404 si aucun résultat
    """
    collection = db.get_collection(Config.COLLECTION_RATINGS)
    ratings = list(collection.find({'uuid': uuid}, {'_id': 0}))
    if not ratings:
        return jsonify({'error': 'no ratings found'}), 404
    return jsonify(ratings)