import contextlib as ctx
import uuid
from datetime import datetime
from typing import Any, Sequence

import sqlalchemy as sa

from .connection import session
from .tables import Trips, Users


def get_trips_by_user(user_id: uuid.UUID) -> Sequence[Trips]:
    with ctx.closing(session()) as s:
        result = s.scalars(sa.select(Trips).where(Trips.created_by == user_id))
        trips = result.all()
        return trips


def get_user(email: str) -> Users | None:
    with ctx.closing(session()) as s:
        result = s.scalars(sa.select(Users).where(Users.email == email))
        user = result.first()
        return user


def create_trip(
    title: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    created_by: uuid.UUID,
):
    with ctx.closing(session()) as s:
        trip = Trips(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_by=created_by,
            archived=False,
        )
        s.add(trip)
        s.commit()
        return trip
