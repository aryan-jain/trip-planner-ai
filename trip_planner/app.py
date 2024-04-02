import streamlit as st
import streamlit_pydantic as sp
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from trip_planner.llm.models import Activity, Itinerary
from trip_planner.llm.travel_agent import TravelAgent


class TripDetails(BaseModel):
    destination: str = Field(
        ...,
        description="The destination of the trip. E.g. 'San Diego, CA'",
    )
    num_days: int = Field(
        ...,
        ge=1,
        le=5,
        description="The number of days of the trip",
    )
    num_people: int = Field(
        ...,
        ge=1,
        le=30,
        description="The number of people going on the trip",
    )
    trip_type: str = Field(
        ...,
        description="The type of trip. E.g. 'vacation with friends', 'couple's getaway'",
    )
    additional_info: str = Field(
        "",
        description="Anything specific you want to add about your trip. E.g. 'We want to experience at least a couple boujee restaurants, but otherwise on a budget. We want to spend one afternoon on the beach. Make sure we get to see at least a few good bars and nightclubs while we are there.'",
        format="multi-line",
    )


def main():
    travel_agent = TravelAgent()

    st.title("Trip Planner AI")
    st.write(
        """
        This AI will help you plan your trip. 
        Enter the details of your trip below and click the button to get your itinerary.
        """
    )
    data = sp.pydantic_form(key="my_form", model=TripDetails)

    if data:
        with st.spinner("Planning your trip..."):
            recs = travel_agent.get_recs(
                destination=data.destination,
                num_days=data.num_days,
                num_people=data.num_people,
                trip_type=data.trip_type,
                additional_info=data.additional_info,
            )

        st.write("Here is your itinerary:")

        st.markdown("## Areas to Stay:")
        for neighborhood in recs.areas_to_stay:
            st.markdown(f"### {neighborhood.name.title()}")
            st.markdown(f"Type: {neighborhood.type.capitalize()}")
            st.write(f"{neighborhood.description}")
            st.caption(f"Walking Score: {neighborhood.walking_score}")
        for day in recs.days:

            st.divider()
            st.markdown(f"## Day {day.day_num}")
            for activity in day.timeline:
                st.markdown(f"### {activity.time.capitalize()}")
                match activity.type:
                    case "restaurant":
                        st.markdown(f"#### 🍽️ {activity.name}")
                    case "museum":
                        st.markdown(f"#### 🏛️ {activity.name}")
                    case "park":
                        st.markdown(f"#### 🌳 {activity.name}")
                    case "beach":
                        st.markdown(f"#### 🏖️ {activity.name}")
                    case "shopping":
                        st.markdown(f"#### 🛍️ {activity.name}")
                    case "hiking":
                        st.markdown(f"#### 🥾 {activity.name}")
                    case "sightseeing":
                        st.markdown(f"#### 🏞️ {activity.name}")
                    case "bar":
                        st.markdown(f"#### 🍺 {activity.name}")
                    case "nightclub":
                        st.markdown(f"#### 🪩 {activity.name}")
                st.markdown(f"*{activity.price}*")
                st.write(activity.description)
                if activity.url:
                    st.link_button(
                        "Website ⎋", activity.url, help="Open the website in a new tab"
                    )


if __name__ == "__main__":
    load_dotenv()
    st.set_page_config(page_title="Trip Planner AI", page_icon="🌍")
    main()
