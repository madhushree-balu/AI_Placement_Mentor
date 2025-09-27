from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash, send_file
from werkzeug.utils import secure_filename
import os
import handlers  # your handlers.py file
from gemini_wrapper import GeminiWrapper
import json
import time
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key_change_in_production"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database and AI wrapper
handlers.init_db()
gemini = GeminiWrapper()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    return os.path.getsize(file_path)

# -------------------- ROUTES FOR PAGES -------------------- #

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html", error=None)

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if handlers.add_user(email, password):
            flash("Account created successfully! Please log in.", "success")
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
        flash(f"Welcome back, {email}!", "success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Invalid credentials")

@app.route("/logout")
def logout_page():
    user_email = session.get("user", "")
    session.clear()
    flash(f"Goodbye, {user_email}! You've been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    
    # Get user statistics
    user_email = session["user"]
    resumes = handlers.get_resumes(user_email)
    profile = handlers.get_profile(user_email)
    interview_stats = handlers.get_interview_statistics(user_email)
    recent_sessions = handlers.get_user_interview_sessions(user_email, limit=5)
    job_applications = handlers.get_job_applications(user_email)
    
    stats = {
        'total_resumes': len(resumes),
        'analyzed_resumes': len([r for r in resumes if r[7] == 'completed']),  # analysis_status
        'total_interviews': interview_stats[0] if interview_stats else 0,
        'avg_interview_score': round(interview_stats[1], 1) if interview_stats and interview_stats[1] else 0,
        'job_applications': len(job_applications),
        'profile_complete': bool(profile and profile[4])  # name field
    }
    
    return render_template("dashboard.html", 
                         user=user_email, 
                         stats=stats,
                         recent_sessions=recent_sessions[:3])

@app.route("/home")
def home():
    return redirect(url_for("dashboard"))

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
        
        if resume_file.filename == '':
            return render_template("upload_resume.html", error="No file selected")
        
        if resume_file and allowed_file(resume_file.filename):
            original_filename = resume_file.filename
            filename = secure_filename(f"{int(time.time())}_{original_filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save file temporarily to check size
            resume_file.save(file_path)
            file_size = get_file_size(file_path)
            
            if file_size > MAX_FILE_SIZE:
                os.remove(file_path)
                return render_template("upload_resume.html", 
                                     error="File too large. Maximum size is 16MB.")
            
            # Add to database
            resume_id = handlers.add_resume(session["user"], filename, original_filename, category, file_size)
            
            # Start background analysis
            threading.Thread(target=analyze_resume_background, args=(resume_id, file_path)).start()
            
            flash("Resume uploaded successfully! Analysis will be ready in a few minutes.", "success")
            return redirect(url_for("list_resumes"))
        else:
            return render_template("upload_resume.html", 
                                 error="Invalid file format. Please upload PDF, DOC, DOCX, or TXT files.")

    return render_template("upload_resume.html", error=None)

def analyze_resume_background(resume_id, file_path):
    """Background task to analyze resume"""
    try:
        handlers.update_resume_analysis_status(resume_id, 'analyzing')
        
        # Extract text
        extracted_text = handlers.extract_text_from_resume(file_path)
        if not extracted_text:
            handlers.update_resume_analysis_status(resume_id, 'failed')
            return
        
        # Analyze with AI
        analysis_result = gemini.analyze_resume_content(extracted_text)
        
        # Save analysis to database
        handlers.save_resume_analysis(
            resume_id=resume_id,
            extracted_text=extracted_text,
            skills_found=analysis_result.get('skills', {}),
            experience_years=analysis_result.get('experience', {}).get('years_experience', 0),
            education_level=analysis_result.get('education', {}).get('highest_degree', ''),
            analysis_score=analysis_result.get('scores', {}).get('overall_strength', 50),
            improvement_suggestions=analysis_result.get('missing_elements', []),
            ats_score=analysis_result.get('scores', {}).get('ats_compatibility', 50)
        )
        
        handlers.update_resume_analysis_status(resume_id, 'completed')
        
    except Exception as e:
        print(f"Error analyzing resume {resume_id}: {e}")
        handlers.update_resume_analysis_status(resume_id, 'failed')

@app.route("/list_resumes")
def list_resumes():
    if "user" not in session:
        return redirect(url_for("index"))
    resumes = handlers.get_resumes(session["user"])
    return render_template("list_resumes.html", resumes=resumes)

@app.route("/resume_analysis/<int:resume_id>")
def resume_analysis(resume_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    resume = handlers.get_resume_by_id(resume_id)
    if not resume or resume[1] != session["user"]:  # user_email check
        flash("Resume not found or access denied.", "error")
        return redirect(url_for("list_resumes"))
    
    analysis = handlers.get_resume_analysis(resume_id)
    if not analysis:
        flash("Analysis not available yet. Please try again later.", "warning")
        return redirect(url_for("list_resumes"))
    
    # Parse JSON fields
    try:
        skills_found = json.loads(analysis[3]) if analysis[3] else {}
        improvement_suggestions = json.loads(analysis[6]) if analysis[6] else []
    except json.JSONDecodeError:
        skills_found = {}
        improvement_suggestions = []
    
    return render_template("resume_analysis.html", 
                         resume=resume, 
                         analysis=analysis,
                         skills_found=skills_found,
                         improvement_suggestions=improvement_suggestions)

@app.route("/improve_resume/<int:resume_id>", methods=["GET", "POST"])
def improve_resume(resume_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    resume = handlers.get_resume_by_id(resume_id)
    if not resume or resume[1] != session["user"]:
        flash("Resume not found or access denied.", "error")
        return redirect(url_for("list_resumes"))
    
    if request.method == "POST":
        job_description = request.form.get("job_description", "")
        
        # Get resume analysis
        analysis = handlers.get_resume_analysis(resume_id)
        if not analysis:
            flash("Please wait for initial analysis to complete.", "warning")
            return redirect(url_for("resume_analysis", resume_id=resume_id))
        
        # Get improvement suggestions
        try:
            improvement_suggestions = gemini.get_resume_improvement_suggestions(
                analysis[2], job_description  # extracted_text
            )
            
            if job_description:
                # Also get job matching analysis
                job_match = gemini.match_resume_to_job(analysis[2], job_description)
                return render_template("improve_resume.html", 
                                     resume=resume,
                                     improvements=improvement_suggestions,
                                     job_match=job_match,
                                     job_description=job_description)
            else:
                return render_template("improve_resume.html", 
                                     resume=resume,
                                     improvements=improvement_suggestions)
        except Exception as e:
            flash(f"Error generating improvements: {str(e)}", "error")
            return redirect(url_for("resume_analysis", resume_id=resume_id))
    
    return render_template("improve_resume.html", resume=resume)

# -------------------- PROFILE ROUTES -------------------- #

@app.route("/profile_page", methods=["GET", "POST"])
def profile_page():
    if "user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        linkedin = request.form.get("linkedin_username")
        github = request.form.get("github_username")
        stackoverflow = request.form.get("stackoverflow_username")
        skills = request.form.get("skills")
        experience_level = request.form.get("experience_level")
        preferred_roles = request.form.get("preferred_roles")
        location = request.form.get("location")
        phone = request.form.get("phone")
        
        # Convert comma-separated strings to JSON lists
        if skills:
            skills = [skill.strip() for skill in skills.split(',')]
        if preferred_roles:
            preferred_roles = [role.strip() for role in preferred_roles.split(',')]
        
        handlers.add_or_update_profile(
            session["user"], linkedin, github, stackoverflow, name, skills,
            experience_level, preferred_roles, location, phone
        )
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile_page"))

    profile = handlers.get_profile(session["user"])
    
    # Parse JSON fields for display
    if profile:
        try:
            skills = json.loads(profile[5]) if profile[5] else []
            preferred_roles = json.loads(profile[7]) if profile[7] else []
            profile = list(profile)  # Convert tuple to list for modification
            profile[5] = ', '.join(skills) if isinstance(skills, list) else skills
            profile[7] = ', '.join(preferred_roles) if isinstance(preferred_roles, list) else preferred_roles
        except (json.JSONDecodeError, IndexError):
            pass
    
    return render_template("profile.html", profile=profile)

# -------------------- MOCK INTERVIEW ROUTES -------------------- #

@app.route("/interview", methods=["GET", "POST"])
def interview():
    if "user" not in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        job_title = request.form.get("job_title", "").strip()
        job_description = request.form.get("job_description", "").strip()
        difficulty_level = request.form.get("difficulty_level", "intermediate")
        session_type = request.form.get("session_type", "technical")
        
        if not job_title or not job_description:
            flash("Please provide both job title and description.", "error")
            return render_template("interview_setup.html")
        
        # Create new interview session
        session_id = handlers.create_interview_session(
            session["user"], job_title, job_description, difficulty_level, session_type
        )
        
        # Store in session for easy access
        session["current_interview"] = session_id
        
        flash("Interview session created! Let's begin.", "success")
        return redirect(url_for("interview_session", session_id=session_id))
    
    # Get user's recent sessions for display
    recent_sessions = handlers.get_user_interview_sessions(session["user"], limit=5)
    return render_template("interview_setup.html", recent_sessions=recent_sessions)

@app.route("/interview_session/<int:session_id>", methods=["GET", "POST"])
def interview_session(session_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    interview_session_data = handlers.get_interview_session(session_id)
    if not interview_session_data or interview_session_data[1] != session["user"]:
        flash("Interview session not found or access denied.", "error")
        return redirect(url_for("interview"))
    
    if request.method == "POST":
        # Handle answer submission
        question_id = request.form.get("question_id")
        user_answer = request.form.get("answer", "").strip()
        time_taken = int(request.form.get("time_taken", 0))
        
        if question_id and user_answer:
            # Get question details
            questions = handlers.get_session_questions(session_id)
            current_question = next((q for q in questions if str(q[0]) == question_id), None)
            
            if current_question:
                try:
                    # Validate answer based on question type
                    if current_question[3] == 'behavioral':  # question_type
                        validation_result = gemini.validate_behavioral_answer(
                            current_question[1], user_answer  # question_text, user_answer
                        )
                    else:
                        validation_result = gemini.validate_tech_question_answer(
                            current_question[1], user_answer, current_question[4]  # question, answer, expected
                        )
                    
                    validation_data = json.loads(validation_result)
                    score = validation_data.get("score", 5)
                    ai_feedback = validation_data.get("overall_feedback", "No feedback available")
                    
                    # Update question with answer and feedback
                    handlers.update_interview_answer(
                        question_id, user_answer, ai_feedback, score, time_taken
                    )
                    
                    # Store feedback in session for display
                    session["last_feedback"] = {
                        "question": current_question[1],
                        "user_answer": user_answer,
                        "feedback": validation_data,
                        "score": score
                    }
                    
                    return redirect(url_for("interview_session", session_id=session_id))
                    
                except Exception as e:
                    flash(f"Error processing answer: {str(e)}", "error")
    
    # Check if we need to generate a new question
    questions = handlers.get_session_questions(session_id)
    unanswered_questions = [q for q in questions if not q[5]]  # user_answer is None
    
    current_question = None
    if unanswered_questions:
        current_question = unanswered_questions[0]
    elif len(questions) < 10:  # Limit to 10 questions per session
        # Generate new question
        try:
            answered_questions = [q[1] for q in questions]  # question_text
            
            if interview_session_data[5] == 'behavioral':  # session_type
                question_response = gemini.get_behavioral_question(
                    interview_session_data[3], answered_questions  # job_description
                )
            elif interview_session_data[5] == 'mixed':
                question_response = gemini.get_mixed_question(
                    interview_session_data[3], answered_questions
                )
            else:  # technical
                question_response = gemini.get_tech_question(
                    interview_session_data[3], answered_questions, interview_session_data[4]  # difficulty
                )
            
            question_data = json.loads(question_response)
            
            # Add question to database
            question_id = handlers.add_interview_question(
                session_id,
                question_data["question"],
                question_data.get("question_type", "technical"),
                question_data.get("answer", "")
            )
            
            # Refresh questions list
            questions = handlers.get_session_questions(session_id)
            current_question = questions[-1]  # Get the newly added question
            
        except Exception as e:
            flash(f"Error generating question: {str(e)}", "error")
            return redirect(url_for("interview_results", session_id=session_id))
    
    # If no current question and we've reached the limit, end the session
    if not current_question:
        handlers.complete_interview_session(session_id)
        return redirect(url_for("interview_results", session_id=session_id))
    
    # Get feedback from last answer if available
    last_feedback = session.pop("last_feedback", None)
    
    return render_template("interview_session.html",
                         interview_session=interview_session_data,
                         current_question=current_question,
                         question_number=len(questions),
                         total_questions=min(10, len(questions) + 1),
                         last_feedback=last_feedback)

@app.route("/interview_results/<int:session_id>")
def interview_results(session_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    interview_session_data = handlers.get_interview_session(session_id)
    if not interview_session_data or interview_session_data[1] != session["user"]:
        flash("Interview session not found.", "error")
        return redirect(url_for("interview"))
    
    questions = handlers.get_session_questions(session_id)
    answered_questions = [q for q in questions if q[5]]  # Has user_answer
    
    if not answered_questions:
        flash("No answers to analyze yet.", "warning")
        return redirect(url_for("interview_session", session_id=session_id))
    
    # Calculate statistics
    total_score = sum(q[7] for q in answered_questions if q[7])  # score
    avg_score = total_score / len(answered_questions) if answered_questions else 0
    total_time = sum(q[8] for q in answered_questions if q[8])  # time_taken
    
    # Prepare data for detailed report generation
    session_data = {
        "job_title": interview_session_data[2],
        "session_type": interview_session_data[5],
        "difficulty_level": interview_session_data[4],
        "questions": [
            {
                "question": q[1],
                "user_answer": q[5],
                "ai_feedback": q[6],
                "score": q[7],
                "time_taken": q[8]
            }
            for q in answered_questions
        ]
    }
    
    # Generate comprehensive feedback report
    try:
        detailed_report = gemini.generate_interview_feedback_report(session_data)
    except:
        detailed_report = "Detailed report generation temporarily unavailable."
    
    stats = {
        "total_questions": len(answered_questions),
        "avg_score": round(avg_score, 1),
        "total_time": total_time,
        "avg_time_per_question": round(total_time / len(answered_questions)) if answered_questions else 0
    }
    
    return render_template("interview_results.html",
                         interview_session=interview_session_data,
                         questions=answered_questions,
                         stats=stats,
                         detailed_report=detailed_report)

@app.route("/interview_history")
def interview_history():
    if "user" not in session:
        return redirect(url_for("index"))
    
    sessions = handlers.get_user_interview_sessions(session["user"], limit=20)
    return render_template("interview_history.html", sessions=sessions)

@app.route("/practice_questions")
def practice_questions():
    if "user" not in session:
        return redirect(url_for("index"))
    
    # This could be enhanced to show personalized practice questions
    # based on user's weak areas from previous interviews
    return render_template("practice_questions.html")

# -------------------- JOB APPLICATIONS TRACKER -------------------- #

@app.route("/job_tracker", methods=["GET", "POST"])
def job_tracker():
    if "user" not in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        company_name = request.form.get("company_name")
        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")
        resume_used = request.form.get("resume_used")
        
        if company_name and job_title:
            resume_id = int(resume_used) if resume_used and resume_used != "0" else None
            handlers.add_job_application(session["user"], company_name, job_title, job_description, resume_id)
            flash("Job application added successfully!", "success")
        else:
            flash("Company name and job title are required.", "error")
    
    applications = handlers.get_job_applications(session["user"])
    resumes = handlers.get_resumes(session["user"])
    
    return render_template("job_tracker.html", applications=applications, resumes=resumes)

@app.route("/update_application/<int:application_id>", methods=["POST"])
def update_application(application_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    status = request.form.get("status")
    notes = request.form.get("notes")
    interview_date = request.form.get("interview_date")
    
    handlers.update_application_status(application_id, status, interview_date, notes)
    flash("Application updated successfully!", "success")
    return redirect(url_for("job_tracker"))

# -------------------- ROADMAP ROUTES -------------------- #

@app.route("/roadmaps", methods=["GET", "POST"])
def roadmaps():
    if "user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        if not description:
            return render_template("roadmaps.html", error="Please provide a description")
        
        try:
            # Generate roadmap using Gemini AI
            roadmap_plantuml = gemini.generate_roadmap(description)
            return render_template("roadmaps.html", 
                                 roadmap=roadmap_plantuml, 
                                 description=description,
                                 success="Roadmap generated successfully!")
        except Exception as e:
            return render_template("roadmaps.html", 
                                 error=f"Failed to generate roadmap: {str(e)}")

    return render_template("roadmaps.html")

# -------------------- API ROUTES -------------------- #

@app.route("/api/generate_roadmap", methods=["POST"])
def api_generate_roadmap():
    """API endpoint for generating roadmaps"""
    if "user" not in session:
        return jsonify({"error": "Authentication required"}), 401
    
    data = request.get_json()
    description = data.get("description", "").strip()
    
    if not description:
        return jsonify({"error": "Description is required"}), 400
    
    try:
        roadmap_plantuml = gemini.generate_roadmap(description)
        return jsonify({
            "success": True,
            "roadmap": roadmap_plantuml,
            "description": description
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/resume_quick_scan", methods=["POST"])
def api_resume_quick_scan():
    """Quick resume scan API for immediate feedback"""
    if "user" not in session:
        return jsonify({"error": "Authentication required"}), 401
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400
    
    try:
        # Save temporary file
        temp_filename = f"temp_{int(time.time())}_{secure_filename(file.filename)}"
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(temp_path)
        
        # Extract and analyze
        text = handlers.extract_text_from_resume(temp_path)
        if text:
            analysis = gemini.analyze_resume_content(text)
            # Clean up temp file
            os.remove(temp_path)
            
            return jsonify({
                "success": True,
                "analysis": analysis
            })
        else:
            os.remove(temp_path)
            return jsonify({"error": "Could not extract text from file"}), 400
            
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500

# -------------------- ERROR HANDLERS -------------------- #

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

@app.errorhandler(413)
def too_large(error):
    flash("File too large. Maximum size is 16MB.", "error")
    return redirect(request.url)

# -------------------- UTILITY ROUTES -------------------- #

@app.route("/download_resume/<int:resume_id>")
def download_resume(resume_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    resume = handlers.get_resume_by_id(resume_id)
    if not resume or resume[1] != session["user"]:
        flash("Resume not found or access denied.", "error")
        return redirect(url_for("list_resumes"))
    
    file_path = os.path.join(UPLOAD_FOLDER, resume[2])  # file_name
    if os.path.exists(file_path):
        return send_file(file_path, 
                        as_attachment=True, 
                        download_name=resume[3])  # original_filename
    else:
        flash("File not found on server.", "error")
        return redirect(url_for("list_resumes"))

@app.route("/delete_resume/<int:resume_id>", methods=["POST"])
def delete_resume_route(resume_id):
    if "user" not in session:
        return redirect(url_for("index"))
    
    resume = handlers.get_resume_by_id(resume_id)
    if not resume or resume[1] != session["user"]:
        flash("Resume not found or access denied.", "error")
        return redirect(url_for("list_resumes"))
    
    # Delete file from filesystem
    file_path = os.path.join(UPLOAD_FOLDER, resume[2])
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    handlers.delete_resume(resume_id)
    flash("Resume deleted successfully.", "success")
    return redirect(url_for("list_resumes"))

# -------------------- RUN APP -------------------- #
if __name__ == "__main__":
    app.run(debug=True, threaded=True)