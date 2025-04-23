import streamlit as st
import pandas as pd
import time
from datetime import datetime
from utils import load_questions, save_score

def show_game():
    # Initialize or retrieve session state variables
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = time.time()
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    
    # Load questions
    questions = load_questions()
    total_questions = len(questions)
    
    if total_questions < 20:
        st.warning(f"Warning: Only {total_questions} questions available. The quiz is designed for 20 questions.")
    
    # Display header with score - FIX SCORE DISPLAY FORMAT
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Church Music Quiz")
    with col2:
        # Show questions answered as denominator rather than question index
        st.metric("Score", f"{st.session_state.score}/{total_questions}")
    # End game if all questions answered
    if st.session_state.question_index >= min(20, total_questions):
        show_game_end()
        return
    
    # Get current question
    question = questions.iloc[st.session_state.question_index]
    
    # Display question
    st.subheader(f"Question {st.session_state.question_index + 1}: {question['question']}")
    
    # Calculate remaining time
    elapsed = time.time() - st.session_state.timer_start
    remaining = max(0, 10 - elapsed)
    
    # Display timer
    progress = st.progress(remaining / 10)
    st.write(f"Time remaining: {int(remaining)} seconds")
    
    # Display options
    options = {
        "A": question["option_a"],
        "B": question["option_b"],
        "C": question["option_c"],
        "D": question["option_d"]
    }
    
    # Disable options if already answered
    disabled = st.session_state.answered
    
    selected_option = st.radio(
        "Select your answer:",
        ["A", "B", "C", "D"],
        format_func=lambda x: f"{x}: {options[x]}",
        disabled=disabled,
        key=f"question_{st.session_state.question_index}"
    )
    
    # Display feedback if available
    if st.session_state.feedback:
        if "Correct" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        elif "Wrong" in st.session_state.feedback:
            st.error(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)
    
    # Check answer when selected
    if not st.session_state.answered and st.button("Submit Answer", key="submit_answer"):
        correct_answer = question["correct"]
        if selected_option == correct_answer:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ Correct! The answer is {correct_answer}."
        else:
            st.session_state.feedback = f"❌ Wrong! The correct answer is {correct_answer}."
        st.session_state.answered = True
        st.rerun()
    
    # Next question button
    if st.session_state.answered and st.button("Next Question", key="next_question"):
        st.session_state.question_index += 1
        st.session_state.timer_start = time.time()
        st.session_state.answered = False
        st.session_state.feedback = None
        st.rerun()
    
  
 
    
    # Auto-advance if time's up
    if remaining <= 0 and not st.session_state.answered:
        st.session_state.feedback = "Time's up! ⏰"
        st.session_state.answered = True
        st.rerun()
    
    # Auto-refresh timer
    if not st.session_state.answered and remaining > 0:
        time.sleep(0.1)  # Small delay to prevent excessive reruns
        st.rerun()

def show_game_end():
    st.title("Quiz Complete!")
    
    # Display final score
    st.balloons()
    st.success(f"Congratulations! Your final score is: {st.session_state.score}/20")
    
    # Save score to leaderboard
    if st.session_state.get("logged_in", False):
        save_score(
            st.session_state.user_id,
            st.session_state.score,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    # Show options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.timer_start = time.time()
            st.session_state.answered = False
            st.session_state.feedback = None
            st.experimental_rerun()
    with col2:
        if st.button("View Leaderboard"):
            st.session_state.page = "leaderboard"
            st.experimental_rerun()