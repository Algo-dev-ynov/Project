import pytest
import sys
import os

"""
Tests d'intégration pour les endpoints de l'API Flask.

Ces tests vérifient le bon fonctionnement des routes principales
liées aux lieux (places) et aux avis (ratings).
"""

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask_api import create_app

@pytest.fixture
def client():
    """
    Crée un client de test Flask.

    Returns:
        FlaskClient: client permettant de tester les endpoints
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_places(client):
    """
    Vérifie que l'endpoint /places retourne une liste de lieux.
    """
    response = client.get('/places')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_get_places_filter_city(client):
    """
    Vérifie le filtrage des lieux par ville.
    """
    response = client.get('/places?city=Paris')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_search_places(client):
    """
    Vérifie la recherche de lieux par label.
    """
    response = client.get('/places/search?label=camping')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_types(client):
    """
    Vérifie la récupération des types de lieux.
    """
    response = client.get('/places/types')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_cities(client):
    """
    Vérifie la récupération des villes.
    """
    response = client.get('/places/cities')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_place_not_found(client):
    """
    Vérifie le cas où un lieu n'existe pas (404).
    """
    response = client.get('/places/uuid-inexistant')
    assert response.status_code == 404

def test_get_ratings_not_found(client):
    """
    Vérifie le cas où aucun avis n'est trouvé (404).
    """
    response = client.get('/ratings/uuid-inexistant')
    assert response.status_code == 404