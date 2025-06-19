from http import HTTPStatus

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.globais import PathFiles
from fast_zero.schema import ListUsers, UserPrivate, UserPublic

# testar a questão de segurança ao excluir e adicionar depois


def read_data() -> pd.DataFrame:
    if PathFiles.DATABASE.value.exists():
        return pd.read_csv(PathFiles.DATABASE.value, sep=';')

    PathFiles.DATABASE.value.touch()

    df = pd.DataFrame(
        columns=['id', 'first_name', 'last_name', 'birthday', 'password']
    )
    df.to_csv(PathFiles.DATABASE.value, index=False, sep=';')

    return df


app = FastAPI(title='MY API BULLET!')


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def main():
    return '<h1>Hello World, User</h1>'


@app.post(
    '/created_user', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def created_people(user: UserPrivate):
    df = read_data()

    df_size = df.shape[0]
    user = user.model_dump()
    user['id'] = df_size

    df.loc[df_size] = user

    df.to_csv(PathFiles.DATABASE.value, index=False, sep=';')

    return df.loc[df_size]


@app.get(
    '/user/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def read_people(user_id: int):
    df = read_data()

    return df.loc[user_id]


@app.get('/list_users', status_code=HTTPStatus.OK, response_model=ListUsers)
def read_peoples():
    df = read_data()

    return {'users': df.to_dict(orient='records')}


@app.put(
    '/update_users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserPrivate):
    df = read_data()

    if user_id not in df['id'].unique():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei...'
        )

    user = user.model_dump()
    user['id'] = df.loc[user_id]['id']
    df.loc[user_id] = user

    df.to_csv(PathFiles.DATABASE.value, sep=';', index=False)
    return df.loc[user_id]


@app.delete(
    '/delete_user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def delete_user(user_id: int):
    df = read_data()

    if user_id not in df['id'].unique():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim! Não achei...'
        )

    new_df = df.drop(index=user_id).copy()

    new_df.to_csv(PathFiles.DATABASE.value, sep=';', index=False)

    return df.loc[user_id]
