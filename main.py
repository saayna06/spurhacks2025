import streamlit as st
from home import show_mission_board, show_my_missions, show_messages, show_apply_to_mission
from edit_profile import edit_profile_page
from signup import signup_page

if "page" not in st.session_state:
    st.session_state.page = "signup"

if st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "mission_board":
    show_mission_board(st.session_state.curr_user)
elif st.session_state.page == "edit_profile":
    edit_profile_page(st.session_state.curr_user)
elif st.session_state.page == "my_missions":
    show_my_missions(st.session_state.curr_user)
elif st.session_state.page == "messages":
    show_messages(st.session_state.curr_user)
elif st.session_state.page == "apply_to_mission":
    show_apply_to_mission(st.session_state.curr_user)
