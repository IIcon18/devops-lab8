from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Sidor Sidorov',
        'email': 's.sidorov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert response.json()['name'] == new_user['name']
    assert response.json()['email'] == new_user['email']
    assert 'id' in response.json()  # Проверка, что возвращается id

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user_email = users[0]['email']
    new_user = {
        'name': 'Duplicate User',
        'email': existing_user_email
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409
    assert response.json() == {'detail': 'Email already in use'}

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete_email = users[1]['email']
    response = client.delete("/api/v1/user", params={'email': user_to_delete_email})
    assert response.status_code == 204

    # Проверяем, что пользователь больше недоступен
    response = client.get("/api/v1/user", params={'email': user_to_delete_email})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}