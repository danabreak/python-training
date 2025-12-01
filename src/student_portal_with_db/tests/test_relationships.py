import pytest
from student_portal import create_app, db
from student_portal.models import Student, User, Course, EnrollmentRequest

def test_user_student_relation(app):
    with app.app_context():
        user = User(username="u1", role="student")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        student = Student(name="Dana", age=22, user=user)
        db.session.add(student)
        db.session.commit()

        # User له Student واحد
        assert user.student is student

        # Student إله User
        assert student.user is user


def test_student_courses(app):
    with app.app_context():
        user = User(username="st1", role="student")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        s = Student(name="Ali", age=20, user=user)
        c1 = Course(name="Python")
        c2 = Course(name="Flask")

        db.session.add_all([s, c1, c2])
        db.session.commit()

        # enroll
        s.courses.extend([c1, c2])
        db.session.commit()

        assert len(s.courses) == 2
        assert c1 in s.courses
        assert c2 in s.courses


def test_instructor_teaches_multiple_courses(app):
    with app.app_context():
        instr = User(username="inst1", role="instructor")
        instr.set_password("123")
        db.session.add(instr)
        db.session.commit()

        c1 = Course(name="DSA", instructor=instr)
        c2 = Course(name="APIs", instructor=instr)

        db.session.add_all([c1, c2])
        db.session.commit()

        assert instr.courses_taught.count() == 2
        assert c1 in instr.courses_taught
        assert c2 in instr.courses_taught


def test_enrollment_request(app):
    with app.app_context():
        user = User(username="st2", role="student")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        s = Student(name="Lara", age=19, user=user)
        c = Course(name="HTML Basics")

        db.session.add_all([s, c])
        db.session.commit()

        req = EnrollmentRequest(student=s, course=c, status="pending")
        db.session.add(req)
        db.session.commit()

        assert req.student is s
        assert req.course is c
        assert req.status == "pending"

        # الطالب عنده 1 request
        assert len(s.enrollment_requests) == 1
