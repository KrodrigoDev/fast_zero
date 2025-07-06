from http import HTTPStatus
from random import randint

import pandas as pd

from fast_zero.globais import PathFiles


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


def test_created_user(client):
    response = client.post(
        '/created_user/',
        json={
            'first_name': 'string',
            'last_name': 'string',
            'birthday': '2025-06-08',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['id'] > 0


def test_read_people(client):
    response = client.get('/user/0')

    assert response.status_code == HTTPStatus.OK
    assert type(response.json()['first_name']) is str


def test_read_peoples(client):
    response = client.get('/list_users')

    assert len(response.json()['users']) >= 0


def test_update_user(client):
    response = client.put(
        '/update_users/1',
        json={
            'first_name': 'string teste',
            'last_name': 'string teste',
            'birthday': '2025-06-09',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_peoples(client):
    ids = pd.read_csv(PathFiles.DATABASE.value, sep=';')['id'].to_list()

    id = ids[randint(0, len(ids))]
    response = client.delete(f'/delete_user/{id}')

    assert response.status_code == HTTPStatus.OK


def test_error_update_user(client):
    response = client.put(
        '/update_users/190',
        json={
            'first_name': 'string teste',
            'last_name': 'string teste',
            'birthday': '2025-06-09',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_error_delete_user(client):
    response = client.delete('/delete_user/190')

    assert response.status_code == HTTPStatus.NOT_FOUND
