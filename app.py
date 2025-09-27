from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import handlers  # your handlers.py file

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
handlers.init_db()

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if handlers.add_user(email, password):
        return jsonify({"success": True, "message": "Signup successful"})
    else:
        return jsonify({"success": False, "message": "User already exists"}), 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if handlers.validate_user(email, password):
        session["user"] = email
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True, "message": "Logged out"})

@app.route("/api/user", methods=["GET"])
def get_user():
    if "user" in session:
        return jsonify({"loggedIn": True, "email": session["user"]})
    return jsonify({"loggedIn": False}), 401

# --------- Resume APIs ---------
@app.route("/api/resume", methods=["POST"])
def upload_resume():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    if "resume" not in request.files:
        return jsonify({"success": False, "message": "Resume file required"}), 400

    resume_file = request.files["resume"]
    category = request.form.get("category", "general")
    filename = secure_filename(resume_file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(path)

    handlers.add_resume(session["user"], filename, category)

    return jsonify({"success": True, "message": "Resume uploaded successfully"})

@app.route("/api/resume", methods=["GET"])
def list_resumes():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    resumes = handlers.get_resumes(session["user"])
    resume_list = [{"resume_id": r[0], "file_name": r[2], "category": r[3]} for r in resumes]
    return jsonify({"success": True, "resumes": resume_list})

# --------- Profile APIs ---------
@app.route("/api/profile", methods=["POST"])
def add_update_profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.json
    linkedin = data.get("linkedin_username")
    github = data.get("github_username")
    stackoverflow = data.get("stackoverflow_username")
    name = data.get("name")
    skills = data.get("skills")  # comma-separated string

    handlers.add_or_update_profile(session["user"], linkedin, github, stackoverflow, name, skills)
    return jsonify({"success": True, "message": "Profile updated successfully"})

@app.route("/api/profile", methods=["GET"])
def get_profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    profile = handlers.get_profile(session["user"])
    if profile:
        profile_data = {
            "linkedin_username": profile[2],
            "github_username": profile[3],
            "stackoverflow_username": profile[4],
            "name": profile[5],
            "skills": profile[6]
        }
        return jsonify({"success": True, "profile": profile_data})
    else:
        return jsonify({"success": False, "message": "Profile not found"}), 404

# --------- Resume Analysis API (Optional AI) ---------
@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    if "resume" not in request.files:
        return jsonify({"success": False, "message": "Resume file required"}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("jobDescription", "")
    github_username = request.form.get("githubUsername", "")
    
    # Save resume file (optional)
    filename = secure_filename(resume_file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(path)

    # Mock AI analysis (replace with your AI logic)
    analysis_result = {
        "aiAnalysis": f"Analyzed resume for {github_username}",
        "skillGaps": ["Docker", "Kubernetes"],  # Example missing skills
        "githubProjects": [
            {"name": "AI Chatbot", "summary": "Built using NLP and Flask"},
            {"name": "Portfolio Website", "summary": "React + Flask full-stack project"}
        ]
    }

    return jsonify(analysis_result)

if __name__ == "__main__":
    app.run(debug=True)

    