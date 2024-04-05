import streamlit as st
from pydantic import SecretStr


def settings():
    st.title("Settings")

    with st.container():
        st.header("OpenAI API Key")
        st.markdown(
            """
            To use the OpenAI API, you need to provide your API key. 
            You can find your API key or generate a new one from [here](https://platform.openai.com/).
            """
        )
        api_key = st.text_input("API Key", type="password")
        if st.button("Save", key="save_api"):
            st.session_state["openai_key"] = SecretStr(api_key)
            st.success("API key saved successfully!")

    with st.expander("Advanced Settings"):
        st.header("Model Parameters")
        st.markdown(
            """
            You can customize the model parameters here. 
            The default parameters are set to the recommended values.
            Only change these if you know what you are doing!
            """
        )

        model_name = st.selectbox(
            "Model", ["gpt-3.5-turbo-1106", "gpt-3.5-turbo", "gpt-4"], index=0
        )
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5)
        if model_name:
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=1,
                value=4096 if model_name.startswith("gpt-3.5") else 10_000,
                max_value=10_000,
            )
        if st.button("Save", key="save_params"):
            st.session_state["model_name"] = model_name
            st.session_state["temperature"] = temperature
            st.session_state["max_tokens"] = max_tokens
            st.success("Model parameters saved successfully!")


if __name__ == "__main__":
    st.set_page_config(page_title="Settings", page_icon="⚙️")
    settings()
