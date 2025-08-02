import pytest
from app.main import app
from app.models import url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Reset the url_store before each test
    url_store._urls = {}
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post('/api/shorten', json={'url': 'http://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6

def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid URL'

def test_redirect_success(client):
    # First, shorten a URL
    post_response = client.post('/api/shorten', json={'url': 'http://example.com'})
    short_code = post_response.get_json()['short_code']

    # Then, redirect
    get_response = client.get(f'/{short_code}')
    assert get_response.status_code == 302
    assert get_response.location == 'http://example.com'

def test_redirect_not_found(client):
    response = client.get('/invalid')
    assert response.status_code == 404

def test_get_stats_success(client):
    # First, shorten a URL
    post_response = client.post('/api/shorten', json={'url': 'http://example.com'})
    short_code = post_response.get_json()['short_code']

    # Then, get stats
    get_response = client.get(f'/api/stats/{short_code}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data['url'] == 'http://example.com'
    assert 'created_at' in data
    assert data['clicks'] == 0

def test_get_stats_not_found(client):
    response = client.get('/api/stats/invalid')
    assert response.status_code == 404

def test_click_increment(client):
    # First, shorten a URL
    post_response = client.post('/api/shorten', json={'url': 'http://example.com'})
    short_code = post_response.get_json()['short_code']

    # Click the link twice
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')

    # Check the stats
    get_response = client.get(f'/api/stats/{short_code}')
    data = get_response.get_json()
    assert data['clicks'] == 2