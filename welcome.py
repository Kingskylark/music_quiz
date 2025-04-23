import streamlit as st

# In your welcome page function
def show_welcome():
    st.title("🎵 Church Music Quiz Game 🎵")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to the Church Music Quiz!
        
        Test your knowledge of church music with our interactive quiz game.
        
        ### How to Play:
        - Register or log in to start playing
        - Answer 20 multiple-choice questions
        - You have 10 seconds to answer each question
        - See how high you can score and make it to the leaderboard!
        
        Are you ready to test your church music knowledge?
        """)
        
        # Check if user is already logged in
        if "logged_in" not in st.session_state or not st.session_state.logged_in:
            # User is not logged in, show login and register buttons
            st.button("Login", key="login_button", on_click=set_page, args=("login",))
            st.button("Register", key="register_button", on_click=set_page, args=("register",))
        else:
            # User is logged in, show game options instead
            username = st.session_state.get("username", "User")
            st.write(f"Welcome back, {username}!")
            
            # Play Game button that takes user to the pre-game page
            st.button("Play Game", key="play_game_button", on_click=set_page, args=("pregame",))
            st.button("View Leaderboard", key="leaderboard_button", on_click=set_page, args=("leaderboard",))
            
            # Add logout option
            if st.button("Logout", key="logout_button"):
                # Clear session state variables related to login
                for key in ["logged_in", "username", "user_id", "score", "question_index"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.page = "welcome"
                st.experimental_rerun()
        
    with col2:
         st.image("data/church_quiz.jpg", use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("© 2025 Church Music Quiz Game")

def set_page(page):
    st.session_state.page = page