import uuid
from typing import Sequence

import sqlalchemy as sa

from .connection import get_sync_session
from .tables import Trips, Users


def get_trips_by_user(user_id: uuid.UUID) -> Sequence[sa.Row[tuple[Trips]]]:
    with get_sync_session() as session:
        result = session.execute(sa.select(Trips).where(Trips.created_by == user_id))
        return result.fetchall()


def get_user(email: str) -> sa.Row[tuple[Users]] | None:
    with get_sync_session() as session:
        result = session.execute(sa.select(Users).where(Users.email == email))
        return result.fetchone()
