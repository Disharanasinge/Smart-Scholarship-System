# Smart Scholarship Verification and Recommendation System

A Flask-based web application that helps students find verified scholarships while protecting them from fraud.

---

## Problem Statement

Every year, thousands of students in India fall victim to fake scholarship schemes. They either lose money or miss out on real opportunities because they cannot easily verify whether a scholarship is genuine. There is no single, trustworthy platform where students can search, verify, and apply for scholarships while also sharing their experiences with others.

---

## Objectives

- Build a platform where only verified scholarships are listed by admin
- Allow students to search and filter scholarships based on their needs
- Provide a trust score system so students know how reliable a scholarship is
- Allow students to report fraudulent scholarships
- Enable community interaction through ratings and comments
- Notify students about the status of their recommendations

---

## Features

### Student Features
- Register and login securely
- Search and filter scholarships by keyword or category
- View complete scholarship details including eligibility, documents, and process
- Rate scholarships (1–5 stars)
- Comment on scholarships to share experiences
- Report suspicious/fake scholarships with reasons
- Recommend new scholarships for admin review
- Receive notifications on recommendation status
- Update profile and password

### Admin Features
- Secure admin login
- Dashboard with platform statistics
- Add, edit, and delete scholarships
- Review and approve/reject student recommendations
- Investigate fraud reports and remove suspicious listings
- Receive notifications on new reports and recommendations

---

## Technologies Used

| Layer    | Technology            |
|----------|-----------------------|
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Backend  | Python, Flask         |
| Database | SQLite                |
| Security | Werkzeug (password hashing), Flask Sessions |
| Icons    | Font Awesome 6        |
| Fonts    | Google Fonts (Nunito) |

---

## Project Structure

```
SMART_SCHOLARSHIP/
│
├── app.py                        ← Main Flask application
├── database.db                   ← SQLite database (auto-created)
├── requirements.txt              ← Python dependencies
├── README.md                     ← This file
│
├── templates/
│   ├── index.html                ← Landing/Home page
│   ├── login.html                ← Login page
│   ├── register.html             ← Registration page
│   ├── student_home.html         ← Student scholarship listing
│   ├── scholarship_details.html  ← Scholarship detail view
│   ├── student_profile.html      ← Student profile management
│   ├── student_notifications.html← Student notifications
│   ├── recommend.html            ← Recommend a scholarship
│   ├── admin_dashboard.html      ← Admin overview
│   ├── admin_manage_scholarships.html ← Admin scholarship list
│   ├── admin_add_scholarship.html     ← Add scholarship form
│   ├── admin_edit_scholarship.html    ← Edit scholarship form
│   ├── admin_recommendations.html     ← Review student recommendations
│   ├── admin_fraud_reports.html       ← Review fraud reports
│   └── admin_notifications.html       ← Admin notifications
│
└── static/
    ├── style.css                 ← Custom styles
    └── script.js                 ← JavaScript (star rating, alerts)
```

---

## Installation Steps

### Step 1: Make sure Python is installed
```bash
python --version
```

### Step 2: Install Flask and Werkzeug
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
python app.py
```

### Step 4: Open in browser
```
http://127.0.0.1:5000
```

---

## Default Admin Credentials

```
Email:    admin@scholarship.com
Password: admin123
```

---

ADD DEBUG = FALSE BEFORE FINAL SUBMISSION
Current:
app.run(debug=True)
Before submission:
app.run(debug=False)

Why:
professional deployment practice
avoids exposing errors in viva
BUT while developing:
keep True.

---

## How to Use

### As a Student:
1. Go to the homepage and click **Register**
2. Create your account
3. Login and browse scholarships
4. Click **View Details** on any scholarship
5. Rate it, comment, or report it if suspicious
6. Use the **Recommend** page to suggest new scholarships

### As Admin:
1. Login with admin credentials
2. Use the dashboard to see platform statistics
3. Add new scholarships via **Add New Scholarship**
4. Review student recommendations and approve/reject them
5. Handle fraud reports — investigate and remove or keep scholarships

---

## Route Explanation

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage |
| `/register` | GET/POST | Student registration |
| `/login` | GET/POST | Login for all users |
| `/logout` | GET | Clear session and redirect |
| `/student/home` | GET | Student dashboard with search |
| `/scholarship/<id>` | GET | Scholarship detail page |
| `/rate/<id>` | POST | Submit star rating |
| `/comment/<id>` | POST | Post a comment |
| `/report/<id>` | POST | Submit fraud report |
| `/recommend` | GET/POST | Recommend a scholarship |
| `/profile` | GET/POST | View and edit profile |
| `/notifications` | GET | View student notifications |
| `/admin/dashboard` | GET | Admin overview |
| `/admin/scholarships` | GET | Admin scholarship list |
| `/admin/scholarship/add` | GET/POST | Add scholarship |
| `/admin/scholarship/edit/<id>` | GET/POST | Edit scholarship |
| `/admin/scholarship/delete/<id>` | POST | Delete scholarship |
| `/admin/recommendations` | GET | View recommendations |
| `/admin/recommendation/action/<id>/<action>` | GET | Approve/reject |
| `/admin/fraud-reports` | GET | View fraud reports |
| `/admin/fraud-report/action/<id>/<action>` | GET | Remove/keep scholarship |
| `/admin/notifications` | GET | Admin notifications |

---

## Database Tables

### users
Stores all user accounts (students and admin)

### scholarships
Stores all scholarship listings added by admin

### ratings
Stores student star ratings (1–5) for each scholarship

### comments
Stores student comments on scholarships

### fraud_reports
Stores reports submitted by students about suspicious scholarships

### recommendations
Stores scholarship suggestions submitted by students for admin review

### notifications
Stores messages sent to students or admin about system events

---

## Trust Score Logic

The trust score is calculated as:

```
score = (average_rating / 5) * 100
score = score - (pending_fraud_reports * 10)
score = clamp between 0 and 100
```

| Score Range | Label    | Meaning                        |
|-------------|----------|--------------------------------|
| 70–100      | Trusted  | High ratings, no/few reports   |
| 40–69       | Moderate | Average ratings or some reports|
| 0–39        | Risky    | Low ratings or many reports    |

---

## Future Enhancements

- Email notifications using Flask-Mail
- SMS alerts for application deadlines
- PDF export of scholarship details
- Advanced search with multiple filters
- Scholarship eligibility matching based on student profile
- Admin analytics dashboard with charts
- Mobile app using React Native or Flutter

---

## License

This project is created as a BCA Final Year Academic Project.
