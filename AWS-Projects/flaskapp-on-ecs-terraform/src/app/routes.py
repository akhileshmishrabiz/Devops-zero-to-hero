from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Student, Attendance

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@bp.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form['student_id']
    status = request.form['status']
    new_attendance = Attendance(student_id=student_id, status=status)
    db.session.add(new_attendance)
    db.session.commit()
    return redirect(url_for('main.index'))