import streamlit as st
from streamlit_extras import card


def trips():
    st.title("Trips")
    st.write("Add or view your trips here.")

    card.card(
        title="San Diego 2024",
        text="Arvind's Birthday Trip",
        on_click=click,
    )


def click():
    st.write("You clicked the card!")


if __name__ == "__main__":
    st.set_page_config(page_title="Trips", page_icon="📅")
    trips()
