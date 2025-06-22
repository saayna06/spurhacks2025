import streamlit as st
from classes import User

GOOGLE_API_KEY = "AIzaSyD03gVfZR53O17UMNS96zu3D4rXxJBBWtA"

def edit_profile_page(user: User):
    st.set_page_config(page_title="Edit Profile", page_icon="⚙️")
    st.title("⚙️ Edit Profile")

    # Editable fields
    name = st.text_input("Name", value=user.name)
    bio = st.text_area("Bio", value=user.bio)
    age = st.number_input("Age", min_value=0, max_value=120, value=user.age)
    email = st.text_input("Email", value=user.email)
    phone_num = st.text_input("Phone Number", value=user.phone_num)
    postal_code = st.text_input("Postal Code", value=user.postal_code)

    if st.button("Save Changes"):
        # Update user attributes
        user.name = name
        user.bio = bio
        user.age = age
        user.email = email
        user.phone_num = phone_num
        user.postal_code = postal_code

        st.success("Profile updated!")
        st.rerun()

    if st.sidebar.button("⬅️ Back to Mission Board"):
        st.session_state.page = "mission_board"
        st.rerun()
