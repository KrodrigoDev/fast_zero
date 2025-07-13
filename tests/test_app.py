from datetime import datetime
from http import HTTPStatus

from fast_zero.schema import UserPublic


def test_main(client):
    """
    Esse test tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garante que A é A
    """
    # client = arrange

    # Act
    response = client.get('/')

    # Assert
    assert response.text == '<h1>Hello World, User</h1>'
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    user = {
        'first_name': 'string',
        'last_name': 'string',
        'birthday': '2003-07-25',
        'email': 'user@example.com',
        'password': 'batatinha123',
    }

    response = client.post('/created_user', json=user)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['email'] == 'user@example.com'


def test_read_peoples(client, user):
    response = client.get('/list_users')

    assert len(response.json()['users']) >= 1


def test_people_is_people(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/list_users')

    data = response.json()

    for raw_user in data['users']:
        raw_user['birthday'] = datetime.strptime(
            raw_user['birthday'], '%Y-%m-%d'
        ).date()

    assert response.status_code == HTTPStatus.OK
    assert data == {'users': [user_schema]}


def test_read_people(client, user):
    response = client.get('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert type(response.json()['first_name']) is str


def test_update_user(client, user):
    response = client.put(
        '/update_users/1',
        json={
            'first_name': 'string teste',
            'last_name': 'string teste',
            # 'birthday': '2025-06-09',  # dar um jeito de atualizar a idade
            'email': 'saddssada@gmail.com',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_peoples(client, user):
    response = client.delete('/delete_user/1')

    assert response.status_code == HTTPStatus.OK


def test_error_update_user(client):
    response = client.put(
        '/update_users/190',
        json={
            'first_name': 'string teste',
            'last_name': 'string teste',
            'birthday': '2025-06-09',
            'email': 'saddssada@gmail.com',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_error_delete_user(client):
    response = client.delete('/delete_user/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
