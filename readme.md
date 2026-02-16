# create virtual env


1. python -m venv mytodo-venv 

2. activate : .\mytodo-venv\Scripts\activate

3. deactivate : .\mytodo-venv\Scripts\deactivate.bat 


# freeze requirements.txt

1. cmd : pip freeze > requirements.txt

2. pip install -r requirements.txt

# for sqlite
pip install flask-sqlalchemy
pip show flask-sqlalchemy



# ✅ PERFECT INTERVIEW EXPLANATION (MEMORIZE THIS)
Sir/Ma’am, I developed a secure Todo REST API using Flask.
It is a backend project where users can register, login, and manage their personal tasks.
I used Flask for building APIs, SQLAlchemy for database handling, and SQLite as storage.
For authentication, I implemented JWT-based login system, so every user gets a secure token after login.
All protected APIs like creating, updating, and deleting tasks require a valid JWT token.
Passwords are never stored in plain text. I used Werkzeug hashing to encrypt passwords before saving them in database.
Each task is linked with a user ID, so users can only access their own tasks.
I implemented full CRUD operations: Create, Read, Update, and Delete for tasks.
The API also supports CORS for frontend integration.
Overall, this project focuses on security, scalability, and clean API design.

# Q EXPLAIN YOUR ARCHITECTURE
My project follows REST architecture.
The client sends HTTP requests.
Flask handles routing.
JWT handles authentication.
SQLAlchemy manages database operations.
SQLite stores data.

# Q HOW IS SECURITY HANDLED?
I implemented JWT-based authentication.
Passwords are hashed using Werkzeug.
All private APIs are protected using jwt_required.
Users can access only their own data using user_id filtering.

# Q WHY DID YOU USE JWT?
JWT is stateless, scalable, and secure.
Server doesn’t need to store sessions.
Token is verified on every request.

# QWHAT CHALLENGES DID YOU FACE?
Initially, I faced issues with token authentication and user-task mapping.
I solved it by linking tasks with user_id and using get_jwt_identity().
I also handled CORS and error handling properly.

# Q HOW CAN YOU IMPROVE THIS PROJECT?
In future, I can:
        Use PostgreSQL instead of SQLite
        Add refresh tokens
        Implement role-based access
        Add pagination
        Add API documentation using Swagger
        Deploy on cloud

# ⭐ BONUS: ONE-LINE POWER STATEMENT --> end with this line
 This project helped me understand real-world backend development including authentication, security, and API design.


1️⃣ Read answer loudly
2️⃣ Record yourself
3️⃣ Improve confidence
4️⃣ Remove fear
Confidence = 50% selection 😄
