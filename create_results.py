import sqlite3

conn = sqlite3.connect("quiz.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score REAL,
    total_questions INTEGER
)
""")

conn.commit()
conn.close()

print("Results table created!")
