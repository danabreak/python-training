from flask import Blueprint, render_template, request, redirect, url_for
from student_portal import db
from student_portal.models import Student, Course

students_bp = Blueprint('students', __name__, url_prefix='/students',
                        template_folder='../templates')

@students_bp.route('/', methods=['GET'])
def list_students():
    students = Student.query.all()
    return render_template('students/list.html', students=students)

@students_bp.route('/add', methods=['GET','POST'])
def add_student():
    courses = Course.query.all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age') or 0
        try:
            age = int(age)
        except ValueError:
            age = 0
        student = Student(name=name, age=age)
        db.session.add(student)
        # link courses
        for cid in request.form.getlist('courses'):
            c = Course.query.get(int(cid))
            if c:
                student.courses.append(c)
        db.session.commit()
        return redirect(url_for('students.list_students'))
    return render_template('students/add.html', courses=courses)
