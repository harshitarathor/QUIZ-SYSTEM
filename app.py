from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey123"

def get_db():
    conn = sqlite3.connect("quiz.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================== HOME PAGE ==================
@app.route("/")
def home():
    return render_template("home.html")

# ================== START QUIZ ==================
@app.route("/quiz")
def quiz():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()
    return render_template("quiz.html", questions=questions)

# ================== SUBMIT QUIZ ==================
@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()

    score = 0
    total = len(questions)
    details = []

    for q in questions:
        selected = request.form.get(str(q["id"]))
        is_correct = selected == q["answer"]
        if is_correct:
            score += 1
        details.append({
            "question": q["question"],
            "selected": selected,
            "answer": q["answer"],
            "is_correct": is_correct
        })

    username = request.form.get("username") or "Guest"

    cur.execute(
        "INSERT INTO results (username, score, total_questions) VALUES (?, ?, ?)",
        (username, score, total)
    )
    conn.commit()
    conn.close()

    percentage = round((score / total) * 100, 2) if total > 0 else 0

    return render_template("result.html",
                           score=percentage,
                           correct=score,
                           total=total,
                           details=details)

# ================== ADMIN LOGIN ==================
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admins WHERE username=?", (username,))
        admin = cur.fetchone()
        conn.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid Credentials")

    return render_template("admin_login.html")

# ================== ADMIN DASHBOARD ==================
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    cur.execute("SELECT * FROM results ORDER BY timestamp DESC")
    results = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html",
                           questions=questions,
                           results=results,
                           add_question_url=url_for("add_question_page"))

# ================== ADD QUESTION PAGE ==================
@app.route("/add_question_page")
def add_question_page():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    return render_template("add_question.html", edit=False)

# ================== ADD QUESTION ACTION ==================
@app.route("/add_question", methods=["POST"])
def add_question():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    q = request.form["question"]
    o1 = request.form["option1"]
    o2 = request.form["option2"]
    o3 = request.form["option3"]
    o4 = request.form["option4"]
    ans = request.form["answer"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)",
        (q, o1, o2, o3, o4, ans)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))

# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

# ================== RUN APP ==================
if __name__ == "__main__":
    app.run(debug=True)
