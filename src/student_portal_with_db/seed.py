from student_portal import create_app, db
from student_portal.models import Course, Student

app = create_app()

with app.app_context():
    db.create_all()

    names = ['Math','Physics','Chemistry','Biology','History']
    for n in names:
        if not Course.query.filter_by(name=n).first():
            db.session.add(Course(name=n))
    db.session.commit()

    if not Student.query.filter_by(name='Ali').first():
        s = Student(name='Ali', age=20)
        s.courses.append(Course.query.filter_by(name='Math').first())
        db.session.add(s)
        db.session.commit()

    print("Seed completed")
