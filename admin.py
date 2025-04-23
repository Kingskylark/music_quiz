import streamlit as st
import pandas as pd
import os
import hashlib
from utils import load_users, load_scores, load_questions

def show_admin_panel():
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. Admin privileges required.")
        st.session_state.page = "welcome"
        st.experimental_rerun()
        return
    
    st.title("Admin Panel")
    st.write(f"Welcome, {st.session_state.username}!")
    
    # Create tabs for different admin functions
    tab1, tab2, tab3 = st.tabs(["User Management", "Question Management", "View Scores"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_question_management()
    
    with tab3:
        show_all_scores()

def show_user_management():
    st.header("User Management")
    
    # Load users
    users = load_users()
    
    # Display users with edit functionality
    with st.expander("All Users", expanded=True):
        edited_users = st.data_editor(
            users[["id", "name", "role"]], 
            use_container_width=True,
            num_rows="dynamic", 
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True),
                "name": st.column_config.TextColumn("Username"),
                "role": st.column_config.SelectboxColumn("Role", options=["user", "admin"])
            }
        )
    
    # User selection for detailed actions
    if not users.empty:
        selected_user = st.selectbox("Select a user to modify:", users["name"])
        user_id = users.loc[users["name"] == selected_user, "id"].values[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Change role
            new_role = st.selectbox("Change role:", ["user", "admin"], index=0 if users.loc[users["name"] == selected_user, "role"].values[0] == "user" else 1)
            if st.button("Update Role"):
                if selected_user == st.session_state.username and new_role != "admin":
                    st.error("You cannot remove your own admin privileges.")
                else:
                    users.loc[users["name"] == selected_user, "role"] = new_role
                    users.to_csv("data/users.csv", index=False)
                    st.success(f"Updated {selected_user}'s role to {new_role}")
                    st.experimental_rerun()
            
            # Reset password
            new_password = st.text_input("New password:", type="password")
            if st.button("Reset Password") and new_password:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                users.loc[users["id"] == user_id, "password"] = hashed_password
                users.to_csv("data/users.csv", index=False)
                st.success(f"Password for {selected_user} has been reset")
        
        with col2:
            # Delete user
            if st.button("Delete User", type="primary", use_container_width=True):
                if selected_user == st.session_state.username:
                    st.error("You cannot delete your own account.")
                else:
                    users = users[users["name"] != selected_user]
                    users.to_csv("data/users.csv", index=False)
                    st.success(f"User {selected_user} has been deleted")
                    st.experimental_rerun()
    
    # Add new user section
    st.markdown("---")
    st.subheader("Add New User")
    
    col1, col2 = st.columns(2)
    with col1:
        new_username = st.text_input("Username")
    with col2:
        new_password = st.text_input("Password", type="password")
    
    new_role = st.selectbox("Role", ["user", "admin"])
    
    if st.button("Add User"):
        if new_username and new_password:
            if new_username in users["name"].values:
                st.error("Username already exists")
            else:
                # Create user
                user_id = str(pd.util.hash_pandas_object([new_username])[0])
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                
                new_user = pd.DataFrame({
                    "id": [user_id],
                    "name": [new_username],
                    "password": [hashed_password],
                    "role": [new_role]
                })
                
                users = pd.concat([users, new_user], ignore_index=True)
                users.to_csv("data/users.csv", index=False)
                st.success(f"User {new_username} added successfully")
                st.experimental_rerun()
        else:
            st.error("Username and password are required")

def show_question_management():
    st.header("Question Management")
    
    # Load questions
    questions = load_questions()
    
    # Display and edit questions
    with st.expander("All Questions", expanded=True):
        edited_questions = st.data_editor(
            questions,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "question": st.column_config.TextColumn("Question"),
                "option_a": st.column_config.TextColumn("Option A"),
                "option_b": st.column_config.TextColumn("Option B"),
                "option_c": st.column_config.TextColumn("Option C"),
                "option_d": st.column_config.TextColumn("Option D"),
                "correct": st.column_config.SelectboxColumn("Correct Answer", options=["A", "B", "C", "D"])
            }
        )
    
    # Save changes to questions
    if st.button("Save Changes to Questions"):
        edited_questions.to_csv("data/questions.csv", index=False)
        st.success("Questions updated successfully")
    
    # Add new question section
    st.markdown("---")
    st.subheader("Add New Question")
    
    new_question = st.text_area("Question")
    
    col1, col2 = st.columns(2)
    with col1:
        option_a = st.text_input("Option A")
        option_c = st.text_input("Option C")
    with col2:
        option_b = st.text_input("Option B")
        option_d = st.text_input("Option D")
    
    correct_answer = st.selectbox("Correct Answer", ["A", "B", "C", "D"])
    
    if st.button("Add Question"):
        if new_question and option_a and option_b and option_c and option_d:
            # Create question
            new_question_df = pd.DataFrame({
                "question": [new_question],
                "option_a": [option_a],
                "option_b": [option_b],
                "option_c": [option_c],
                "option_d": [option_d],
                "correct": [correct_answer]
            })
            
            questions = pd.concat([questions, new_question_df], ignore_index=True)
            questions.to_csv("data/questions.csv", index=False)
            st.success("Question added successfully")
            st.experimental_rerun()
        else:
            st.error("All fields are required")

def show_all_scores():
    st.header("All Scores")
    
    # Load scores and users
    scores = load_scores()
    users = load_users()
    
    if scores.empty:
        st.info("No scores recorded yet.")
    else:
        # Convert user_id in scores to the same type as id in users
        scores['user_id'] = scores['user_id'].astype(str)
        
        # Now merge should work
        all_scores = scores.merge(users[["id", "name"]], left_on="user_id", right_on="id")
        
        # Sort by score (highest first)
        all_scores = all_scores.sort_values(["score", "date"], ascending=[False, True])
        
        # Display scores with ability to edit
        with st.expander("All Scores", expanded=True):
            display_scores = all_scores[["name", "score", "date", "user_id"]].reset_index(drop=True)
            display_scores.columns = ["Player", "Score", "Date", "User ID"]
            
            edited_scores = st.data_editor(
                display_scores,
                use_container_width=True,
                column_config={
                    "Player": st.column_config.TextColumn("Player", disabled=True),
                    "Score": st.column_config.NumberColumn("Score", min_value=0, max_value=20),
                    "Date": st.column_config.TextColumn("Date"),
                    "User ID": st.column_config.TextColumn("User ID", disabled=True)
                }
            )
        
        # Save edited scores
        if st.button("Save Changes to Scores"):
            # Convert back to original format
            for i, row in edited_scores.iterrows():
                scores.loc[scores['user_id'] == row['User ID'], 'score'] = row['Score']
                scores.loc[scores['user_id'] == row['User ID'], 'date'] = row['Date']
            
            scores.to_csv("data/scores.csv", index=False)
            st.success("Scores updated successfully")
        
        # Delete score functionality
        st.markdown("---")
        st.subheader("Delete Scores")
        
        selected_player = st.selectbox("Select a player:", display_scores["Player"].unique())
        if st.button("Delete All Scores for Selected Player"):
            user_id = all_scores.loc[all_scores["name"] == selected_player, "user_id"].values[0]
            scores = scores[scores["user_id"] != user_id]
            scores.to_csv("data/scores.csv", index=False)
            st.success(f"Deleted all scores for {selected_player}")
            st.experimental_rerun()