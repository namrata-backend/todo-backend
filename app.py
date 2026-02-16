from flask import Flask, request, jsonify
# 👉 This brings Flask tools into your project.
# Flask → makes the web app (server)
# request → gets data sent by user (POST/PUT data)
# jsonify → converts Python data into JSON format

from flask_sqlalchemy import SQLAlchemy
# 👉 This helps you use database easily with Flask.
# SQLAlchemy = helper to talk to database using Python instead of SQL

from flask_cors import CORS
# 👉 This allows your frontend (website/app) to talk to backend.
# Without this → browser blocks your API (CORS error) ❌

import os
# 👉 This helps work with files and folders in your computer
# Used to find where this file is saved

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# 👉 This is for login security (token system)
# JWTManager → manages tokens
# create_access_token → creates token when user logs in
# jwt_required → protects routes (only logged user can access)
# get_jwt_identity → finds which user is logged in

from werkzeug.security import generate_password_hash, check_password_hash
# 👉 This is for password safety (security)
# Werkzeug is a helper library used by Flask

# ✔ generate_password_hash → converts password into secret code (HASH)
#    Example: "1234" → "pbkdf2:sha256:...."
#    One-way process → cannot get original password back 🔒

# ✔ check_password_hash → compares saved hash with entered password
#    Returns True (correct) or False (wrong)

# -----------------------
# App Configuration
# -----------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 👉 Finds the folder where this Python file is saved

DB_PATH = os.path.join(BASE_DIR, "todo.db")
# 👉 Makes full path for database file "todo.db"
# Example: C:/project/todo.db

app = Flask(__name__)
# 👉 Creates your Flask app (your backend server)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
# 👉 Tells Flask:
# "Use SQLite database and store it in todo.db file"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 👉 Stops unnecessary tracking (saves memory and speed)

db = SQLAlchemy(app)
# 👉 Connects database system to Flask app

CORS(app)
# 👉 Allows frontend (browser) to access this backend

# -----------------------
# Database Model (Database Table)
# -----------------------

class Task(db.Model):
    # 👉 Creates a database table named "Task"

    id = db.Column(db.Integer, primary_key=True)
    # 👉 Unique ID for every task (1,2,3...)

    task = db.Column(db.String(100), nullable=False)
    # 👉 Stores task name (max 100 characters)

    priority = db.Column(db.String(10), nullable=False)
    # 👉 Stores task priority (High/Low/Medium)

    status = db.Column(db.String(20), nullable=False)
    # 👉 Stores task status (Done/Pending/etc)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # 👉 Links task to user
    # Means: this task belongs to this user

    def __repr__(self):
        # 👉 Used for debugging (shows task in terminal nicely)
        return f"<Task {self.id}>"

    def to_dict(self):
        # 👉 Converts task object into dictionary
        # Needed to send data as JSON
        return {
            "id": self.id,
            "task": self.task,
            "priority": self.priority,
            "status": self.status,
            "user_id": self.user_id
        }

# -----------------------
# User Model (User Table)
# -----------------------

class User(db.Model):
    # 👉 Creates user table

    id = db.Column(db.Integer, primary_key=True)
    # 👉 Unique ID for every user

    username = db.Column(db.String(50), unique=True, nullable=False)
    # 👉 Username must be unique (no two same usernames)

    password = db.Column(db.String(200), nullable=False)
    # 👉 Stores hashed password (not real password)

    tasks = db.relationship("Task", backref="user", lazy=True)
    # 👉 Connects User and Task tables
    # One user → many tasks

    def __repr__(self):
        # 👉 Used for debugging (shows user name)
        return f"<User {self.username}>"

# -----------------------
# JWT Configuration
# -----------------------

app.config["JWT_SECRET_KEY"] = "mysecretkey123"
# 👉 Secret key used to sign JWT tokens
# Keeps tokens safe from hacking

jwt = JWTManager(app)
# 👉 Starts JWT system in this app

# -----------------------
# Create Database
# -----------------------

with app.app_context():
    # 👉 Creates database tables if they do not exist
    db.create_all()

# -----------------------
# Home Route
# -----------------------

@app.route("/")
# 👉 When someone opens: http://localhost:5000/

def home():
    # 👉 Function runs for home page
    return jsonify({"message": "Welcome to Todo API"}), 200
    # 👉 Sends JSON message
    # 200 = success status code

# -----------------------
# Register API
# -----------------------

@app.route("/api/register", methods=["POST"])
# 👉 API URL for new user registration

def register():

    data = request.get_json()
    # 👉 Gets JSON data sent by user

    username = data.get("username")
    password = data.get("password")
    # 👉 Extract username and password

    if not username or not password:
        # 👉 If any field is empty → error
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        # 👉 Checks if username already exists
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    # 👉 Converts password into secure hash

    user = User(
        username=username,
        password=hashed_password
    )
    # 👉 Creates new user object

    db.session.add(user)
    db.session.commit()
    # 👉 Saves user into database

    return jsonify({"message": "User registered successfully"}), 201
    # 👉 201 = created successfully

# -----------------------
# Login API
# -----------------------

@app.route("/api/login", methods=["POST"])
# 👉 API URL for login

def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    # 👉 Finds user in database

    if not user or not check_password_hash(user.password, password):
        # 👉 If username or password is wrong
        return jsonify({"error": "Invalid login"}), 401

    token = create_access_token(identity=str(user.id))
    # 👉 Creates JWT token for logged user

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

# -----------------------
# Create Task
# -----------------------

@app.route("/api/tasks", methods=["POST"])
@jwt_required()
# 👉 Only logged-in users can create tasks

def create_task():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["task", "priority", "status"]
    # 👉 Required fields list

    if not all(key in data for key in required):
        # 👉 Checks if any field is missing
        return jsonify({"error": "Missing required fields"}), 400

    user_id = int(get_jwt_identity())
    # 👉 Gets ID of logged-in user

    print("Creating task for user:", user_id)
    # 👉 Prints in terminal (for debugging)

    new_task = Task(
        task=data["task"],
        priority=data["priority"],
        status=data["status"],
        user_id=user_id
    )
    # 👉 Creates new task object

    db.session.add(new_task)
    db.session.commit()
    # 👉 Saves task in database

    return jsonify({
        "message": "Task created successfully",
        "task": new_task.to_dict()
    }), 201

# -----------------------
# Get All Tasks
# -----------------------

@app.route("/api/tasks", methods=["GET"])
@jwt_required()

def get_tasks():

    user_id = int(get_jwt_identity())
    # 👉 Gets logged-in user ID

    print("Getting tasks for user:", user_id)

    tasks = Task.query.filter_by(user_id=user_id).all()
    # 👉 Gets only tasks of this user

    return jsonify([t.to_dict() for t in tasks]), 200

# -----------------------
# Get Single Task
# -----------------------

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
# 👉 <int:task_id> gets task ID from URL

@jwt_required()

def get_task(task_id):

    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    # 👉 Finds task and checks owner (security)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict()), 200

# -----------------------
# Update Task
# -----------------------

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()

def update_task(task_id):

    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    # 👉 Finds task owned by user

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    task.task = data.get("task", task.task)
    # 👉 Update only if new value exists

    task.priority = data.get("priority", task.priority)
    task.status = data.get("status", task.status)

    db.session.commit()
    # 👉 Saves changes

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()
    }), 200

# -----------------------
# Delete Task
# -----------------------

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()

def delete_task(task_id):

    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    # 👉 Finds task owned by user

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    # 👉 Removes task from database

    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200

# -----------------------
# Run Server
# -----------------------

if __name__ == "__main__":
    # 👉 Runs only when this file is executed directly

    app.run(debug=True)
    # 👉 Starts server
    # debug=True → shows errors on screen
