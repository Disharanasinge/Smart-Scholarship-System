# SMART SCHOLARSHIP VERIFICATION AND RECOMMENDATION SYSTEM
## Complete Project Documentation

### BCA Final Year Project | 2024–25

---

## ABSTRACT

The Smart Scholarship Verification and Recommendation System is a web-based application developed using Python (Flask framework) and SQLite database. The main purpose of this project is to help students find genuine, verified scholarships and protect them from online scholarship fraud. The system provides a student-friendly interface where students can search, filter, rate, comment on, and report scholarships. Admin manages all scholarship data and ensures only verified information is published on the platform. A built-in trust score system helps students evaluate the reliability of each scholarship at a glance.

---

## INTRODUCTION

Education is one of the most important investments a person can make. However, not every student can afford the full cost of higher education. Scholarships play a vital role in helping students financially. But finding the right scholarship and verifying whether it is real or fake has become a major challenge for students.

In India, many students lose money and personal data to fake scholarship websites. These websites look professional but are designed to collect fees or personal information. Students who come from rural or low-income backgrounds are the most vulnerable group.

This project addresses this problem by creating a centralized, verified, and community-driven scholarship platform.

---

## PROBLEM STATEMENT

Students searching for scholarships online face several problems:

1. **Too many results, no verification** — Search engines show hundreds of results with no way to verify which ones are real.
2. **Duplicate information** — The same scholarship appears on multiple third-party websites with different details.
3. **Fraud websites** — Fake scholarship sites collect personal data or demand fees.
4. **Lack of community feedback** — No platform allows students to share their experience about scholarships.
5. **No centralized database** — Students have to visit multiple government and private websites.

---

## OBJECTIVES

1. Build a Flask web application with student and admin login functionality
2. Allow admin to add, edit, and delete only verified scholarship listings
3. Provide students with search and filter options for finding scholarships
4. Implement a trust score system based on ratings and fraud reports
5. Allow students to rate and comment on scholarships
6. Let students report suspicious scholarships to admin
7. Allow students to recommend scholarships for admin review
8. Send notifications to students and admin for important events

---

## SCOPE OF THE PROJECT

**Included:**
- Student registration, login, and profile management
- Admin scholarship management (CRUD)
- Trust score calculation and display
- Community features: ratings, comments, fraud reports, recommendations
- Notification system

**Not included in current version:**
- Payment gateway integration
- Scholarship application tracking
- Email or SMS notifications
- Mobile application

---

## MODULES DESCRIPTION

### Module 1: User Authentication
This module handles registration and login for both students and admin. Passwords are stored as hashes using Werkzeug's `generate_password_hash` function. Flask sessions are used to keep users logged in between page requests.

**Key functions:** `register()`, `login()`, `logout()`

---

### Module 2: Scholarship Management (Admin)
Only the admin can add, edit, or delete scholarships. This ensures that no unverified information is published. The admin fills in all details like name, provider, eligibility, documents required, deadline, and amount.

**Key functions:** `admin_add_scholarship()`, `admin_edit_scholarship()`, `admin_delete_scholarship()`

---

### Module 3: Scholarship Discovery (Student)
Students can search and filter scholarships by keyword or category. Results are displayed as cards showing the name, provider, deadline, amount, and trust score.

**Key functions:** `student_home()`, `scholarship_details()`

---

### Module 4: Trust Score System
The trust score is calculated from the average student rating and the number of pending fraud reports. It is displayed on every scholarship card and detail page with labels: Trusted, Moderate, or Risky.

**Formula:** `score = (avg_rating / 5 * 100) - (fraud_report_count * 10)`

---

### Module 5: Community Features
Students can rate scholarships (1–5 stars), post comments to share experiences, and report fraud with reasons. This makes the platform community-driven and self-improving.

**Key functions:** `rate_scholarship()`, `add_comment()`, `report_scholarship()`

---

### Module 6: Recommendation System
Students can suggest scholarships they know about. Admin reviews the suggestion and either approves (adding it to the database) or rejects it. The student receives a notification either way.

**Key functions:** `recommend()`, `recommendation_action()`

---

### Module 7: Notification System
The notification system sends messages to students (about their recommendations) and to admin (about new fraud reports or recommendations). Notifications are stored in the database and shown on the notifications page.

**Key function:** `add_notification()`

---

## ADVANTAGES

1. **Verified information only** — Admin controls what is published, reducing fraud
2. **Community-driven trust** — Ratings and comments from real students
3. **Simple and clean UI** — Easy to use even for non-technical students
4. **Fraud detection** — Students can report suspicious scholarships
5. **Fast search** — Keyword and category filters make discovery easy
6. **Free platform** — No registration fees, no charges

---

## LIMITATIONS

1. The trust score is simple and does not use AI or machine learning
2. No email notifications — only in-app notifications
3. No automated verification of scholarship links
4. Admin has to manually add each scholarship
5. No mobile application currently

---

## FUTURE SCOPE

1. Integrate email alerts using Flask-Mail for deadline reminders
2. Add an AI-based recommendation engine that suggests scholarships based on student profile
3. Build a mobile app with React Native or Flutter
4. Add PDF export for scholarship details
5. Integrate Google Login for easier registration
6. Add a chatbot to answer student questions about scholarships

---

## CONCLUSION

The Smart Scholarship Verification and Recommendation System successfully solves a real and important problem faced by students in India. By creating a single trusted platform where only verified scholarships are listed, and where students can rate, comment, and report, the system empowers students to make informed decisions. The project demonstrates practical use of Flask, SQLite, HTML/CSS/Bootstrap, and Python — making it a well-rounded and complete final year project.

---

---

# VIVA QUESTIONS AND ANSWERS

---

**Q1. What is Flask and why did you use it?**

Flask is a lightweight Python web framework. I chose Flask because it is simple to learn, requires very little code to get started, and is perfect for small to medium projects like this. Unlike Django, Flask does not force a specific project structure, so I could organize the code the way I wanted.

---

**Q2. What is the difference between GET and POST methods?**

GET is used to retrieve data from the server. For example, loading a page. POST is used to send data to the server. For example, submitting a login form. GET requests show data in the URL; POST requests do not, which is why we use POST for forms involving sensitive data like passwords.

---

**Q3. How does login work in your project?**

When a student fills the login form and submits, the server checks the email in the database. If found, it uses `check_password_hash()` to verify the password. If correct, the user's ID, name, and role are stored in the Flask session. The session is like a temporary memory that keeps the user "logged in" across pages until they logout or the session expires.

---

**Q4. What is password hashing and why is it important?**

Password hashing means converting the password into a scrambled string using a mathematical function. Even if someone reads the database, they cannot get the original password. I used `generate_password_hash()` from Werkzeug to hash passwords before saving, and `check_password_hash()` to verify them during login.

---

**Q5. What is SQLite and why did you use it?**

SQLite is a simple, file-based database. It does not require a separate server to run — it stores everything in a single `.db` file. This makes it perfect for student projects and development work. The database file `database.db` is created automatically when the app starts.

---

**Q6. What is a session in Flask?**

A session is a way to store information about a user between requests. In Flask, when a user logs in, I store their `user_id`, `user_name`, and `role` in the session. This data is available on all pages until the user logs out. Sessions are secured using a `secret_key`.

---

**Q7. How does your trust score work?**

The trust score is calculated using:
- Average rating of the scholarship (out of 5 stars)
- Number of pending fraud reports

Formula: `score = (avg_rating / 5 * 100) - (fraud_reports * 10)`

A score of 70+ is Trusted, 40–69 is Moderate, and below 40 is Risky. The score is recalculated every time the scholarship detail page is loaded.

---

**Q8. What is CRUD and how did you implement it?**

CRUD stands for Create, Read, Update, Delete — the four basic database operations.

- **Create:** Admin adds a scholarship (`INSERT INTO scholarships`)
- **Read:** Students view scholarships (`SELECT * FROM scholarships`)
- **Update:** Admin edits a scholarship (`UPDATE scholarships SET ... WHERE id=?`)
- **Delete:** Admin deletes a scholarship (`DELETE FROM scholarships WHERE id=?`)

---

**Q9. How did you prevent SQL injection?**

I used parameterized queries (prepared statements). Instead of putting user input directly into the SQL string, I used `?` as a placeholder and passed the actual values as a separate list. This prevents attackers from injecting malicious SQL code.

Example:
```python
conn.execute("SELECT * FROM users WHERE email=?", (email,))
```

---

**Q10. How does the admin-student role separation work?**

The `users` table has a `role` column. Students have `role = 'student'` and admin has `role = 'admin'`. After login, the role is stored in the session. I created two decorator functions — `login_required` and `admin_required` — that check the session before allowing access to protected pages. If a student tries to access an admin page, they are redirected.

---

**Q11. What is `@login_required` decorator?**

A decorator is a function that wraps another function to add extra behavior. My `login_required` decorator checks if `user_id` is in the session. If not, it redirects to the login page. This protects all student pages from being accessed without logging in.

---

**Q12. How does the recommendation system work?**

A student fills a form with the scholarship name, provider, link, and description. This data is saved in the `recommendations` table with status `pending`. Admin receives a notification. Admin can then approve (which adds it to the scholarships table) or reject it. In both cases, the student receives a notification.

---

**Q13. What is the purpose of `row_factory = sqlite3.Row`?**

By default, SQLite returns data as plain tuples. Setting `conn.row_factory = sqlite3.Row` makes each row behave like a dictionary, so I can access columns by name like `user['email']` instead of `user[1]`. This makes the code much more readable.

---

**Q14. Why did you use Bootstrap?**

Bootstrap is a CSS framework that provides ready-made components like cards, tables, buttons, and a responsive grid system. It saved me a lot of time on the frontend design. The website automatically adjusts to look good on both desktop and mobile screens without writing extra CSS media queries.

---

**Q15. What tables does your database have and what do they store?**

| Table | Stores |
|-------|--------|
| users | Student and admin accounts |
| scholarships | Scholarship listings |
| ratings | Star ratings given by students |
| comments | Student comments on scholarships |
| fraud_reports | Reports about suspicious scholarships |
| recommendations | Scholarships suggested by students |
| notifications | Messages for students and admin |

---

**Q16. How does Flask handle form data?**

Flask uses `request.form.get('field_name')` to access data submitted via an HTML form with `method="POST"`. For GET requests with URL parameters (like search queries), it uses `request.args.get('param_name')`.

---

**Q17. What is `url_for()` in Flask templates?**

`url_for()` generates the URL for a given route/function name. Instead of hardcoding URLs like `/student/home`, I use `url_for('student_home')`. This is better because if I change the URL in `app.py`, the templates automatically use the new URL without any changes.

---

**Q18. How does the fraud report system protect students?**

When a student submits a fraud report with a reason, it is saved in the `fraud_reports` table with status `pending`. This also increases the scholarship's risk score. Admin is notified and can investigate. Admin can either remove the scholarship permanently or mark it as reviewed and keep it. The student who reported cannot report the same scholarship twice.

---

**Q19. What security measures did you implement?**

1. Password hashing with Werkzeug
2. Flask sessions with a secret key
3. Role-based access control (student vs admin)
4. Parameterized SQL queries (prevent SQL injection)
5. Input validation before saving to database
6. One-report-per-user restriction on fraud reports

---

**Q20. What would you improve if you had more time?**

I would add email notifications for deadlines, an AI recommendation engine that matches scholarships to a student's profile, a proper mobile app, and an admin analytics dashboard with graphs showing ratings, reports over time, and most popular categories.

---

*End of Documentation*
