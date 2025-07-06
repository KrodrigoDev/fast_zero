from dataclasses import asdict
from datetime import date

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    # now = datetime.now()
    #
    # with mock_db_time(model=User, time=now):
    new_user = User(
        first_name='Kaua',
        last_name='Rodrigo',
        password='batatinha123',
        birthday=date(2003, 7, 25),
        email='teste2@gmail.com',
        age=None
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.password == 'batatinha123'))

    assert asdict(user)['password'] == 'batatinha123'
