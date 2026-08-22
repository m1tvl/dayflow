from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from models import db, User, Attendance, Leave

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayflow.db'
db.init_app(app)

# Only people who know this code can register as Admin/HR.
# Change this before your demo — share it only with your team's designated admin(s).
ADMIN_SECRET_CODE = 'DAYFLOW-ADMIN-2026'

with app.app_context():
    db.create_all()


def login_required(role=None):
    """Simple decorator factory to check session + optional role."""
    def wrapper(fn):
        from functools import wraps

        @wraps(fn)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return "Unauthorized", 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form['employee_id']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # 'employee' or 'admin'

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        # Gate admin signups behind a secret code known only to authorized people
        if role == 'admin':
            admin_code = request.form.get('admin_code', '')
            if admin_code != ADMIN_SECRET_CODE:
                flash('Invalid admin code. Admin accounts require authorization.')
                return redirect(url_for('signup'))

        user = User(
            name=name,
            employee_id=employee_id,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            job_title=request.form.get('job_title', ''),
            phone=request.form.get('phone', ''),
            company=request.form.get('company', ''),
            department=request.form.get('department', ''),
            manager=request.form.get('manager', ''),
            location=request.form.get('location', ''),
            work_experience=request.form.get('work_experience', ''),
            previous_company=request.form.get('previous_company', ''),
            skills=request.form.get('skills', ''),
            date_of_birth=request.form.get('date_of_birth', ''),
            residing_address=request.form.get('residing_address', ''),
            nationality=request.form.get('nationality', ''),
            personal_email=request.form.get('personal_email', ''),
            gender=request.form.get('gender', ''),
            marital_status=request.form.get('marital_status', ''),
            date_of_joining=request.form.get('date_of_joining', ''),
            bank_account_number=request.form.get('bank_account_number', ''),
            bank_name=request.form.get('bank_name', ''),
            ifsc_code=request.form.get('ifsc_code', ''),
            pan_no=request.form.get('pan_no', ''),
            uan_no=request.form.get('uan_no', '')
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('employee_dashboard'))

        flash('Invalid credentials')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- Employee routes ----------

@app.route('/employee/dashboard')
@login_required(role='employee')
def employee_dashboard():
    user = User.query.get(session['user_id'])
    return render_template('employee_dashboard.html', user=user)


@app.route('/employee/attendance', methods=['GET', 'POST'])
@login_required(role='employee')
def employee_attendance():
    user_id = session['user_id']
    today = date.today()
    record = Attendance.query.filter_by(user_id=user_id, date=today).first()

    if request.method == 'POST':
        action = request.form['action']
        if action == 'check_in' and not record:
            record = Attendance(user_id=user_id, date=today,
                                 check_in=datetime.now().strftime('%H:%M:%S'),
                                 status='Present')
            db.session.add(record)
            db.session.commit()
        elif action == 'check_out' and record and not record.check_out:
            record.check_out = datetime.now().strftime('%H:%M:%S')
            db.session.commit()
        return redirect(url_for('employee_attendance'))

    history = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.date.desc()).all()
    return render_template('attendance.html', record=record, history=history)


@app.route('/employee/leave', methods=['GET', 'POST'])
@login_required(role='employee')
def employee_leave():
    user_id = session['user_id']

    if request.method == 'POST':
        leave = Leave(
            user_id=user_id,
            leave_type=request.form['leave_type'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            remarks=request.form.get('remarks', ''),
            status='Pending'
        )
        db.session.add(leave)
        db.session.commit()
        return redirect(url_for('employee_leave'))

    leaves = Leave.query.filter_by(user_id=user_id).order_by(Leave.id.desc()).all()
    return render_template('leave.html', leaves=leaves)


@app.route('/employee/profile')
@login_required(role='employee')
def employee_profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', employee=user, is_self=True)


@app.route('/employee/change-password', methods=['POST'])
@login_required(role='employee')
def change_password():
    user = User.query.get(session['user_id'])
    current = request.form.get('current_password', '')
    new = request.form.get('new_password', '')

    if not check_password_hash(user.password_hash, current):
        flash('Current password is incorrect.')
    elif len(new) < 6:
        flash('New password must be at least 6 characters.')
    else:
        user.password_hash = generate_password_hash(new)
        db.session.commit()
        flash('Password updated successfully.')

    return redirect(url_for('employee_profile'))


# ---------- Admin routes ----------

@app.route('/admin/dashboard')
@login_required(role='admin')
def admin_dashboard():
    employees = User.query.filter_by(role='employee').all()
    pending_leaves = Leave.query.filter_by(status='Pending').count()
    return render_template('admin_dashboard.html', employees=employees, pending_leaves=pending_leaves)


@app.route('/admin/leaves', methods=['GET', 'POST'])
@login_required(role='admin')
def admin_leaves():
    if request.method == 'POST':
        leave_id = request.form['leave_id']
        action = request.form['action']
        leave = Leave.query.get(leave_id)
        leave.status = 'Approved' if action == 'approve' else 'Rejected'
        db.session.commit()
        return redirect(url_for('admin_leaves'))

    leaves = Leave.query.order_by(Leave.id.desc()).all()
    return render_template('admin_leaves.html', leaves=leaves)


@app.route('/admin/attendance')
@login_required(role='admin')
def admin_attendance():
    records = Attendance.query.order_by(Attendance.date.desc()).all()
    return render_template('admin_attendance.html', records=records)


@app.route('/admin/employee/<int:emp_id>')
@login_required(role='admin')
def admin_view_employee(emp_id):
    # Profile info is sensitive — only Admin can view another user's here.
    employee = User.query.get_or_404(emp_id)
    return render_template('profile.html', employee=employee, is_self=False)


if __name__ == '__main__':
    app.run(debug=True)
