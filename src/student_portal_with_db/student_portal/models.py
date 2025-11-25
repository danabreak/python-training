from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

enrollments = db.Table(
    'enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='pending_student')
    profile_pic = db.Column(db.String(255), nullable=True)

    student = db.relationship('Student', back_populates='user', uselist=False)
    courses_taught = db.relationship('Course', back_populates='instructor', lazy='dynamic')

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw) -> bool:
        return check_password_hash(self.password_hash, raw)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='student')

    courses = db.relationship('Course', secondary=enrollments, back_populates='students')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'courses': [c.name for c in self.courses],
            'profile_pic': self.user.profile_pic if self.user else None,
            'user_id': self.user_id
        }


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    instructor = db.relationship('User', back_populates='courses_taught', foreign_keys=[instructor_id])

    students = db.relationship('Student', secondary=enrollments, back_populates='courses')


class EnrollmentRequest(db.Model):
    __tablename__ = 'enrollment_request'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') 
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref='enrollment_requests')
    course = db.relationship('Course', backref='enrollment_requests')
