import pytest
import os
import tempfile
from src import create_app
from src.database import get_db, close_db
from init_db import init_db_main as init_test_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(config_override={
        'TESTING': True,
        'DATABASE_NAME': db_path,
    })

    with app.app_context():
        init_test_db(app.config['DATABASE_NAME'])

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_health_check(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'

def test_create_user(client):
    resp = client.post('/users', json={"name": "Test User", "email": "test@example.com", "password": "password"})
    assert resp.status_code == 201
    assert "User created" in resp.get_json()['message']

def test_create_user_duplicate_email(client):
    client.post('/users', json={"name": "Test User", "email": "test@example.com", "password": "password"})
    resp = client.post('/users', json={"name": "Another User", "email": "test@example.com", "password": "password"})
    assert resp.status_code == 409
    assert "Email already exists" in resp.get_json()['error']

def test_get_all_users(client):
    resp = client.get('/users')
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)
    assert len(resp.get_json()) == 3 # From init_db

def test_get_user(client):
    resp = client.get('/user/1')
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'John Doe'

def test_get_user_not_found(client):
    resp = client.get('/user/999')
    assert resp.status_code == 404

def test_login(client):
    resp = client.post('/login', json={"email": "john@example.com", "password": "password123"})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'success'

def test_login_wrong_password(client):
    resp = client.post('/login', json={"email": "john@example.com", "password": "wrongpassword"})
    assert resp.status_code == 401
    assert resp.get_json()['status'] == 'failed'

def test_update_user(client):
    resp = client.put('/user/1', json={"name": "John Updated", "email": "john.updated@example.com"})
    assert resp.status_code == 200
    assert "User updated" in resp.get_json()['message']

    get_resp = client.get('/user/1')
    assert get_resp.get_json()['name'] == 'John Updated'
    assert get_resp.get_json()['email'] == 'john.updated@example.com'

def test_delete_user(client):
    resp = client.delete('/user/1')
    assert resp.status_code == 200
    assert "deleted" in resp.get_json()['message']

    get_resp = client.get('/user/1')
    assert get_resp.status_code == 404

def test_search_users(client):
    resp = client.get('/search?name=John Doe')
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1
    assert resp.get_json()[0]['name'] == 'John Doe'
