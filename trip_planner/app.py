import streamlit as st
from dotenv import load_dotenv
from st_pages import show_pages_from_config


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
    show_pages_from_config()
    main()
