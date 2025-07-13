from datetime import date, datetime

from sqlalchemy import Boolean, String, func, text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
)

table_registry = registry()


# anotation para mapear os colunas da tabelada criada
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(70), nullable=False)
    last_name: Mapped[str] = mapped_column(String(70), nullable=False)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    birthday: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(70), unique=True)
    # fazer isso funcionar depois usando hooks
    age: Mapped[int] = mapped_column(nullable=True)
    # é mesmo necessário passar esses dois default?
    vip: Mapped[bool] = mapped_column(
        Boolean, server_default=text('0'), default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    update_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), server_onupdate=func.now()
    )

    # init é dado como falso para que não seja preciso passar o campo
    # pois o mesmo vai se autopreencher

    # mapear os campos
    # mapped_column permite com que seja adicionada restrições
    # func permite com que seja pego a hora do banco
