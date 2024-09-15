from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Course, Enrollment, Grade
from app.forms import RegistrationForm, LoginForm, CourseForm, GradeForm

bp = Blueprint('main', __name__)

@bp.route("/")
@bp.route("/index")
def index():
    return render_template('index.html')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check credentials.', 'danger')
    return render_template('login.html', form=form)

@bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == 'Admin':
        return render_template('admin_dashboard.html')
    elif current_user.role == 'Teacher':
        return render_template('teacher_dashboard.html')
    else:
        return render_template('student_dashboard.html')

@bp.route("/manage_courses", methods=['GET', 'POST'])
@login_required
def manage_courses():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data, teacher_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully', 'success')
        return redirect(url_for('main.manage_courses'))
    courses = Course.query.filter_by(teacher_id=current_user.id).all() if current_user.role == 'Teacher' else Course.query.all()
    return render_template('manage_courses.html', form=form, courses=courses)

@bp.route("/gradebook", methods=['GET', 'POST'])
@login_required
def gradebook():
    form = GradeForm()
    form.student_id.choices = [(u.id, u.username) for u in User.query.filter_by(role='Student').all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.all()]
    if form.validate_on_submit():
        enrollment = Enrollment.query.filter_by(student_id=form.student_id.data, course_id=form.course_id.data).first()
        if enrollment:
            grade = Grade(enrollment_id=enrollment.id, grade=form.grade.data)
            db.session.add(grade)
            db.session.commit()
            flash('Grade submitted successfully', 'success')
        else:
            flash('Student is not enrolled in the course', 'danger')
    return render_template('gradebook.html', form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
