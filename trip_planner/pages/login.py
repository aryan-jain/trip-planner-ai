import uuid
import webbrowser
from dataclasses import dataclass
from typing import Any

import streamlit as st
from gotrue.types import (
    AuthResponse,
    SignInWithEmailAndPasswordCredentials,
    SignInWithOAuthCredentials,
    UserResponse,
)
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript

from trip_planner.db import query
from trip_planner.db.tables import Users
from trip_planner.sb import supabase
from trip_planner.util.validator import (
    Validator,
    check_email,
    check_password,
    max_length,
    min_length,
    required,
)


@dataclass
class AuthenticatedUser:
    id: uuid.UUID
    email: str
    logged_in: bool
    token: str

    db_user: Users


def login():
    st.title("Login")

    url: str = st_javascript("await fetch('').then(r => window.parent.location.href)")
    browser = webbrowser.get("firefox")

    if isinstance(url, str) and "#" in url:
        browser.open(url.replace("#", "?"), new=0)

    # Check if the user has been redirected from an OAuth provider
    access_token = st.query_params.get("access_token")
    if access_token:
        refresh_token = st.query_params["refresh_token"]
        supabase.auth.set_session(access_token, refresh_token)

        sb_user_resp: UserResponse | None = supabase.auth.get_user(access_token)
        if sb_user_resp and sb_user_resp.user:
            db_user = query.get_user(sb_user_resp.user.email or "")
            if not db_user:
                st.error("User not found.")
            else:
                st.session_state["user"] = AuthenticatedUser(
                    id=uuid.UUID(sb_user_resp.user.id),
                    email=db_user.email,
                    logged_in=True,
                    token=access_token,
                    db_user=db_user,
                )

    # Check if user is already logged in
    if st.session_state.get("user"):
        st.success("Login successful.")
        if st.button("Log Out"):
            supabase.auth.sign_out()
            st.session_state["user"] = None
    else:
        login_form()


def login_form():
    with st.container():
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.button("Login")
        st.write("----- OR -----")
        provider = st.button("Login with Google")
        validator = Validator({"email": email, "password": password})

        validator.set_rule("email", [required, check_email])
        validator.set_rule(
            "password", [required, min_length(8), max_length(50), check_password]
        )

        if submit:
            errors = validator.validate()
            if any(error.error for error in errors.values()):
                for error in errors.values():
                    if error.error:
                        st.error(error.error_msg)

            else:
                user: AuthResponse = supabase.auth.sign_in_with_password(
                    SignInWithEmailAndPasswordCredentials(
                        email=email, password=password
                    )
                )

                if user.user and user.session:
                    db_user = query.get_user(email)
                    if not db_user:
                        st.error("User not found.")
                    else:
                        st.session_state["user"] = AuthenticatedUser(
                            id=uuid.UUID(user.user.id),
                            email=email,
                            logged_in=True,
                            token=user.session.access_token,
                            db_user=db_user,
                        )
                        st.success("Login successful.")

                else:
                    st.error("Invalid email and password combination.")

        if provider:
            resp = supabase.auth.sign_in_with_oauth(
                SignInWithOAuthCredentials(
                    provider="google",
                    options={"redirect_to": "http://localhost:8501/Login"},
                )
            )
            browser = webbrowser.get("firefox")
            browser.open(resp.url, new=0)


def get_authenticated_user() -> AuthenticatedUser | None:
    user: AuthenticatedUser | None = st.session_state.get("user")
    # if user:
    #     resp: UserResponse | None = supabase.auth.get_user(user.token)
    #     if resp and resp.user:
    #         return user

    return user


if __name__ == "__main__":
    login()
