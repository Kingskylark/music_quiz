import pandas as pd
import os
import hashlib
import uuid

# --- File paths ---
USERS_FILE = "data/users.csv"
SCORES_FILE = "data/scores.csv"
QUESTIONS_FILE = "data/questions.csv"

# --- User management functions ---
def load_users():
    """Load users from CSV or create it if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        
        # Create empty users file with columns
        users = pd.DataFrame(columns=["id", "name", "password", "role"])
        users.to_csv(USERS_FILE, index=False)
        return users
    else:
        return pd.read_csv(USERS_FILE)

def save_user(username, password, role="user"):
    """Save a new user to the users file"""
    users = load_users()
    
    # Create a unique ID
    user_id = str(uuid.uuid4())
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Add the new user
    new_user = pd.DataFrame({
        "id": [user_id],
        "name": [username],
        "password": [hashed_password],
        "role": [role]
    })
    
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)
    
    return user_id

def verify_login(username, password):
    """Verify login credentials"""
    users = load_users()
    
    # Check if username exists
    if username not in users["name"].values:
        return False
    
    # Get stored password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    stored_password = users.loc[users["name"] == username, "password"].values[0]
    
    return hashed_password == stored_password

def get_user_id(username):
    """Get user ID from username"""
    users = load_users()
    if username in users["name"].values:
        return users.loc[users["name"] == username, "id"].values[0]
    return None

# --- Score management functions ---
def load_scores():
    """Load scores from CSV or create it if it doesn't exist"""
    if not os.path.exists(SCORES_FILE):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
        
        # Create empty scores file with columns
        scores = pd.DataFrame(columns=["user_id", "score", "date"])
        scores.to_csv(SCORES_FILE, index=False)
        return scores
    else:
        return pd.read_csv(SCORES_FILE)

def save_score(user_id, score, date):
    """Save a user's score to the scores file"""
    scores = load_scores()
    
    # Add the new score
    new_score = pd.DataFrame({
        "user_id": [user_id],
        "score": [score],
        "date": [date]
    })
    
    scores = pd.concat([scores, new_score], ignore_index=True)
    scores.to_csv(SCORES_FILE, index=False)

# --- Question management functions ---
def load_questions():
    """Load questions from CSV or create a sample file if it doesn't exist"""
    if not os.path.exists(QUESTIONS_FILE):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
        
        # Create sample questions file
        questions = pd.DataFrame({
            "question": [
                "Which of these is NOT one of the four parts in traditional hymn singing?",
                "Who composed 'Amazing Grace'?",
                "What instrument is traditionally used to lead congregational singing?",
                "Which book of the Bible contains most of the Psalms?",
                "What is the term for a song of praise to God?"
            ],
            "option_a": [
                "Soprano", 
                "John Newton", 
                "Piano", 
                "Proverbs", 
                "Hymn"
            ],
            "option_b": [
                "Alto", 
                "Charles Wesley", 
                "Guitar", 
                "Psalms", 
                "Anthem"
            ],
            "option_c": [
                "Tenor", 
                "Isaac Watts", 
                "Organ", 
                "Ecclesiastes", 
                "Spiritual"
            ],
            "option_d": [
                "Baritone", 
                "Fanny Crosby", 
                "Trumpet", 
                "Song of Solomon", 
                "Carol"
            ],
            "correct": ["D", "A", "C", "B", "A"]
        })
        questions.to_csv(QUESTIONS_FILE, index=False)
        return questions
    else:
        return pd.read_csv(QUESTIONS_FILE)


# Add this to utils.py
def create_admin_if_not_exists():
    """Create an admin user if one doesn't exist"""
    users = load_users()
    if "admin" not in users["role"].values:
        save_user("admin", "admin123", role="admin")  # Default admin credentials