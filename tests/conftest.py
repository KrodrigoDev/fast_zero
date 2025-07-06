from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


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
    # table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time_(model, time=datetime.now()):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'update_at'):
            target.update_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time_


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
