import streamlit as st
from classes import User

GOOGLE_API_KEY = "AIzaSyD03gVfZR53O17UMNS96zu3D4rXxJBBWtA"

def signup_page():
    st.title("Sign Up")

    name = st.text_input("Name *")
    user_id = st.text_input("User ID *")
    age = st.number_input("Age *", min_value=0, max_value=120, step=1)
    email = st.text_input("Email *")
    phone_num = st.text_input("Phone Number *")
    bio = st.text_area("Bio (Optional)")

    postal_code = st.text_input("Postal Code *")
    city = st.text_input("City *")
    country = st.text_input("Country *")

    formatted_address = f"{postal_code.strip()}, {city.strip()}, {country.strip()}"

    if st.button("Sign Up"):
        if not all([name, user_id, email, phone_num, postal_code, city, country]):
            st.error("Please fill all required fields.")
        else:
            try:
                user = User(
                    name=name,
                    postal_code=formatted_address,
                    user_id=user_id,
                    bio=bio,
                    age=age,
                    email=email,
                    phone_num=phone_num,
                    google_api_key=GOOGLE_API_KEY,
                )
                st.session_state.curr_user = user
                st.session_state.page = "mission_board"
                st.rerun()
            except Exception as e:
                st.error(f"Failed to create user: {e}")
