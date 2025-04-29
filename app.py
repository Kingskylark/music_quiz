import streamlit as st
import os

# Import page modules
from welcome import show_welcome
from auth import show_login, show_register, show_forgot_password, show_admin_login  # Add admin login import
from game import show_game
from leaderboard import show_leaderboard
from admin import show_admin_panel
from utils import create_admin_if_not_exists
from pregame import show_pregame

# Set page configuration
st.set_page_config(
    page_title="Church Music Quiz Game",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize admin user
create_admin_if_not_exists()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    
    # Show different options based on login status
    if st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.username}!")
        
        # Show admin panel option only for admin users
        if st.session_state.get("is_admin", False):
            if st.button("Admin Panel", key="admin_panel_btn"):
                st.session_state.page = "admin_panel"
                st.experimental_rerun()
        
        if st.button("Play Game", key="play_game_btn"):
            st.session_state.page = "game"
            st.experimental_rerun()
            
        if st.button("Leaderboard", key="view_leaderboard_btn"):
            st.session_state.page = "leaderboard"
            st.experimental_rerun()
            
        if st.button("Logout", key="logout_btn"):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key != "page":
                    del st.session_state[key]
            st.session_state.logged_in = False
            st.session_state.page = "welcome"
            st.experimental_rerun()
    else:
        if st.button("Welcome", key="welcome_btn"):
            st.session_state.page = "welcome"
            st.experimental_rerun()
            
        if st.button("Login", key="login_btn"):
            st.session_state.page = "login"
            st.experimental_rerun()
            
        if st.button("Register", key="register_btn"):
            st.session_state.page = "register"
            st.experimental_rerun()
            
        if st.button("Admin Login", key="sidebar_admin_login_btn"):
            st.session_state.page = "admin_login"
            st.experimental_rerun()
            
        if st.button("Leaderboard", key="leaderboard_btn"):
            st.session_state.page = "leaderboard"
            st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("© 2025 Church Music Quiz")

# Main content routing
if st.session_state.page == "welcome":
    show_welcome()
elif st.session_state.page == "login":
    show_login()
elif st.session_state.page == "register":
    show_register()
elif st.session_state.page == "forgot_password":
    show_forgot_password()
elif st.session_state.page == "admin_login":  # Add this route
    show_admin_login()
elif st.session_state.page == "admin_panel":  # Add this route
    show_admin_panel()
elif st.session_state.page == "pregame":  # Add this new route
    show_pregame()
elif st.session_state.page == "game":
    if not st.session_state.get("logged_in", False):
        st.warning("Please login to play the game")
        st.session_state.page = "login"
        st.experimental_rerun()
    else:
        show_game()
elif st.session_state.page == "leaderboard":
    show_leaderboard()
else:
    st.error("Page not found")
    st.session_state.page = "welcome"
    st.experimental_rerun()
