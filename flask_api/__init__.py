from flask import Flask
from flask_api.routes.places import bp as places_bp
from flask_api.routes.ratings import bp as ratings_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(places_bp)
    app.register_blueprint(ratings_bp)
    return app