from contextlib import contextmanager
from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    birthday = date(2003, 7, 25)
    with _mock_db_age_(model=User, birthday=birthday) as age:
        new_user = User(
            first_name='Kaua',
            last_name='Rodrigo',
            password='batatinha123',
            birthday=birthday,
            email='teste@gmail.com',
            age=age,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user


@pytest.fixture
def session():
    engine = create_engine(
        'mysql://root:123456789@127.0.0.1:3306/testes_alembic'
    )

    # vai pegar todos os campos que registramos no models
    # e criar uma tabela. isso é como um create table
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # limpando o banco virtual depois de todos os processos
    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_age_(model, birthday):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'age'):
            target.age = datetime.now().year - target.birthday.year

    event.listen(model, 'before_insert', fake_time_hook)

    yield datetime.now().year - birthday.year

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_age():
    return _mock_db_age_


# @contextmanager
# def _birthday_user_(model):
#     def idade_hook(mapper, connection, target):
#         if hasattr(target, 'birthday'):
#             target.age = datetime.now().year - target.birthday.year
#
#     event.listen(model, 'before_insert', idade_hook)
#
#     yield model.age
#
#     event.remove(model, 'before_insert', idade_hook)
#

# @pytest.fixture
# def birthday_user():
#     return _birthday_user_
