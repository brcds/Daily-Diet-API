import bcrypt
import pytest
import os

from app import app, db
from models.user import User
from dotenv import load_dotenv

# CRUD
BASE_URL = 'http://127.0.0.1:5000'

tasks = []

os.environ['FLASK_ENV'] = 'testing'
load_dotenv(dotenv_path=".env.testing")


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def create_test_user(client):
    password = bcrypt.hashpw(b'teste', bcrypt.gensalt()).decode("utf-8")
    user = User(username="teste", password=password)
    db.session.add(user)
    db.session.commit()
    return user


def login(client, username, password):
    return client.post(f"{BASE_URL}/login", json={"username": username, "password": password})


## Meals tests
@pytest.fixture
def create_meal(client, create_test_user):
    response = login(client, "teste", "teste")
    assert response.status_code == 200

    meal = {
        "name": "testeName",
        "description": "testeDescription",
        "is_in_diet": "False"
    }
    response = client.post(BASE_URL + '/meal', json=meal)
    assert response.status_code == 200

    meal_1 = {
        "name": "testeName1",
        "description": "testeDescription2",
        "is_in_diet": "False"
    }
    response = client.post(BASE_URL + '/meal', json=meal_1)
    assert response.status_code == 200
    return response.get_json()


def test_create_meal(client, create_test_user):
    response = login(client, "teste", "teste")
    assert response.status_code == 200
    meal = {
        "name": "testeName",
        "description": "testeDescription",
        "is_in_diet": "False"
    }
    response = client.post(BASE_URL + '/meal', json=meal)
    assert response.status_code == 200


def test_get_meals(client, create_meal):
    response = login(client, "teste", "teste")
    assert response.status_code == 200

    response = client.get(f"{BASE_URL}/meal")
    assert response.status_code == 200

    data = response.get_json()
    assert 'meals' in data
    assert len(data['meals']) == 2


def test_get_meal(client, create_meal):
    response = login(client, "teste", "teste")
    assert response.status_code == 200

    response = client.get(f"{BASE_URL}/meal/1")
    assert response.status_code == 200

    data = response.get_json()
    assert 'meal' in data


def test_update_meal(client, create_meal):
    response = login(client, "teste", "teste")
    assert response.status_code == 200

    meal_id = create_meal['id']
    update_meal = {
        "name": "testeEditado",
        "description": "testeDescriptionEditado",
        "is_in_diet": "False"
    }
    response = client.put(BASE_URL + f'/meal/{meal_id}', json=update_meal)
    assert response.status_code == 200

    response = client.get(f"{BASE_URL}/meal/{meal_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["meal"]["name"] == "testeEditado"


def test_delete_meal(client, create_meal):
    response = login(client, "teste", "teste")
    assert response.status_code == 200

    meal_id = create_meal['id']

    response = client.delete(f"{BASE_URL}/meal/{meal_id}")
    assert response.status_code == 200

    response = client.get(f"{BASE_URL}/meal/{meal_id}")
    assert response.status_code == 404
