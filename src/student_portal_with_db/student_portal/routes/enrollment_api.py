from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from student_portal import db
from student_portal.models import Student, Course, EnrollmentRequest

enrollment_api_bp = Blueprint("enrollment_api", __name__, url_prefix="/api/enrollment")

# ---------------------------
# 1) Create Enrollment Request
# ---------------------------
@enrollment_api_bp.route("", methods=["POST"])
@login_required
def create_enrollment_request():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")

    if not student_id or not course_id:
        return jsonify({"error": "student_id and course_id are required"}), 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({"error": "Invalid student_id or course_id"}), 404

    # Already enrolled?
    if course in student.courses:
        return jsonify({"status": "already_enrolled"}), 200

    # Existing pending request?
    pending = EnrollmentRequest.query.filter_by(
        student_id=student_id,
        course_id=course_id,
        status="pending"
    ).first()

    if pending:
        return jsonify({"status": "already_pending"}), 200

    req = EnrollmentRequest(
        student_id=student_id,
        course_id=course_id,
        status="pending"
    )
    db.session.add(req)
    db.session.commit()

    return jsonify({"status": "pending", "message": "Enrollment request created"}), 201


# ---------------------------
# 2) Check Enrollment Status
# ---------------------------
@enrollment_api_bp.route("/status", methods=["GET"])
@login_required
def check_status():
    student_id = request.args.get("student_id", type=int)
    course_id = request.args.get("course_id", type=int)

    if not student_id or not course_id:
        return jsonify({"error": "student_id and course_id are required"}), 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({"error": "Invalid student_id or course_id"}), 404

    # Enrolled?
    if course in student.courses:
        return jsonify({"status": "enrolled"}), 200

    # Check existing request
    req = EnrollmentRequest.query.filter_by(
        student_id=student_id,
        course_id=course_id
    ).first()

    if not req:
        return jsonify({"status": "not_requested"}), 200

    return jsonify({"status": req.status}), 200


# ---------------------------
# 3) Get All Courses of a Student
# ---------------------------
@enrollment_api_bp.route("/student/<int:student_id>", methods=["GET"])
@login_required
def student_courses(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    courses = [
        {"id": c.id, "name": c.name, "description": c.description}
        for c in student.courses
    ]

    return jsonify(courses), 200


# ---------------------------
# 4) Unenroll Student (Optional)
# ---------------------------
@enrollment_api_bp.route("/remove", methods=["DELETE"])
@login_required
def unenroll():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")

    if not student_id or not course_id:
        return jsonify({"error": "student_id and course_id are required"}), 400

    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({"error": "Invalid student_id or course_id"}), 404

    if course not in student.courses:
        return jsonify({"status": "not_enrolled"}), 200

    # Remove enrollment
    student.courses.remove(course)
    db.session.commit()

    return jsonify({"status": "removed"}), 200
