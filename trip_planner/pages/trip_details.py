import streamlit as st

from trip_planner.db.tables import Trips


def trip_details():
    trip: Trips | None = st.session_state.get("trip")
    if trip:
        st.title(trip.title)
        st.write(trip.description)

        st.write(f"Start date: {trip.start_date.date()}")
        st.write(f"End date: {trip.end_date.date()}")

        with st.container():
            st.subheader("Attendees:")

        st.divider()

        with st.container():
            st.subheader("Accommodations:")

        st.divider()

        with st.container():
            st.subheader("Itinerary:")

        st.divider()

        with st.container():
            st.subheader("Expenses:")


if __name__ == "__main__":
    st.set_page_config(page_title="Trip Details", page_icon="📅")
    trip_details()
