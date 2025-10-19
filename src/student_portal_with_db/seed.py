from school import db, Student, Course, app

with app.app_context():

    db.create_all()

    courses_data = ['Math', 'Physics', 'Chemistry', 'Biology', 'History']

    courses = []
    for name in courses_data:
        existing = Course.query.filter_by(name=name).first()
        if not existing:
            c = Course(name=name)
            db.session.add(c)
            courses.append(c)

    db.session.commit()

    students_data = [
        {'name': 'Ali', 'age': 20, 'course_names': ['Math', 'Physics']},
        {'name': 'Sara', 'age': 22, 'course_names': ['Biology', 'Chemistry']},
        {'name': 'Omar', 'age': 21, 'course_names': ['Math', 'History']}
    ]

    for sdata in students_data:
        existing = Student.query.filter_by(name=sdata['name']).first()
        if not existing:
            student = Student(name=sdata['name'], age=sdata['age'])
            for cname in sdata['course_names']:
                course = Course.query.filter_by(name=cname).first()
                if course:
                    student.courses.append(course)
            db.session.add(student)

    db.session.commit()

    print("Demo data added successfully!")
