from http import HTTPStatus

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schema import Books, ListUsers, Message, UserPrivate, UserPublic

# testar a questão de segurança ao excluir e adicionar depois


app = FastAPI(title='MY API BULLET!')


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def main():
    return '<h1>Hello World, User</h1>'


@app.post(
    '/created_user', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def created_people(user: UserPrivate, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'this email {user.email} exits in database',
        )

    db_user = User(**user.model_dump(), age=(2025 - int(user.birthday.year)))

    session.add(db_user)
    session.commit()

    # para os parametros que são inicializados dentro do banco
    session.refresh(db_user)

    return db_user


@app.get(
    '/user/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def read_people(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    return db_user


@app.get('/list_users', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_peoples(
    session=Depends(get_session), limit: int = 10, offset: int = 0
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.put(
    '/update_users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserPrivate, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei...'
        )

    try:
        user_db.email = user.email
        user_db.first_name = user.first_name
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )


@app.delete(
    '/delete_user/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei...'
        )

    session.delete(user_db)
    session.commit()
    return {'message': 'user delete with sucess'}


@app.get('/all_books/{year_of_lauch}', response_model=Books)
def all_books(year_of_lauch: int):
    df_books = pd.DataFrame(
        data={
            'name': ['Intrdução SQL', 'Ultra-Apredizado', 'Clean Code'],
            'isbn': ['31234', '3213', '53432'],
            'author': ['Franz Kafka', 'Zahar', 'Nield'],
            'year_of_lauch': [2003, 2003, 2015],
        }
    )
    df_books = df_books.query(f'year_of_lauch == {year_of_lauch}')
    return {'books': df_books.to_dict(orient='records')}
