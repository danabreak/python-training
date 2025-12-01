import os
import sqlite3
from flask import Flask, app, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


db = SQLAlchemy()
login_manager = LoginManager()          
login_manager.login_view = "auth.login" 
def create_app(config_object=None):
    app = Flask(__name__, template_folder='templates')

    # نرجع مستوى واحد للأعلى حتى نوصل لمجلد project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    instance_dir = os.path.join(project_root, "instance")
    os.makedirs(instance_dir, exist_ok=True)

    db_path = os.path.join(instance_dir, "school.db")

    load_dotenv(os.path.join(project_root, ".env"))

    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET", "dev-secret"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", f"sqlite:///{db_path}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    
    @app.errorhandler(404)
    def not_found(e):
     return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
     return render_template("errors/500.html"), 500
    


    if config_object:
        app.config.from_object(config_object)




    db.init_app(app)
    login_manager.init_app(app)         
    migrate = Migrate(app, db)  


 
    from .models import User, EnrollmentRequest, enrollments, Course, Student 
          
           
         
    @login_manager.user_loader        
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .routes.students import students_bp
    from .routes.students_api import students_api_bp
    from .routes.auth import auth_bp              
    from .routes.dashboard import dashboard_bp    
    from .routes.admin import admin_bp
    from .routes.instructor import instructor_bp
    from .routes.courses_api import courses_api_bp
    from .routes.courses import courses_bp
    from .routes.enrollment_api import enrollment_api_bp
    app.register_blueprint(enrollment_api_bp)

    app.register_blueprint(courses_bp)

    app.register_blueprint(students_bp)
    app.register_blueprint(students_api_bp)
    app.register_blueprint(auth_bp)              
    app.register_blueprint(dashboard_bp)          
    app.register_blueprint(courses_api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(instructor_bp)


    @app.cli.command("seed")
    def seed():
        """Reset & seed database with sample data."""
        from sqlalchemy import text

        print("🔄 Clearing existing data...")

        # امسح جدول الربط many-to-many أولاً
        db.session.execute(enrollments.delete())
        # امسح الجداول اللي فيها FK
        EnrollmentRequest.query.delete()
        Student.query.delete()
        Course.query.delete()
        User.query.delete()
        db.session.commit()

        print("✅ Tables cleared.")

        # ---------- 1) Create Admin ----------
        admin = User(
            username="admin",
            email="admin@test.com",
            role="admin",
            name="Site Admin"
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # ---------- 2) Create Instructors ----------
        instr1 = User(username="ali123",  name="Ali Ahmad",  role="instructor")
        instr2 = User(username="sara12",  name="Sara Omar",  role="instructor")
        instr3 = User(username="john01",  name="John Doe",   role="instructor")

        for ins in (instr1, instr2, instr3):
            ins.set_password("pass123")
            db.session.add(ins)

        # ---------- 3) Create Students (User + Student profile) ----------
        stu1_user = User(username="dana01",  email="dana@example.com",  role="student", name="Dana")
        stu2_user = User(username="ahmad77", email="ahmad@example.com", role="student", name="Ahmad")
        stu3_user = User(username="noor88",  email="noor@example.com",  role="student", name="Noor")
        stu4_user = User(username="lara22",  email="lara@example.com",  role="student", name="Lara")
        stu5_user = User(username="omar55",  email="omar@example.com",  role="student", name="Omar")

        students = [
            (stu1_user, "Dana", 22),
            (stu2_user, "Ahmad", 21),
            (stu3_user, "Noor",  23),
            (stu4_user, "Lara",  20),
            (stu5_user, "Omar",  24),
        ]

        for user_obj, name, age in students:
            user_obj.set_password("pass123")
            db.session.add(user_obj)
            # Student مرتبط بـ User
            s = Student(name=name, age=age, user=user_obj)
            db.session.add(s)

        db.session.commit()
        print("✅ Admin, instructors, and students created.")

        # نرجع نجيب الطلاب بعد الـ commit
        all_students = Student.query.order_by(Student.id).all()
        s1, s2, s3, s4, s5 = all_students  # 5 طلاب

        # ---------- 4) Create Courses ----------
        c1 = Course(name="Python Basics",        description="Introduction to Python.",      instructor=instr1)
        c2 = Course(name="Flask Web Dev",       description="Build web apps with Flask.",   instructor=instr1)
        c3 = Course(name="Databases 101",       description="Intro to SQL & design.",       instructor=instr2)
        c4 = Course(name="Algorithms & DS",     description="Core CS fundamentals.",        instructor=instr2)
        c5 = Course(name="Frontend Basics",     description="HTML, CSS, JS basics.",        instructor=instr3)
        c6 = Course(name="APIs and REST",       description="Building RESTful APIs.",       instructor=instr3)

        for c in (c1, c2, c3, c4, c5, c6):
            db.session.add(c)

        db.session.commit()
        print("✅ Courses created.")

        # ---------- 5) Enrollments (many-to-many) ----------
        # s1 و s2 ماخذين Python + Flask
        s1.courses.extend([c1, c2])
        s2.courses.extend([c1, c3])

        # s3 ماخد Databases + Algorithms
        s3.courses.extend([c3, c4])

        # s4 ماخدة Frontend
        s4.courses.append(c5)

        # s5 ماخد APIs فقط
        s5.courses.append(c6)

        db.session.commit()
        print("✅ Enrollments inserted.")

        # ---------- 6) Enrollment Requests ----------
        # s1 طالب يسجل في Algorithms (لسّا pending)
        req1 = EnrollmentRequest(student_id=s1.id, course_id=c4.id, status="pending")
        # s2 طلبه على Frontend مرفوض
        req2 = EnrollmentRequest(student_id=s2.id, course_id=c5.id, status="rejected")
        # s4 طلب APIs ولسّا pending
        req3 = EnrollmentRequest(student_id=s4.id, course_id=c6.id, status="pending")

        db.session.add_all([req1, req2, req3])
        db.session.commit()
        print("✅ Enrollment requests added.")

        print("\n🎉 Seeding done!")
        print("Admin login → username: admin , password: admin123")
        print("Example instructor → username: ali123 , password: pass123")
        print("Example student   → username: dana01 , password: pass123")



    @app.route('/')
    def home():
     return render_template('home_guest.html')

    return app
