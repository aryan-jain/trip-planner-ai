from datetime import date, datetime, timedelta

import streamlit as st
from dateutil.tz import gettz
from pytz import all_timezones
from streamlit_extras.switch_page_button import switch_page
from tzlocal import get_localzone_name

from trip_planner.db import query
from trip_planner.pages.login import get_authenticated_user


def create_trip():
    st.title("Create Trip")
    st.write("Let's create a new trip!")

    user = get_authenticated_user()
    if not user:
        st.error("Please log in first.")
        switch_page("Login")
    else:
        with st.form("create_trip_form"):
            title = st.text_input("Title", help="e.g. San Diego '24")
            description = st.text_area(
                "Description", help="e.g. Celebrating John's birthday in San Diego!"
            )
            dates = st.date_input(
                "Dates",
                value=[date.today(), date.today() + timedelta(days=1)],
                min_value=date.today(),
            )
            tz = st.selectbox(
                "Timezone",
                all_timezones,
                index=all_timezones.index(get_localzone_name()),
            )

            if st.form_submit_button("Create Trip"):
                if not isinstance(dates, tuple) or len(dates) != 2:
                    st.error("Please select a start and end date.")
                else:
                    try:
                        query.create_trip(
                            title=title,
                            description=description,
                            start_date=datetime.combine(
                                dates[0], datetime.min.time(), gettz(tz)
                            ),
                            end_date=datetime.combine(
                                dates[1], datetime.min.time(), gettz(tz)
                            ),
                            created_by=user.db_user.id,
                        )
                        st.success("Trip created successfully")
                        switch_page("Trips")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(page_title="Create Trip", page_icon="➕")
    create_trip()
