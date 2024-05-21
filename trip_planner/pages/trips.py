import itertools as it

import streamlit as st
from streamlit_extras import card
from streamlit_extras.switch_page_button import switch_page

from trip_planner.db import query
from trip_planner.pages.login import get_authenticated_user


def trips():
    st.title("Trips")
    st.write("Add or view your trips here.")

    user = get_authenticated_user()
    if not user:
        switch_page("Login")
    else:
        trips = query.get_trips_by_user(user.db_user.id)

        if len(trips):
            st.write("Your trips:")
            cols = st.columns(3)
            grid = it.cycle(cols)
            for trip in trips:
                with next(grid):
                    card.card(
                        title=trip.title,
                        text=[
                            trip.description,
                            " ⠀ ",
                            f"{trip.start_date.date()} - {trip.end_date.date()}",
                        ],
                        styles={
                            "card": {
                                "padding": "20px",
                                "width": "100%",
                                "height": "100%",
                            },
                            "text": {"font-size": "0.9rem"},
                        },
                        on_click=lambda t=trip: load_trip_details(t),
                    )
        else:
            st.write("You have no trips yet.")

        st.divider()
        if st.button("Create Trip"):
            switch_page("Create Trip")


def load_trip_details(trip):
    st.session_state["trip"] = trip
    switch_page("Trip Details")


if __name__ == "__main__":
    st.set_page_config(page_title="Trips", page_icon="📅")
    trips()
