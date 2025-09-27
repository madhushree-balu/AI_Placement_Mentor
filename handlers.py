import sqlite3
import json
from datetime import datetime
import PyPDF2
import docx
import os

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Resume table - Enhanced
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resume (
            resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            file_name TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            category TEXT,
            file_size INTEGER,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)

    # Resume Analysis table - New
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            extracted_text TEXT,
            skills_found TEXT, -- JSON string
            experience_years INTEGER,
            education_level TEXT,
            analysis_score INTEGER,
            improvement_suggestions TEXT, -- JSON string
            ats_score INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resume(resume_id)
        )
    """)

    # Profile table - Enhanced
    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            linkedin_username TEXT,
            github_username TEXT,
            stackoverflow_username TEXT,
            name TEXT,
            skills TEXT, -- JSON string
            experience_level TEXT,
            preferred_roles TEXT, -- JSON string
            location TEXT,
            phone TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)

    # Mock Interview Sessions table - New
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            job_title TEXT,
            job_description TEXT,
            difficulty_level TEXT DEFAULT 'intermediate',
            session_type TEXT DEFAULT 'technical', -- technical, behavioral, mixed
            status TEXT DEFAULT 'active', -- active, completed, paused
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)

    # Interview Questions table - New
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            question_type TEXT, -- technical, behavioral, situational
            expected_answer TEXT,
            user_answer TEXT,
            ai_feedback TEXT,
            score INTEGER, -- 1-10 rating
            time_taken INTEGER, -- seconds
            answered_at TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id)
        )
    """)

    # Job Applications Tracker table - New
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            job_description TEXT,
            application_status TEXT DEFAULT 'applied', -- applied, interviewed, rejected, accepted
            applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interview_date TIMESTAMP,
            notes TEXT,
            resume_used INTEGER, -- resume_id
            FOREIGN KEY (user_email) REFERENCES users(email),
            FOREIGN KEY (resume_used) REFERENCES resume(resume_id)
        )
    """)

    conn.commit()
    conn.close()

# User functions - Enhanced
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

# Resume functions - Enhanced
def add_resume(user_email, file_name, original_filename, category, file_size):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resume (user_email, file_name, original_filename, category, file_size) 
        VALUES (?, ?, ?, ?, ?)
    """, (user_email, file_name, original_filename, category, file_size))
    resume_id = cur.lastrowid
    conn.commit()
    conn.close()
    return resume_id

def get_resumes(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, ra.analysis_score, ra.ats_score 
        FROM resume r 
        LEFT JOIN resume_analysis ra ON r.resume_id = ra.resume_id 
        WHERE r.user_email=? 
        ORDER BY r.upload_date DESC
    """, (user_email,))
    resumes = cur.fetchall()
    conn.close()
    return resumes

def get_resume_by_id(resume_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM resume WHERE resume_id=?", (resume_id,))
    resume = cur.fetchone()
    conn.close()
    return resume

def update_resume_analysis_status(resume_id, status):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE resume SET analysis_status=? WHERE resume_id=?", (status, resume_id))
    conn.commit()
    conn.close()

# Resume Analysis functions - New
def save_resume_analysis(resume_id, extracted_text, skills_found, experience_years, 
                        education_level, analysis_score, improvement_suggestions, ats_score):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resume_analysis 
        (resume_id, extracted_text, skills_found, experience_years, education_level, 
         analysis_score, improvement_suggestions, ats_score) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (resume_id, extracted_text, json.dumps(skills_found), experience_years, 
          education_level, analysis_score, json.dumps(improvement_suggestions), ats_score))
    conn.commit()
    conn.close()

def get_resume_analysis(resume_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM resume_analysis WHERE resume_id=? ORDER BY analyzed_at DESC LIMIT 1", (resume_id,))
    analysis = cur.fetchone()
    conn.close()
    return analysis

def extract_text_from_resume(file_path):
    """Extract text from PDF or DOCX resume files"""
    text = ""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        
        elif file_ext == '.docx':
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None
    
    return text.strip()

# Profile functions - Enhanced
def add_or_update_profile(user_email, linkedin, github, stackoverflow, name, skills, 
                         experience_level=None, preferred_roles=None, location=None, phone=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Convert lists to JSON strings if needed
    if isinstance(skills, list):
        skills = json.dumps(skills)
    if isinstance(preferred_roles, list):
        preferred_roles = json.dumps(preferred_roles)
    
    # Check if profile exists
    cur.execute("SELECT * FROM profile WHERE user_email=?", (user_email,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE profile 
            SET linkedin_username=?, github_username=?, stackoverflow_username=?, name=?, 
                skills=?, experience_level=?, preferred_roles=?, location=?, phone=?, 
                updated_at=CURRENT_TIMESTAMP
            WHERE user_email=?
        """, (linkedin, github, stackoverflow, name, skills, experience_level, 
              preferred_roles, location, phone, user_email))
    else:
        cur.execute("""
            INSERT INTO profile 
            (user_email, linkedin_username, github_username, stackoverflow_username, 
             name, skills, experience_level, preferred_roles, location, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_email, linkedin, github, stackoverflow, name, skills, 
              experience_level, preferred_roles, location, phone))
    
    conn.commit()
    conn.close()

def get_profile(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile WHERE user_email=?", (user_email,))
    profile = cur.fetchone()
    conn.close()
    return profile

# Mock Interview functions - New
def create_interview_session(user_email, job_title, job_description, difficulty_level='intermediate', session_type='technical'):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO interview_sessions (user_email, job_title, job_description, difficulty_level, session_type)
        VALUES (?, ?, ?, ?, ?)
    """, (user_email, job_title, job_description, difficulty_level, session_type))
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_interview_session(session_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM interview_sessions WHERE session_id=?", (session_id,))
    session = cur.fetchone()
    conn.close()
    return session

def get_user_interview_sessions(user_email, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM interview_sessions 
        WHERE user_email=? 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (user_email, limit))
    sessions = cur.fetchall()
    conn.close()
    return sessions

def add_interview_question(session_id, question_text, question_type, expected_answer):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO interview_questions (session_id, question_text, question_type, expected_answer)
        VALUES (?, ?, ?, ?)
    """, (session_id, question_text, question_type, expected_answer))
    question_id = cur.lastrowid
    conn.commit()
    conn.close()
    return question_id

def update_interview_answer(question_id, user_answer, ai_feedback, score, time_taken):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        UPDATE interview_questions 
        SET user_answer=?, ai_feedback=?, score=?, time_taken=?, answered_at=CURRENT_TIMESTAMP
        WHERE question_id=?
    """, (user_answer, ai_feedback, score, time_taken, question_id))
    conn.commit()
    conn.close()

def get_session_questions(session_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM interview_questions 
        WHERE session_id=? 
        ORDER BY question_id ASC
    """, (session_id,))
    questions = cur.fetchall()
    conn.close()
    return questions

def complete_interview_session(session_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        UPDATE interview_sessions 
        SET status='completed', completed_at=CURRENT_TIMESTAMP 
        WHERE session_id=?
    """, (session_id,))
    conn.commit()
    conn.close()

def get_interview_statistics(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Get session count and average scores
    cur.execute("""
        SELECT 
            COUNT(*) as total_sessions,
            AVG(CASE WHEN iq.score IS NOT NULL THEN iq.score END) as avg_score,
            COUNT(CASE WHEN is_completed.status = 'completed' THEN 1 END) as completed_sessions
        FROM interview_sessions is_completed
        LEFT JOIN interview_questions iq ON is_completed.session_id = iq.session_id
        WHERE is_completed.user_email = ?
    """, (user_email,))
    
    stats = cur.fetchone()
    conn.close()
    return stats

def delete_resume(resume_id):
    """Delete resume from database"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Delete analysis first (foreign key constraint)
    cur.execute("DELETE FROM resume_analysis WHERE resume_id = ?", (resume_id,))
    
    # Delete resume record
    cur.execute("DELETE FROM resume WHERE resume_id = ?", (resume_id,))
    
    conn.commit()
    conn.close()

def delete_interview_session(session_id):
    """Delete interview session and all related questions"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Delete questions first (foreign key constraint)
    cur.execute("DELETE FROM interview_questions WHERE session_id = ?", (session_id,))
    
    # Delete session
    cur.execute("DELETE FROM interview_sessions WHERE session_id = ?", (session_id,))
    
    conn.commit()
    conn.close()

def get_resume_statistics(user_email):
    """Get resume statistics for dashboard"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            COUNT(*) as total_resumes,
            COUNT(CASE WHEN analysis_status = 'completed' THEN 1 END) as analyzed_resumes,
            AVG(CASE WHEN ra.analysis_score IS NOT NULL THEN ra.analysis_score END) as avg_analysis_score,
            AVG(CASE WHEN ra.ats_score IS NOT NULL THEN ra.ats_score END) as avg_ats_score
        FROM resume r
        LEFT JOIN resume_analysis ra ON r.resume_id = ra.resume_id
        WHERE r.user_email = ?
    """, (user_email,))
    
    stats = cur.fetchone()
    conn.close()
    return stats

def get_recent_activity(user_email, limit=10):
    """Get recent user activity for dashboard"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    activities = []
    
    # Recent resume uploads
    cur.execute("""
        SELECT 'resume_upload' as activity_type, original_filename as description, upload_date as timestamp
        FROM resume 
        WHERE user_email = ? 
        ORDER BY upload_date DESC 
        LIMIT ?
    """, (user_email, limit//2))
    
    resume_activities = cur.fetchall()
    for activity in resume_activities:
        activities.append({
            'type': activity[0],
            'description': f"Uploaded resume: {activity[1]}",
            'timestamp': activity[2]
        })
    
    # Recent interview sessions
    cur.execute("""
        SELECT 'interview_session' as activity_type, job_title as description, created_at as timestamp
        FROM interview_sessions 
        WHERE user_email = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (user_email, limit//2))
    
    interview_activities = cur.fetchall()
    for activity in interview_activities:
        activities.append({
            'type': activity[0],
            'description': f"Started interview for: {activity[1]}",
            'timestamp': activity[2]
        })
    
    # Sort all activities by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    conn.close()
    return activities[:limit]

def get_skill_analysis(user_email):
    """Get aggregated skill analysis from all user's resumes"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT ra.skills_found
        FROM resume r
        JOIN resume_analysis ra ON r.resume_id = ra.resume_id
        WHERE r.user_email = ? AND ra.skills_found IS NOT NULL
    """, (user_email,))
    
    results = cur.fetchall()
    all_skills = {
        'technical_skills': set(),
        'soft_skills': set(),
        'tools_technologies': set()
    }
    
    for result in results:
        try:
            skills_data = json.loads(result[0])
            if isinstance(skills_data, dict):
                for category in all_skills.keys():
                    if category in skills_data and isinstance(skills_data[category], list):
                        all_skills[category].update(skills_data[category])
        except (json.JSONDecodeError, TypeError):
            continue
    
    # Convert sets back to lists
    for category in all_skills:
        all_skills[category] = list(all_skills[category])
    
    conn.close()
    return all_skills

def search_resumes(user_email, query):
    """Search resumes by filename or content"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT r.*, ra.analysis_score, ra.ats_score 
        FROM resume r 
        LEFT JOIN resume_analysis ra ON r.resume_id = ra.resume_id 
        WHERE r.user_email = ? AND (
            r.original_filename LIKE ? OR 
            r.category LIKE ? OR
            ra.extracted_text LIKE ?
        )
        ORDER BY r.upload_date DESC
    """, (user_email, f"%{query}%", f"%{query}%", f"%{query}%"))
    
    results = cur.fetchall()
    conn.close()
    return results

def get_improvement_trends(user_email):
    """Get improvement trends over time for interviews"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            DATE(is_session.created_at) as session_date,
            AVG(iq.score) as avg_score,
            COUNT(iq.question_id) as question_count
        FROM interview_sessions is_session
        JOIN interview_questions iq ON is_session.session_id = iq.session_id
        WHERE is_session.user_email = ? AND iq.score IS NOT NULL
        GROUP BY DATE(is_session.created_at)
        ORDER BY session_date
    """, (user_email,))
    
    trends = cur.fetchall()
    conn.close()
    return trends

# Job Applications functions - New
def add_job_application(user_email, company_name, job_title, job_description=None, resume_used=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO job_applications (user_email, company_name, job_title, job_description, resume_used)
        VALUES (?, ?, ?, ?, ?)
    """, (user_email, company_name, job_title, job_description, resume_used))
    application_id = cur.lastrowid
    conn.commit()
    conn.close()
    return application_id

def get_job_applications(user_email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT ja.*, r.original_filename 
        FROM job_applications ja
        LEFT JOIN resume r ON ja.resume_used = r.resume_id
        WHERE ja.user_email=? 
        ORDER BY ja.applied_date DESC
    """, (user_email,))
    applications = cur.fetchall()
    conn.close()
    return applications

def update_application_status(application_id, status, interview_date=None, notes=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        UPDATE job_applications 
        SET application_status=?, interview_date=?, notes=?
        WHERE application_id=?
    """, (status, interview_date, notes, application_id))
    conn.commit()
    conn.close()