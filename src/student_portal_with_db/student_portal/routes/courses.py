from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from student_portal import db
from student_portal.models import Course
from sqlalchemy.exc import SQLAlchemyError

courses_api_bp = Blueprint("courses_api", __name__, url_prefix="/api/courses")

# --------- LIST ---------
@courses_api_bp.route("", methods=["GET"])
def list_courses():
    try:
        courses = Course.query.all()
        return jsonify([{"id": c.id, "name": c.name} for c in courses]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

# --------- CREATE ---------
@courses_api_bp.route("", methods=["POST"])
def create_course():
    try:
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400

        # optional: منع التكرار
        exists = Course.query.filter_by(name=name).first()
        if exists:
            return jsonify({"error": "Course already exists"}), 400

        c = Course(name=name)
        db.session.add(c)
        db.session.commit()
        return jsonify({"id": c.id, "name": c.name}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

# --------- UPDATE ---------
@courses_api_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    try:
        c = Course.query.get(course_id)
        if not c:
            return jsonify({"error": "Not found"}), 404

        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400

        c.name = name
        db.session.commit()
        return jsonify({"id": c.id, "name": c.name}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

# --------- DELETE ---------
@courses_api_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        c = Course.query.get(course_id)
        if not c:
            return jsonify({"error": "Not found"}), 404

        db.session.delete(c)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500




@courses_api_bp.route("/courses/<int:cid>")
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



