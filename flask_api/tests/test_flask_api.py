import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask_api import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_places(client):
    response = client.get('/places')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_get_places_filter_city(client):
    response = client.get('/places?city=Paris')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_search_places(client):
    response = client.get('/places/search?label=camping')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_types(client):
    response = client.get('/places/types')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_cities(client):
    response = client.get('/places/cities')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_place_not_found(client):
    response = client.get('/places/uuid-inexistant')
    assert response.status_code == 404

def test_get_ratings_not_found(client):
    response = client.get('/ratings/uuid-inexistant')
    assert response.status_code == 404