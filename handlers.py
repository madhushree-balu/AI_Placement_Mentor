import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Resume table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resume (
            resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            file_name TEXT NOT NULL,
            category TEXT,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)

    # Profile table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            linkedin_username TEXT,
            github_username TEXT,
            stackoverflow_username TEXT,
            name TEXT,
            skills TEXT,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)

    conn.commit()
    conn.close()

# User functions
def add_user(email, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def validate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user is not None

def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

# Resume functions
def add_resume(user_email, file_name, category):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO resume (user_email, file_name, category) VALUES (?, ?, ?)",
                (user_email, file_name, category))
    conn.commit()
    conn.close()

def get_resumes(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM resume WHERE user_email=?", (user_email,))
    resumes = cur.fetchall()
    conn.close()
    return resumes

# Profile functions
def add_or_update_profile(user_email, linkedin, github, stackoverflow, name, skills):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Check if profile exists
    cur.execute("SELECT * FROM profile WHERE user_email=?", (user_email,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE profile 
            SET linkedin_username=?, github_username=?, stackoverflow_username=?, name=?, skills=?
            WHERE user_email=?
        """, (linkedin, github, stackoverflow, name, skills, user_email))
    else:
        cur.execute("""
            INSERT INTO profile (user_email, linkedin_username, github_username, stackoverflow_username, name, skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_email, linkedin, github, stackoverflow, name, skills))
    
    conn.commit()
    conn.close()

def get_profile(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile WHERE user_email=?", (user_email,))
    profile = cur.fetchone()
    conn.close()
    return profile
