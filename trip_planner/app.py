import streamlit as st
from dotenv import load_dotenv
from st_pages import Page, Section, show_pages, show_pages_from_config


def main():
    st.title("Trip Planner AI")
    st.write(
        "Welcome to the Trip Planner AI! This AI will help you plan your next trip.\n"
    )
    st.markdown(
        "If you have an environment variable set for your OpenAI API key, you can start planning your trip now "
        "by navigating to the `Trip Planner` page from the sidebar on the left. Otherwise, navigate first to the "
        "`Settings` page to set up your OpenAI API key."
    )


if __name__ == "__main__":
    load_dotenv()

    show_pages(
        [
            Page(
                path="trip_planner/pages/login.py",
                name="Login",
                icon="🔑",
            ),
            Page(
                path="trip_planner/app.py",
                name="Home",
                icon="🏠",
            ),
            Page(
                path="trip_planner/pages/settings.py",
                name="Settings",
                icon="⚙️",
            ),
            Page(
                path="trip_planner/pages/planner.py",
                name="Trip Planner",
                icon=":airplane:",
            ),
            Section(
                name="Trips",
                icon="📅",
            ),
            Page(
                path="trip_planner/pages/trips.py",
                name="View Trips",
                in_section=True,
            ),
            Page(
                path="trip_planner/pages/new_trip.py",
                name="Create Trip",
            ),
            Page(
                path="trip_planner/pages/trip_details.py",
                name="Trip Details",
            ),
        ]
    )
    main()
