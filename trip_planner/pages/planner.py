from urllib.parse import quote

import streamlit as st
import streamlit_pydantic as sp
from pydantic import BaseModel, Field

from trip_planner.llm.travel_agent import NotAuthorizedError, TravelAgent


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
        alias="This_trip_is_a_",
        description="The type of trip. E.g. 'vacation with friends', 'couple's getaway'",
    )
    additional_info: str = Field(
        "",
        description="Anything specific you want to add about your trip. E.g. 'We want to experience at least a couple boujee restaurants, but otherwise on a budget. We want to spend one afternoon on the beach. Make sure we get to see at least a few good bars and nightclubs while we are there.'",
        format="multi-line",
    )


def planner():
    try:
        model_params = {}
        if st.session_state.get("model_name"):
            model_params["model_name"] = st.session_state["model_name"]
        if st.session_state.get("temperature"):
            model_params["temperature"] = st.session_state["temperature"]
        if st.session_state.get("max_tokens"):
            model_params["max_tokens"] = st.session_state["max_tokens"]
        if st.session_state.get("openai_key"):
            model_params["openai_api_key"] = st.session_state["openai_key"]
        travel_agent = TravelAgent(**model_params)
    except NotAuthorizedError as e:
        st.error(e)

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
                destination=data.destination.removesuffix("."),
                num_days=data.num_days,
                num_people=data.num_people,
                trip_type=data.trip_type.removesuffix("."),
                additional_info=data.additional_info.removesuffix(".") + ".",
            )

        st.write("Here is your itinerary:")

        total_cost = 0
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
                    case _:
                        st.markdown(f"#### ⭐️ {activity.name}")
                st.markdown(f"*{activity.price}*")
                st.write(f"Estimated cost per person: ${activity.cost_per_person:.2f}")
                total_cost += activity.cost_per_person
                st.write(activity.description)
                if activity.url:
                    st.link_button(
                        "Website ⎋", activity.url, help="Open the website in a new tab"
                    )

        st.subheader(f"Total estimated cost per person: ${total_cost:.2f}")
        # st.link_button(
        #     "Find Hotels",
        #     f"https://www.google.com/travel/search?q={quote(data.destination + " hotels")}&hl=en-US",
        #     help="Find hotels in your destination",
        # )
        st.link_button(
            "Find Flights",
            f"https://www.google.com/flights?q={quote(data.destination)}&hl=en-US",
            help="Find flights to your destination",
        )


if __name__ == "__main__":
    st.set_page_config(page_title="Trip Planner AI", page_icon="🌍")
    planner()
