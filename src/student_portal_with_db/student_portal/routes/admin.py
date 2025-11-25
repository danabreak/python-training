from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from student_portal import db
from student_portal.models import User, Course
from student_portal.models import EnrollmentRequest
from ._decorators import role_required
from student_portal.models import User, Student
from datetime import datetime
import string, random


admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates")



def generate_unique_username():
    """Generate a unique username: 3 letters + 4 digits, e.g., abc1234"""
    while True:
        letters = ''.join(random.choices(string.ascii_lowercase, k=3))
        digits = ''.join(random.choices(string.digits, k=4))
        username = letters + digits

        from student_portal.models import User
        if not User.query.filter_by(username=username).first():
            return username


def generate_random_password(length=10):
    """Generate a random password (not shown to admin)."""
    chars = string.ascii_letters + string.digits + "!@#$%&*?"
    return ''.join(random.choices(chars, k=length))


@admin_bp.route("/courses", methods=["GET"])
@login_required
@role_required("admin")
def courses_list():
    courses = Course.query.all()
    return render_template("admin/courses_list.html", courses=courses)




@admin_bp.route("/courses/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def course_new():
    instructors = User.query.filter_by(role="instructor").all()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        instr_id = request.form.get("instructor_id")  
        if not name:
            flash("Course name is required", "danger")
            return render_template("admin/course_form.html", instructors=instructors)

        instructor = None
        if instr_id:
            instructor = User.query.get(int(instr_id))
            if not instructor or instructor.role != "instructor":
                flash("Selected instructor is invalid", "danger")
                return render_template("admin/course_form.html", instructors=instructors)

        c = Course(name=name, instructor=instructor)
        db.session.add(c)
        db.session.commit()
        flash("Course created", "success")
        return redirect(url_for("admin.courses_list"))

    return render_template("admin/course_form.html", instructors=instructors)



@admin_bp.route("/courses/<int:cid>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def course_edit(cid):
    course = Course.query.get_or_404(cid)
    instructors = User.query.filter_by(role="instructor").all()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        instr_id = request.form.get("instructor_id")

        if not name:
            flash("Course name is required", "danger")
            return render_template("admin/course_form.html", course=course, instructors=instructors)

        instructor = None
        if instr_id:
            instructor = User.query.get(int(instr_id))
            if not instructor or instructor.role != "instructor":
                flash("Selected instructor is invalid", "danger")
                return render_template("admin/course_form.html", course=course, instructors=instructors)

        course.name = name
        course.instructor = instructor  
        db.session.commit()
        flash("Course updated", "success")
        return redirect(url_for("admin.courses_list"))

    return render_template("admin/course_form.html", course=course, instructors=instructors)





@admin_bp.route("/pending-students")
@login_required
@role_required("admin")
def pending_students():
    pending = User.query.filter_by(role="pending_student").all()
    return render_template("admin/pending_students.html", pending=pending)


@admin_bp.route("/approve-student/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def approve_student(user_id):
    user = User.query.get_or_404(user_id)

    if user.role != "pending_student":
        flash("This user is not pending student.", "danger")
        return redirect(url_for("admin.pending_students"))

    user.role = "student"

    new_student = Student(
        name=user.username,   
        age=0,                 
        date_created=datetime.utcnow()
    )

    db.session.add(new_student)
    db.session.commit()

    flash(f"Student '{user.username}' approved successfully.", "success")
    return redirect(url_for("admin.pending_students"))


@admin_bp.route("/reject-student/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def reject_student(user_id):
    user = User.query.get_or_404(user_id)

    if user.role != "pending_student":
        flash("Cannot reject this user.", "danger")
        return redirect(url_for("admin.pending_students"))

    user.role = "rejected"
    db.session.commit()

    flash(f"Student '{user.username}' rejected.", "info")
    return redirect(url_for("admin.pending_students"))
@admin_bp.route("/students/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_student():
    credentials = None
    hide_form = False

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        age = request.form.get("age")
        email = (request.form.get("email") or "").strip()

        if not name:
            flash("Student name is required.", "danger")
            return redirect(url_for("admin.add_student"))

        if not email:
            flash("Email is required.", "danger")
            return redirect(url_for("admin.add_student"))

        try:
            age = int(age)
        except:
            flash("Age must be a number.", "danger")
            return redirect(url_for("admin.add_student"))

        username = generate_unique_username()

        password_plain = generate_random_password()

        user = User(
            username=username,
            email=email,
            role="student"
        )
        user.set_password(password_plain)

        db.session.add(user)
        db.session.commit()

        student = Student(
            name=name,
            age=age,
            user_id=user.id
        )

        db.session.add(student)
        db.session.commit()

        credentials = {
            "name": name,
            "username": username,
            "password": password_plain,
            "email": email,
        }

        hide_form = True

    return render_template(
        "admin/add_student.html",
        credentials=credentials,
        hide_form=hide_form
    )



@admin_bp.route("/students")
@login_required
@role_required("admin")
def students_list():
    students = Student.query.all()
    return render_template("admin/students_list.html", students=students)



@admin_bp.route("/instructors")
@login_required
@role_required("admin")
def instructors_list():
    instructors = User.query.filter_by(role="instructor").all()
    return render_template("admin/instructors_list.html", instructors=instructors)

@admin_bp.route("/instructors/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_instructor():
    credentials = None
    hide_form = False

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()

        if not name:
            flash("Instructor name is required.", "danger")
            return redirect(url_for("admin.add_instructor"))

        username = generate_unique_username()

        password_plain = generate_random_password()

        user = User(
            username=username,
            name=name,
            role="instructor"
            )

        user.set_password(password_plain)

        db.session.add(user)
        db.session.commit()

        credentials = {
            "name": name,
            "username": username,
            "password": password_plain,
        }

        hide_form = True

    return render_template(
        "admin/add_instructor.html",
        credentials=credentials,
        hide_form=hide_form
    )



@admin_bp.route("/students/delete/<int:student_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    user = student.user

    student.courses.clear()

    for req in student.enrollment_requests:
        db.session.delete(req)

    db.session.delete(student)

    if user:
        db.session.delete(user)

    db.session.commit()
    flash("Student deleted successfully.", "success")

    return redirect(url_for("admin.students_list"))



@admin_bp.route("/instructors/delete/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_instructor(user_id):
    instructor = User.query.get_or_404(user_id)

    if instructor.role != "instructor":
        flash("Invalid instructor account.", "danger")
        return redirect(url_for("admin.instructors_list"))

 
    for course in instructor.courses_taught:
        course.instructor_id = None

    db.session.delete(instructor)
    db.session.commit()

    flash("Instructor deleted successfully.", "success")
    return redirect(url_for("admin.instructors_list"))



@admin_bp.route("/pending-enrollments")
@login_required
@role_required("admin")
def pending_enrollments():
    requests_list = EnrollmentRequest.query.filter_by(status="pending").all()
    return render_template("admin/pending_enrollments.html", requests=requests_list)



@admin_bp.route("/approve-enrollment/<int:request_id>", methods=["POST"])
@login_required
@role_required("admin")
def approve_enrollment(request_id):
    req = EnrollmentRequest.query.get_or_404(request_id)

    if req.status != "pending":
        flash("This request is already processed.", "warning")
        return redirect(url_for("admin.pending_enrollments"))

    if req.student not in req.course.students:
        req.course.students.append(req.student)

    req.status = "approved"
    db.session.commit()

    flash(f"Enrollment approved: {req.student.name} → {req.course.name}", "success")
    return redirect(url_for("admin.pending_enrollments"))


@admin_bp.route("/reject-enrollment/<int:request_id>", methods=["POST"])
@login_required
@role_required("admin")
def reject_enrollment(request_id):
    req = EnrollmentRequest.query.get_or_404(request_id)

    if req.status != "pending":
        flash("This request is already processed.", "warning")
        return redirect(url_for("admin.pending_enrollments"))

    req.status = "rejected"
    db.session.commit()

    flash(f"Enrollment rejected for student {req.student.name}.", "info")
    return redirect(url_for("admin.pending_enrollments"))
