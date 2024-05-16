import sqlalchemy as sa
import streamlit as st
from streamlit_extras import card

from trip_planner.db import query
from trip_planner.db.tables import Users


def trips():
    st.title("Trips")
    st.write("Add or view your trips here.")

    user: Users = st.session_state["user"]

    trips = query.get_trips_by_user(user.id)
    for trip in trips:
        card.card(
            title=trip.title,
            text=trip.description,
        )


if __name__ == "__main__":
    st.set_page_config(page_title="Trips", page_icon="📅")
    trips()
