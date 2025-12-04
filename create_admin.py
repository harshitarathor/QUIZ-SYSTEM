import sqlite3
import os
from werkzeug.security import generate_password_hash

# Path to database
db_path = os.path.join(os.path.dirname(__file__), "quiz.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# ================== QUESTIONS TABLE ==================
c.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT,
    option4 TEXT,
    answer TEXT NOT NULL
)
''')

# ================== ADMINS TABLE ==================
c.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# ================== RESULTS TABLE ==================
c.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score REAL NOT NULL,
    total_questions INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# ================== DEFAULT ADMIN ==================
default_username = "admin"
default_password = generate_password_hash("admin123")  # hashed password

# Insert admin only if it does not exist
c.execute("SELECT * FROM admins WHERE username=?", (default_username,))
if not c.fetchone():
    c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
              (default_username, default_password))
    print("Default admin created: username='admin', password='admin123'")
else:
    print("Admin already exists, skipping creation.")

# ================== COMMIT & CLOSE ==================
conn.commit()
conn.close()
print("Database created successfully!")
