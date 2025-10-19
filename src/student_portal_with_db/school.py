from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'school.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    courses = db.relationship('Course', secondary=enrollments,
                              back_populates='students')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', secondary=enrollments,
                               back_populates='courses')



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('students.html', students=students)



@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    courses = Course.query.all() 
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        course_ids = request.form.getlist('courses')  
        student = Student(name=name, age=age)
        
        for cid in course_ids:
            course = Course.query.get(int(cid))
            if course:
                student.courses.append(course)

        db.session.add(student)
        db.session.commit()
        return redirect(url_for('list_students'))
    
    return render_template('add_student.html', courses=courses)


if __name__ == '__main__':
    app.run(debug=True)
