from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret-key")

DATABASE = "smart_scholarship.db"

#  DB HELPER

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'student',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        provider TEXT NOT NULL,
        description TEXT,
        eligibility TEXT,
        documents TEXT,
        process TEXT,
        deadline TEXT,
        amount TEXT,
        official_link TEXT,
        category TEXT,
        added_by INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        scholarship_id INTEGER,
        rating INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, scholarship_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        scholarship_id INTEGER,
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS fraud_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        scholarship_id INTEGER,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        provider TEXT,
        link TEXT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create default admin
    existing = c.execute("SELECT * FROM users WHERE email='admin@smartscholarship.com'").fetchone()
    if not existing:
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "changeme123")
        hashed = generate_password_hash(admin_password)
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                ("Admin", admin_email, hashed, "admin"))

    # Add sample scholarships
    count = c.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    if count == 0:
        samples = [
            ("National Merit Scholarship", "Ministry of Education", "A prestigious scholarship for meritorious students across India.", "10th and 12th pass with 80%+ marks. Annual family income below 1.5 LPA.", "Mark sheets, Income certificate, Aadhaar card, Bank passbook", "Apply online on NSP portal. Fill form, upload documents, submit.", "2024-11-30", "₹12,000/year", "https://scholarships.gov.in", "Merit-based"),
            ("Post-Matric SC/ST Scholarship", "Government of India", "Financial aid for SC/ST students pursuing post-matric education.", "SC/ST students with family income below 2.5 LPA.", "Caste certificate, Income certificate, Admission letter", "Register on NSP, fill details, upload required documents.", "2024-10-31", "₹15,000/year", "https://scholarships.gov.in", "SC/ST"),
            ("Pragati Scholarship for Girls", "AICTE", "Scholarship for girl students pursuing technical education.", "Girl students in 1st year of AICTE-approved institutions. Family income below 8 LPA.", "Admission letter, Income proof, Bank details", "Apply via AICTE portal with required documents.", "2024-12-15", "₹50,000/year", "https://www.aicte-india.org", "Girls"),
            ("Central Sector Scholarship", "UGC", "For students in top 20 percentile of Class 12 board exams.", "Students scoring in top 20% of their state board. Regular college student.", "Class 12 marksheet, College ID, Bank passbook", "Apply on NSP, verify through college.", "2024-11-15", "₹10,000/year", "https://scholarships.gov.in", "Merit-based"),
            ("Buddy4Study Foundation Grant", "Buddy4Study", "Private foundation grant for underprivileged but talented students.", "Students from low-income families with 60%+ academics.", "Income certificate, Marksheets, Essay on goals", "Online application with essay submission.", "2024-12-01", "₹25,000", "https://www.buddy4study.com", "Need-based"),
        ]
        for s in samples:
            c.execute("""INSERT INTO scholarships (name, provider, description, eligibility, documents, process, deadline, amount, official_link, category, added_by)
                         VALUES (?,?,?,?,?,?,?,?,?,?,1)""", s)

    conn.commit()
    conn.close()


#  HELPERS

def compute_trust_score(scholarship_id):
    conn = get_db()
    avg_rating = conn.execute(
        "SELECT AVG(rating) FROM ratings WHERE scholarship_id=?", (scholarship_id,)
    ).fetchone()[0] or 0

    report_count = conn.execute(
        "SELECT COUNT(*) FROM fraud_reports WHERE scholarship_id=? AND status='pending'",
        (scholarship_id,)
    ).fetchone()[0]
    conn.close()

    score = (avg_rating / 5.0) * 100
    score -= report_count * 10
    score = max(0, min(100, score))

    if score >= 70:
        label = "Trusted"
        color = "success"
    elif score >= 40:
        label = "Moderate"
        color = "warning"
    else:
        label = "Risky"
        color = "danger"

    return {"score": round(score, 1), "label": label, "color": color}

def add_notification(user_id, message):
    conn = get_db()
    conn.execute(
        "INSERT INTO notifications (user_id, message) VALUES (?,?)",
        (user_id, message)
    )
    conn.commit()
    conn.close()


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


#  PUBLIC ROUTES

@app.route("/")
def index():
    conn = get_db()
    featured = conn.execute(
        "SELECT * FROM scholarships ORDER BY created_at DESC LIMIT 4"
    ).fetchall()
    conn.close()
    return render_template("index.html", featured=featured)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?,?,?)",
                (name, email, hashed)
            )
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]
            session["user_id"] = user["id"]

            conn2 = get_db()
            unread = conn2.execute(
                "SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0", (user["id"],)
                ).fetchone()[0]
            session["unread_count"] = unread
            conn2.close()
            flash(f"Welcome back, {user['name']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("student_home"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

#  STUDENT ROUTES

@app.route("/student/home")
@login_required
def student_home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    conn = get_db()
    query = "SELECT * FROM scholarships WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE ? OR provider LIKE ? OR description LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY created_at DESC"
    scholarships = conn.execute(query, params).fetchall()

    categories = conn.execute("SELECT DISTINCT category FROM scholarships").fetchall()
    conn.close()

    scholarships_with_trust = []
    for s in scholarships:
        trust = compute_trust_score(s["id"])
        scholarships_with_trust.append({"data": s, "trust": trust})

    return render_template("student_home.html",
                           scholarships=scholarships_with_trust,
                           categories=categories,
                           search=search,
                           selected_category=category)


@app.route("/scholarship/<int:sid>")
@login_required
def scholarship_details(sid):
    conn = get_db()
    s = conn.execute("SELECT * FROM scholarships WHERE id=?", (sid,)).fetchone()
    if not s:
        flash("Scholarship not found.", "danger")
        return redirect(url_for("student_home"))

    comments = conn.execute("""
        SELECT c.*, u.name as user_name
        FROM comments c JOIN users u ON c.user_id = u.id
        WHERE c.scholarship_id=? ORDER BY c.created_at DESC
    """, (sid,)).fetchall()

    avg_rating = conn.execute(
        "SELECT AVG(rating) FROM ratings WHERE scholarship_id=?", (sid,)
    ).fetchone()[0] or 0

    user_rating = conn.execute(
        "SELECT rating FROM ratings WHERE user_id=? AND scholarship_id=?",
        (session["user_id"], sid)
    ).fetchone()

    user_reported = conn.execute(
        "SELECT id FROM fraud_reports WHERE user_id=? AND scholarship_id=?",
        (session["user_id"], sid)
    ).fetchone()

    conn.close()
    trust = compute_trust_score(sid)

    return render_template("scholarship_details.html",
                           s=s, comments=comments,
                           avg_rating=round(avg_rating, 1),
                           user_rating=user_rating,
                           user_reported=user_reported,
                           trust=trust)


@app.route("/rate/<int:sid>", methods=["POST"])
@login_required
def rate_scholarship(sid):
    rating = int(request.form.get("rating", 0))
    if 1 <= rating <= 5:
        conn = get_db()
        conn.execute("""
            INSERT INTO ratings (user_id, scholarship_id, rating) VALUES (?,?,?)
            ON CONFLICT(user_id, scholarship_id) DO UPDATE SET rating=excluded.rating
        """, (session["user_id"], sid, rating))
        conn.commit()
        conn.close()
        flash("Rating submitted!", "success")
    return redirect(url_for("scholarship_details", sid=sid))

@app.route("/comment/<int:sid>", methods=["POST"])
@login_required
def add_comment(sid):
    comment = request.form.get("comment", "").strip()
    if comment:
        conn = get_db()
        conn.execute(
            "INSERT INTO comments (user_id, scholarship_id, comment) VALUES (?,?,?)",
            (session["user_id"], sid, comment)
        )
        conn.commit()
        conn.close()
        flash("Comment posted!", "success")
    return redirect(url_for("scholarship_details", sid=sid))

@app.route("/report/<int:sid>", methods=["POST"])
@login_required
def report_scholarship(sid):
    reason = request.form.get("reason", "").strip()
    if reason:
        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM fraud_reports WHERE user_id=? AND scholarship_id=?",
            (session["user_id"], sid)
        ).fetchone()
        if existing:
            flash("You have already reported this scholarship.", "warning")
            conn.close()
        else:
            conn.execute(
                "INSERT INTO fraud_reports (user_id, scholarship_id, reason) VALUES (?,?,?)",
                (session["user_id"], sid, reason)
            )
            conn.commit()
            flash("Report submitted. Admin will review it.", "success")

            # Get scholarship name
            s = conn.execute(
                "SELECT name FROM scholarships WHERE id=?", (sid,)
            ).fetchone()

            # Get admin id
            admin = conn.execute(
                "SELECT id FROM users WHERE role='admin' LIMIT 1"
            ).fetchone()

            conn.close()

            # Send notification to admin
            if admin and s:
                add_notification(
                    admin["id"],
                    f"New fraud report received for '{s['name']}' by a student."
                )
    return redirect(url_for("scholarship_details", sid=sid))

@app.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        provider = request.form.get("provider", "").strip()
        link = request.form.get("link", "").strip()
        description = request.form.get("description", "").strip()

        if name and provider:
            conn = get_db()
            conn.execute(
                "INSERT INTO recommendations (user_id, name, provider, link, description) VALUES (?,?,?,?,?)",
                (session["user_id"], name, provider, link, description)
            )
            conn.commit()

            # Get admin id
            admin = conn.execute(
                "SELECT id FROM users WHERE role='admin' LIMIT 1"
            ).fetchone()

            conn.close()

            # Send notification to admin
            if admin:
                add_notification(
                    admin["id"],
                    f"New scholarship recommended by a student: '{name}'. Please review it."
                )

            flash("Recommendation submitted! Admin will review it.", "success")
            return redirect(url_for("student_home"))

    return render_template("recommend.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        if name:
            conn.execute("UPDATE users SET name=? WHERE id=?", (name, session["user_id"]))
            session["user_name"] = name
        if password:
            hashed = generate_password_hash(password)
            conn.execute("UPDATE users SET password=? WHERE id=?", (hashed, session["user_id"]))
        conn.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("profile"))

    conn.close()
    return render_template("student_profile.html", user=user)

@app.route("/notifications")
@login_required
def notifications():
    conn = get_db()
    notifs = conn.execute(
        "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (session["user_id"],))
    conn.commit()
    conn.close()
    return render_template("student_notifications.html", notifs=notifs)


#  ADMIN ROUTES
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    conn = get_db()
    total_scholarships = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0]
    pending_reports = conn.execute("SELECT COUNT(*) FROM fraud_reports WHERE status='pending'").fetchone()[0]
    pending_recs = conn.execute("SELECT COUNT(*) FROM recommendations WHERE status='pending'").fetchone()[0]
    recent_scholarships = conn.execute("SELECT * FROM scholarships ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    return render_template("admin_dashboard.html",
                           total_scholarships=total_scholarships,
                           total_students=total_students,
                           pending_reports=pending_reports,
                           pending_recs=pending_recs,
                           recent_scholarships=recent_scholarships)

@app.route("/admin/scholarships")
@admin_required
def admin_scholarships():
    conn = get_db()
    scholarships = conn.execute("SELECT * FROM scholarships ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin_manage_scholarships.html", scholarships=scholarships)


@app.route("/admin/scholarship/add", methods=["GET", "POST"])
@admin_required
def admin_add_scholarship():
    if request.method == "POST":
        fields = ["name", "provider", "description", "eligibility", "documents",
                  "process", "deadline", "amount", "official_link", "category"]
        data = [request.form.get(f, "").strip() for f in fields]
        conn = get_db()
        conn.execute("""
            INSERT INTO scholarships (name, provider, description, eligibility, documents,
            process, deadline, amount, official_link, category, added_by)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, data + [session["user_id"]])
        conn.commit()
        conn.close()
        flash("Scholarship added successfully!", "success")
        return redirect(url_for("admin_scholarships"))
    return render_template("admin_add_scholarship.html")

@app.route("/admin/scholarship/edit/<int:sid>", methods=["GET", "POST"])
@admin_required
def admin_edit_scholarship(sid):
    conn = get_db()
    s = conn.execute("SELECT * FROM scholarships WHERE id=?", (sid,)).fetchone()
    if request.method == "POST":
        fields = ["name", "provider", "description", "eligibility", "documents",
                  "process", "deadline", "amount", "official_link", "category"]
        data = [request.form.get(f, "").strip() for f in fields]
        conn.execute("""
            UPDATE scholarships SET name=?, provider=?, description=?, eligibility=?,
            documents=?, process=?, deadline=?, amount=?, official_link=?, category=?
            WHERE id=?
        """, data + [sid])
        conn.commit()
        conn.close()
        flash("Scholarship updated!", "success")
        return redirect(url_for("admin_scholarships"))
    conn.close()
    return render_template("admin_edit_scholarship.html", s=s)

@app.route("/admin/scholarship/delete/<int:sid>", methods=["POST"])
@admin_required
def admin_delete_scholarship(sid):
    conn = get_db()
    conn.execute("DELETE FROM scholarships WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    flash("Scholarship deleted.", "info")
    return redirect(url_for("admin_scholarships"))

@app.route("/admin/recommendations")
@admin_required
def admin_recommendations():
    conn = get_db()
    recs = conn.execute("""
        SELECT r.*, u.name as student_name FROM recommendations r
        JOIN users u ON r.user_id = u.id ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return render_template("admin_recommendations.html", recs=recs)

@app.route("/admin/recommendation/action/<int:rid>/<action>")
@admin_required
def recommendation_action(rid, action):
    conn = get_db()
    rec = conn.execute("SELECT * FROM recommendations WHERE id=?", (rid,)).fetchone()
    if rec:
        conn.execute("UPDATE recommendations SET status=? WHERE id=?", (action, rid))
        if action == "approved":
            conn.execute("""
                INSERT INTO scholarships (name, provider, description, official_link, added_by)
                VALUES (?,?,?,?,?)
            """, (rec["name"], rec["provider"], rec["description"], rec["link"], session["user_id"]))
            add_notification(rec["user_id"], f"Your recommendation '{rec['name']}' was approved and added!", conn)
        else:
            add_notification(rec["user_id"], f"Your recommendation '{rec['name']}' was reviewed but not approved at this time.", conn)
        conn.commit()
    conn.close()
    flash(f"Recommendation {action}.", "success")
    return redirect(url_for("admin_recommendations"))

@app.route("/admin/fraud-reports")
@admin_required
def admin_fraud_reports():
    conn = get_db()
    reports = conn.execute("""
        SELECT fr.*, u.name as reporter_name, s.name as scholarship_name
        FROM fraud_reports fr
        JOIN users u ON fr.user_id = u.id
        JOIN scholarships s ON fr.scholarship_id = s.id
        ORDER BY fr.created_at DESC
    """).fetchall()
    conn.close()
    return render_template("admin_fraud_reports.html", reports=reports)

@app.route("/admin/fraud-report/action/<int:rid>/<action>")
@admin_required
def fraud_report_action(rid, action):
    conn = get_db()
    report = conn.execute("SELECT * FROM fraud_reports WHERE id=?", (rid,)).fetchone()
    if report:
        conn.execute("UPDATE fraud_reports SET status=? WHERE id=?", (action, rid))
        if action == "removed":
            conn.execute("DELETE FROM scholarships WHERE id=?", (report["scholarship_id"],))
            flash("Scholarship removed due to fraud report.", "warning")
        else:
            flash("Report marked as reviewed.", "info")
        conn.commit()
    conn.close()
    return redirect(url_for("admin_fraud_reports"))

@app.route("/admin/notifications")
@admin_required
def admin_notifications():
    conn = get_db()
    notifs = conn.execute(
        "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (session["user_id"],))
    conn.commit()
    conn.close()
    return render_template("admin_notifications.html", notifs=notifs)

@app.route("/admin/users")
@admin_required
def manage_users():
    conn = get_db()
    users = conn.execute(
        "SELECT * FROM users WHERE role='student' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("manage_users.html", users=users)

@app.route("/admin/user/delete/<int:uid>", methods=["POST"])
@admin_required
def admin_delete_user(uid):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=? AND role='student'", (uid,))
    conn.commit()
    conn.close()
    flash("User deleted successfully.", "info")
    return redirect(url_for("manage_users"))


#  MAIN

if __name__ == "__main__":
    init_db()
    app.run(debug=False)
