from . import db

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
