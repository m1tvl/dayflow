# Dayflow — Human Resource Management System

Every workday, perfectly aligned.

A lightweight HRMS built for [Hackathon Name] that digitizes core HR operations: authentication, role-based dashboards, attendance tracking, leave management, and payroll visibility.

## Features Implemented

- **Authentication**: Sign up / sign in with hashed passwords, role selection (Employee / Admin)
- **Role-based dashboards**: Separate views for Employees and Admin/HR
- **Attendance tracking**: Daily check-in/check-out with history log
- **Leave management**: Employees apply for Paid/Sick/Unpaid leave; Admin approves/rejects
- **Employee profile**: View personal & job details; salary shown as read-only
- **Admin controls**: View all employees, all attendance records, manage all leave requests

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite via SQLAlchemy ORM
- **Frontend**: HTML/CSS (Jinja2 templates)

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
dayflow-hrms/
├── app.py              # Routes and app logic
├── models.py           # Database models (User, Attendance, Leave)
├── templates/           # Jinja2 HTML templates
├── static/css/          # Stylesheet
└── requirements.txt
```

## Future Enhancements

- Email verification on sign-up
- Payroll editing & salary slip generation (PDF export)
- Analytics & reports dashboard
- Email/notification alerts
- Password reset flow

## Team

[Add your team member names here]
