from flask import Flask, request, jsonify, session
import handlers

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
        return jsonify({"success": False, "message": "User already exists or error occurred"}), 400

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


@app.route("/api/user", methods=["GET"])
def get_user():
    if "user" in session:
        return jsonify({"loggedIn": True, "email": session["user"]})
    return jsonify({"loggedIn": False}), 401

if __name__ == "__main__":
    app.run(debug=True)
