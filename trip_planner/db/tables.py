from typing import List

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("email", name="users_email_key"),
    )

    id = mapped_column(Uuid)
    email = mapped_column(Text, nullable=False)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    enabled = mapped_column(Boolean, nullable=False)
    name = mapped_column(String(255))

    trips: Mapped[List["Trips"]] = relationship(
        "Trips", uselist=True, back_populates="users"
    )


class Trips(Base):
    __tablename__ = "trips"
    __table_args__ = (
        ForeignKeyConstraint(
            ["created_by"], ["users.id"], name="trips_created_by_fkey"
        ),
        PrimaryKeyConstraint("id", name="trips_pkey"),
    )

    id = mapped_column(Uuid)
    title = mapped_column(Text, nullable=False)
    start_date = mapped_column(DateTime(True), nullable=False)
    end_date = mapped_column(DateTime(True), nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    created_by = mapped_column(Uuid, nullable=False)
    archived = mapped_column(Boolean, nullable=False)
    description = mapped_column(Text)

    users: Mapped["Users"] = relationship("Users", back_populates="trips")
