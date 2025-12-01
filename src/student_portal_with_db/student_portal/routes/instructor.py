from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from student_portal.models import Course
from ._decorators import role_required

instructor_bp = Blueprint(
    "instructor", __name__, url_prefix="/instructor", template_folder="../templates"
)

@instructor_bp.route("/courses")
@login_required
@role_required("instructor")
def my_courses():
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    return render_template("instructor/courses.html", courses=courses)



@instructor_bp.route("/courses/<int:cid>/roster")
@login_required
@role_required("instructor")
def course_roster(cid):
    course = Course.query.get_or_404(cid)
    if course.instructor_id != current_user.id:
        abort(403)
    return render_template("instructor/roster.html", course=course)
