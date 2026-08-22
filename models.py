from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'employee' or 'admin'

    # Optional profile fields — fill in as needed
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    job_title = db.Column(db.String(100))
    salary = db.Column(db.Float, default=0.0)

    # Org info (header section)
    company = db.Column(db.String(100))
    department = db.Column(db.String(100))
    manager = db.Column(db.String(100))
    location = db.Column(db.String(100))

    # Resume — visible only to the employee themselves and Admin
    work_experience = db.Column(db.String(500))         # e.g. "2 years as Backend Developer at XYZ"
    previous_company = db.Column(db.String(150))
    skills = db.Column(db.String(500))                  # comma-separated

    # Private Info — sensitive, visible only to the employee themselves and Admin
    date_of_birth = db.Column(db.String(20))
    residing_address = db.Column(db.String(255))
    nationality = db.Column(db.String(100))
    personal_email = db.Column(db.String(120))
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(20))
    date_of_joining = db.Column(db.String(20))

    # Salary Info / Bank Details — most sensitive, visible only to the employee themselves and Admin
    bank_account_number = db.Column(db.String(50))
    bank_name = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(20))
    pan_no = db.Column(db.String(20))
    uan_no = db.Column(db.String(20))


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.String(20))
    check_out = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Present')  # Present/Absent/Half-day/Leave


class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # Paid/Sick/Unpaid
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Pending')  # Pending/Approved/Rejected
