from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
import handlers  # your handlers.py file

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
handlers.init_db()


# -------------------- ROUTES FOR PAGES -------------------- #

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("home"))
    return render_template("index.html", error=None)

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if handlers.add_user(email, password):
            return redirect(url_for("index"))
        else:
            return render_template("signup.html", error="User already exists")
    return render_template("signup.html", error=None)

@app.route("/login", methods=["POST"])
def login_page():
    email = request.form.get("email")
    password = request.form.get("password")
    if handlers.validate_user(email, password):
        session["user"] = email
        return redirect(url_for("home"))
    else:
        return render_template("index.html", error="Invalid credentials")

@app.route("/logout")
def logout_page():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("home.html", user=session["user"])


# -------------------- RESUME ROUTES -------------------- #

@app.route("/upload_resume_page", methods=["GET", "POST"])
def upload_resume_page():
    if "user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("upload_resume.html", error="No file uploaded")
        resume_file = request.files["resume"]
        category = request.form.get("category", "general")
        filename = secure_filename(resume_file.filename)
        resume_file.save(os.path.join(UPLOAD_FOLDER, filename))
        handlers.add_resume(session["user"], filename, category)
        return render_template("upload_resume.html", success="Resume uploaded!")

    return render_template("upload_resume.html", error=None)


@app.route("/list_resumes")
def list_resumes():
    if "user" not in session:
        return redirect(url_for("index"))
    resumes = handlers.get_resumes(session["user"])
    return render_template("list_resumes.html", resumes=resumes)


# -------------------- PROFILE ROUTES -------------------- #

@app.route("/profile_page", methods=["GET", "POST"])
def profile_page():
    if "user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        linkedin = request.form.get("linkedin_username")
        github = request.form.get("github_username")
        stackoverflow = request.form.get("stackoverflow_username")
        name = request.form.get("name")
        skills = request.form.get("skills")
        handlers.add_or_update_profile(session["user"], linkedin, github, stackoverflow, name, skills)
        return render_template("profile.html", success="Profile updated successfully", profile=request.form)

    profile = handlers.get_profile(session["user"])
    return render_template("profile.html", profile=profile, success=None)


# -------------------- RESUME ANALYSIS ROUTE (Optional) -------------------- #

@app.route("/analyze_page", methods=["GET", "POST"])
def analyze_page():
    if "user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("analyze.html", error="No resume uploaded")

        resume_file = request.files["resume"]
        job_description = request.form.get("jobDescription", "")
        github_username = request.form.get("githubUsername", "")
        filename = secure_filename(resume_file.filename)
        resume_file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Mock AI analysis (replace with actual AI logic later)
        analysis_result = {
            "aiAnalysis": f"Analyzed resume for {github_username}",
            "skillGaps": ["Docker", "Kubernetes"],
            "githubProjects": [
                {"name": "AI Chatbot", "summary": "Built using NLP and Flask"},
                {"name": "Portfolio Website", "summary": "React + Flask full-stack project"}
            ]
        }

        return render_template("analyze.html", result=analysis_result, error=None)

    return render_template("analyze.html", result=None, error=None)


# -------------------- RUN APP -------------------- #
if __name__ == "__main__":
    app.run(debug=True)
