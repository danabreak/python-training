from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from student_portal import db
from student_portal.models import Course
from sqlalchemy.exc import SQLAlchemyError

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/<int:cid>")
@login_required
def course_details(cid):
    course = Course.query.get_or_404(cid)
    students = course.students

    is_admin = (current_user.role == "admin")
    is_instructor = (current_user.role == "instructor" and course.instructor_id == current_user.id)

    is_student = (current_user.role == "student")

    return render_template(
        "courses/details.html",
        course=course,
        students=students,
        is_admin=is_admin,
        is_instructor=is_instructor,
        is_student=is_student
    )



