from dataclasses import asdict, dataclass
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'hello world!'}


@app.get('/teste/')
def read_teste():
    return {'message': 'será que foi'}


@dataclass
class Pessoa:
    nome: str
    sobrenome: str
    nascimento: datetime
    idade: int = None
    nome_completo: str = None

    def __init__(self, nome: str, sobrenome: str, nascimento: datetime):
        self.nome = nome
        self.sobrenome = sobrenome
        self.nascimento = nascimento
        self.idade = datetime.now().year - nascimento.year
        self.nome_completo = f'{nome} {sobrenome}'


@app.get('/people/')
def read_people():
    p = Pessoa('Kauã', 'Rodrigo', datetime(2003, 7, 25))
    return asdict(p)
