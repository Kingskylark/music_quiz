# Create a new file called pregame.py or add this to an existing file
import streamlit as st
import time

def show_pregame():
    st.title("Get Ready to Play!")
    
    username = st.session_state.get("username", "Player")
    
    st.write(f"Welcome, {username}!")
    st.markdown("""
    ### Game Rules:
    - You will be presented with 20 questions about church music
    - Each question has 4 multiple-choice options
    - You have 10 seconds to answer each question
    - Your final score will be added to the leaderboard
    
    Good luck and enjoy the quiz!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # This button will actually start the game
        if st.button("Start Game", key="start_game_button"):
            # Initialize game state variables
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.timer_start = time.time()
            st.session_state.answered = False
            st.session_state.feedback = None
            # Navigate to the game page
            st.session_state.page = "game"
            st.experimental_rerun()
    
    with col2:
        # Option to go back to welcome page
        if st.button("Back to Home", key="back_to_welcome_button"):
            st.session_state.page = "welcome"
            st.experimental_rerun()