import streamlit as st
from datetime import datetime
from classes import Mission, User
from missionboard import MissionBoard

GOOGLE_API_KEY = "AIzaSyD03gVfZR53O17UMNS96zu3D4rXxJBBWtA"

def show_mission_board(user: User):
    st.set_page_config(page_title="Mission Board", page_icon="🛠️")
    st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #FFFFFF;
        }
        [data-testid="stSidebar"] {
            background-color: #D6EBFF;
        }
        .stMarkdown, .stTextInput, .stTextArea, .stSelectbox, .stButton, .stSlider {
            color: #051014;
        }

        /* ==== BUTTON HOVER STYLING ==== */
        button:hover {
            background-color: #C2E1FF !important;
            color: black !important;
            transition: background-color 0.3s ease;
        }

        /* ==== BUTTON OUTLINE HOVER ==== */
        button:focus, button:active {
            border-color: #CCD5AE !important;
            box-shadow: 0 0 0 0.2rem #CCD5AE50 !important;
        }

        /* ==== SLIDER STYLING ==== */
        [data-testid="stSlider"] > div[role="slider"] > div {
            background-color: #264653 !important; /* Slider track */
        }

        [data-testid="stSlider"] span[data-baseweb="slider"] > div > div {
            background-color: #264653 !important; /* Slider thumb */
            border-color: #264653 !important;
        }

        [data-testid="stSlider"] span[data-baseweb="slider"] > div > div:hover,
        [data-testid="stSlider"] span[data-baseweb="slider"] > div > div:focus {
            box-shadow: 0 0 0 4px rgba(38, 70, 83, 0.3) !important; /* Dark blue focus ring */
        }
    </style>
""", unsafe_allow_html=True)

    st.title("Mission Board 🛠️")
    st.markdown("Here are nearby job requests for you!")

    # Dummy poster user for sample missions
    dummy_user = User(
        name="Poster Making",
        postal_code="M4M 2A5, Toronto, Canada",
        user_id="poster1",
        bio="",
        age=30,
        email="poster1@example.com",
        phone_num="1234567890",
        google_api_key=GOOGLE_API_KEY
    )

    # Sample missions with payment
    mission1 = Mission(
        seeker=dummy_user,
        title="Garage Cleanup",
        description="Clean garage and sort tools",
        urgency="High",
        start_datetime=datetime(2025, 6, 22, 14, 0),
        end_datetime=datetime(2025, 6, 22, 16, 0),
        postal_code="M4M 2A5, Toronto, Canada",
        google_api_key=GOOGLE_API_KEY
    )
    mission1.payment = "$50"

    mission2 = Mission(
        seeker=dummy_user,
        title="Table Assembly",
        description="Assemble IKEA table",
        urgency="Medium",
        start_datetime=datetime(2025, 6, 23, 12, 0),
        end_datetime=datetime(2025, 6, 23, 13, 30),
        postal_code="M5S 1A1, Toronto, Canada",
        google_api_key=GOOGLE_API_KEY
    )
    mission2.payment = "$40"

    if not user.homepage or not user.homepage.missions:
        user.homepage = MissionBoard(missions=[mission1, mission2], curr_user=user)

    # Sidebar buttons
    if st.sidebar.button("⚙️ Edit Profile"):
        st.session_state.page = "edit_profile"
        st.rerun()

    if st.sidebar.button("📋 My Posted Missions"):
        st.session_state.page = "my_missions"
        st.rerun()

    if st.sidebar.button("✉️ Messages"):
        st.session_state.page = "messages"
        st.rerun()

    if st.sidebar.button("➡️ Apply to Mission"):
        st.session_state.page = "apply_to_mission"
        st.rerun()

    if st.button("➕ Create New Mission"):
        st.session_state.show_new_mission_form = True

    if st.session_state.get("show_new_mission_form", False):
        with st.form("new_mission_form"):
            title = st.text_input("Mission Title")
            description = st.text_area("Description")
            urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
            start_date = st.date_input("Start Date")
            start_time = st.time_input("Start Time")
            end_date = st.date_input("End Date")
            end_time = st.time_input("End Time")
            postal_code = st.text_input("Postal Code (e.g., M5S 1A1, Toronto, Canada)")
            payment = st.text_input("Payment Amount (e.g., $50)")

            submitted = st.form_submit_button("Post Mission")
            if submitted:
                try:
                    start_datetime = datetime.combine(start_date, start_time)
                    end_datetime = datetime.combine(end_date, end_time)
                    new_mission = Mission(
                        seeker=user,
                        title=title,
                        description=description,
                        urgency=urgency,
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        postal_code=postal_code,
                        google_api_key=GOOGLE_API_KEY
                    )
                    new_mission.payment = payment if payment else "N/A"
                    user.homepage.missions.append(new_mission)
                    st.success("Mission posted successfully!")
                    st.session_state.show_new_mission_form = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error posting mission: {e}")

    radius = st.slider("📍 Show missions within radius (km):", 1, 50, value=user.homepage.radius)
    filtered_board = user.homepage.find_in_radius(radius)

    for mission in filtered_board.missions:
        with st.expander(f"📝 {mission.title}"):
            st.markdown(f"**Description:** {mission.description}")
            st.markdown(f"**Urgency:** {mission.urgency}")
            st.markdown(f"**Payment:** {getattr(mission, 'payment', 'N/A')}")
            st.markdown(f"**Start:** {mission.start_datetime.strftime('%b %d, %I:%M %p')}")
            st.markdown(f"**End:** {mission.end_datetime.strftime('%b %d, %I:%M %p')}")
            st.markdown(f"**Location:** {mission.location.address}")

def show_apply_to_mission(user: User):
    st.set_page_config(page_title="Apply to Mission", page_icon="➡️")
    st.title("➡️ Apply to a Mission")

    available_missions = [m for m in user.homepage.missions if m.seeker.user_id != user.user_id]

    if not available_missions:
        st.info("No missions available to apply for at the moment.")
        if st.button("⬅️ Back to Mission Board"):
            st.session_state.page = "mission_board"
            st.rerun()
        return

    options = [f"{m.title} (Payment: {getattr(m, 'payment', 'N/A')})" for m in available_missions]
    selected_idx = st.selectbox("Select a mission to apply for:", range(len(options)), format_func=lambda i: options[i])
    selected_mission = available_missions[selected_idx]

    st.markdown(f"**Mission Description:** {selected_mission.description}")
    st.markdown(f"**Urgency:** {selected_mission.urgency}")
    st.markdown(f"**Payment:** {getattr(selected_mission, 'payment', 'N/A')}")
    st.markdown(f"**Start:** {selected_mission.start_datetime.strftime('%b %d, %I:%M %p')}")
    st.markdown(f"**End:** {selected_mission.end_datetime.strftime('%b %d, %I:%M %p')}")
    st.markdown(f"**Location:** {selected_mission.location.address}")

    message = st.text_area("Write a message to the job poster:")

    if st.button("Send Application"):
        selected_mission.requested_users.append(user)
        poster_id = selected_mission.seeker.user_id
        if poster_id not in user.text_log:
            user.text_log[poster_id] = []
        user.text_log.setdefault(poster_id, []).append(f"From {user.name}: {message}")
        st.success("Your application was sent!")

    if st.button("⬅️ Back to Mission Board"):
        st.session_state.page = "mission_board"
        st.rerun()

def show_my_missions(user: User):
    st.set_page_config(page_title="My Missions", page_icon="📋")
    st.title("📋 My Posted Missions")

    if not user.homepage or not user.homepage.missions:
        st.info("You have no posted missions yet.")

        if st.sidebar.button("⬅️ Back to Mission Board"):
            st.session_state.page = "mission_board"
            st.rerun()

        return

    posted = [m for m in user.homepage.missions if m.seeker.user_id == user.user_id]

    if not posted:
        st.info("You have no posted missions yet.")

        if st.sidebar.button("⬅️ Back to Mission Board"):
            st.session_state.page = "mission_board"
            st.rerun()

        return

    for mission in posted:
        with st.expander(f"📝 {mission.title}"):
            st.markdown(f"**Description:** {mission.description}")
            st.markdown(f"**Urgency:** {mission.urgency}")
            st.markdown(f"**Payment:** {getattr(mission, 'payment', 'N/A')}")
            st.markdown(f"**Start:** {mission.start_datetime.strftime('%b %d, %I:%M %p')}")
            st.markdown(f"**End:** {mission.end_datetime.strftime('%b %d, %I:%M %p')}")
            st.markdown(f"**Location:** {mission.location.address}")

            if mission.requested_users:
                st.markdown("**Users who requested this mission:**")
                for u in mission.requested_users:
                    st.write(f"- {u.name} (ID: {u.user_id})")
            else:
                st.markdown("_No users have requested this mission yet._")

    if st.sidebar.button("⬅️ Back to Mission Board"):
        st.session_state.page = "mission_board"
        st.rerun()

def show_messages(user: User):
    st.set_page_config(page_title="Messages", page_icon="✉️")
    st.title("✉️ Your Messages")

    found = False
    for sender_id, messages in user.text_log.items():
        with st.expander(f"From {sender_id}"):
            for msg in messages:
                st.write(msg)
                found = True

    if not found:
        st.info("You have no messages.")

    if st.sidebar.button("⬅️ Back to Mission Board"):
        st.session_state.page = "mission_board"
        st.rerun()
