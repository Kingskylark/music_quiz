import streamlit as st
import pandas as pd
import hashlib
import os
from utils import load_users, save_user, verify_login, get_user_id

# In auth.py, modify the show_login function:
def show_login():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Username and password cannot be empty")
            else:
                # Verify login
                if verify_login(username, password):
                    # Set session state
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = get_user_id(username)
                    
                    # Redirect to welcome page instead of game
                    st.session_state.page = "welcome"
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
    
    st.button("Forgot Password?", on_click=lambda: set_page("forgot_password"))
    st.markdown("---")
    st.markdown("Don't have an account?")
    st.button("Register", on_click=lambda: set_page("register"), key="login_to_register_btn")
    st.button("Back to Welcome Page", on_click=lambda: set_page("welcome"))

def show_register():
    st.title("Create an Account")
    
    users = load_users()
    if len(users) >= 20:
        st.warning("Registration limit reached. No more users can be registered.")
        st.button("Back to Welcome Page", on_click=lambda: set_page("welcome"))
        return  # Exit the function to prevent registration form from showing
    
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Username and password cannot be empty")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif username in users["name"].values:
                st.error("Username already exists")
            else:
                # Register new user
                save_user(username, password)
                st.success("Registration successful! Please login.")
                st.session_state.page = "login"
                st.experimental_rerun()

    st.markdown("---")
    st.markdown("Already have an account?")
    st.button("Login", on_click=lambda: set_page("login"))
    st.button("Back to Welcome Page", on_click=lambda: set_page("welcome"))


def show_forgot_password():
    st.title("Reset Password")
    
    with st.form("reset_form"):
        username = st.text_input("Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submit_button = st.form_submit_button("Reset Password")
        
        if submit_button:
            if username.strip() == "" or new_password.strip() == "":
                st.error("Username and password cannot be empty")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                users = load_users()
                if username not in users["name"].values:
                    st.error("Username does not exist")
                else:
                    # Update user's password
                    user_id = get_user_id(username)
                    users.loc[users["id"] == user_id, "password"] = hashlib.sha256(new_password.encode()).hexdigest()
                    users.to_csv("data/users.csv", index=False)
                    st.success("Password reset successful! Please login.")
                    st.session_state.page = "login"
                    st.experimental_rerun()
    
    st.button("Back to Login", on_click=lambda: set_page("login"))

# Add to auth.py
def show_admin_login():
    st.title("Admin Login")
    
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Username and password cannot be empty")
            else:
                # Verify login
                if verify_login(username, password):
                    # Check if user is admin
                    users = load_users()
                    user_role = users.loc[users["name"] == username, "role"].values[0]
                    
                    if user_role == "admin":
                        # Set session state
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = get_user_id(username)
                        st.session_state.is_admin = True
                        st.session_state.page = "admin_panel"
                        st.success("Admin login successful!")
                        st.experimental_rerun()
                    else:
                        st.error("You do not have admin privileges")
                else:
                    st.error("Invalid username or password")
    
    st.button("Back to Welcome Page", on_click=lambda: set_page("welcome"), key="admin_back_btn")

def set_page(page):
    st.session_state.page = page
