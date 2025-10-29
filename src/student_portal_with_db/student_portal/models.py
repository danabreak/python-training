from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    courses = db.relationship('Course', secondary=enrollments, back_populates='students')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'courses': [c.name for c in self.courses] 
        }


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', secondary=enrollments, back_populates='courses')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw) -> bool:
        return check_password_hash(self.password_hash, raw)