import streamlit as st
import pandas as pd
from utils import load_scores, load_users

def show_leaderboard():
    st.title("🏆 Leaderboard 🏆")
    
    # Load scores and users data
    scores_df = load_scores()
    users_df = load_users()

    # Ensure matching data types
    scores_df["user_id"] = scores_df["user_id"].astype(str)
    users_df["id"] = users_df["id"].astype(str)
    
    if scores_df.empty:
        st.info("No scores yet. Be the first to play!")
    else:
        # Merge scores with usernames
        leaderboard = scores_df.merge(users_df[["id", "name"]], left_on="user_id", right_on="id")
        
        # Sort by score (descending) and date (for tiebreakers)
        leaderboard = leaderboard.sort_values(["score", "date"], ascending=[False, True])
        
        # Take top 10
        top_10 = leaderboard.head(10)
        
        # Display formatted leaderboard
        st.write("### Top 10 Players")
        
        # Create a clean df for display
        display_df = top_10[["name", "score", "date"]].reset_index(drop=True)
        display_df.index = display_df.index + 1  # Start index at 1
        display_df.columns = ["Player", "Score", "Date"]
        
        # Display with styling
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=False
        )
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.timer_start = 0
            st.session_state.answered = False
            st.session_state.feedback = None
            st.session_state.page = "game"
            st.experimental_rerun()
    with col2:
        if st.button("Main Menu"):
            st.session_state.page = "welcome"
            st.experimental_rerun()
