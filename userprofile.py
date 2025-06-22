import streamlit as st
from classes import User, Mission 

# For demo/testing, create a dummy user if not in session state
if "curr_user" not in st.session_state:
    try:
        st.session_state.curr_user = User(
            name="Alice",
            postal_code="M5S 1A1",
            user_id="alice123",
            bio="Hello, I'm Alice!",
            age=30,
            email="alice@example.com",
            phone_num="123-456-7890",
            homepage=None  # or pass MissionBoard instance if you want
        )
    except Exception as e:
        st.error(f"Error creating user: {e}")
        st.stop()

user = st.session_state.curr_user

st.title("🙋 User Profile")

# Editable fields
new_name = st.text_input("Name", value=user.name)
new_bio = st.text_area("Bio", value=user.bio)
new_age = st.number_input("Age", min_value=0, max_value=120, value=user.age)
new_email = st.text_input("Email", value=user.email)
new_phone = st.text_input("Phone Number", value=user.phone_num)

if st.button("Save Changes"):
    try:
        user.edit_name(new_name)  # will raise if invalid
        user.bio = new_bio
        user.age = new_age
        user.email = new_email
        user.phone_num = new_phone

        st.success("Profile updated!")
    except ValueError as ve:
        st.error(ve)
    except Exception as e:
        st.error(e)

# Show updated info
st.subheader("Current Profile Info")
st.write(f"**Name:** {user.name}")
st.write(f"**Bio:** {user.bio}")
st.write(f"**Age:** {user.age}")
st.write(f"**Email:** {user.email}")
st.write(f"**Phone:** {user.phone_num}")