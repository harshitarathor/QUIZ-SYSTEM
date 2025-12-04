import sqlite3
import os
from werkzeug.security import generate_password_hash

db_path = os.path.join(os.path.dirname(__file__), "quiz.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Questions table
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

# Admins table
c.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Results table
c.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score REAL NOT NULL,
    total_questions INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert default admin
default_username = "admin"
default_password = generate_password_hash("admin123")

c.execute("SELECT * FROM admins WHERE username=?", (default_username,))
if not c.fetchone():
    c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
              (default_username, default_password))

conn.commit()
conn.close()
print("Database created successfully with admin and results tables!")
