from flask import Blueprint, jsonify, request, abort
from student_portal.models import Student, db, Course, User
from sqlalchemy.exc import SQLAlchemyError


students_api_bp = Blueprint('students_api', __name__, url_prefix='/api/students')


# ------------------ GET ALL STUDENTS ------------------
@students_api_bp.route('', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

# ------------------ ADD STUDENT ------------------
@students_api_bp.route('', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing 'name' field"}), 400

        age = data.get('age', 0)
        if not isinstance(age, int) or age < 0:
            return jsonify({"error": "'age' must be a positive integer"}), 400

        # ----------------------------
        # Create user automatically
        # ----------------------------
        username = data['name'].lower().replace(" ", "") + "01"
        user = User(username=username, role="student")
        user.set_password("pass123")

        student = Student(
            name=data['name'],
            age=age,
            user=user
        )

        # ----------------------------
        # Courses
        # ----------------------------
        course_names = data.get('courses', [])
        if not isinstance(course_names, list):
            return jsonify({"error": "'courses' must be a list of course names"}), 400

        for cname in course_names:
            course = Course.query.filter_by(name=cname).first()
            if not course:
                course = Course(name=cname)
                db.session.add(course)
            student.courses.append(course)

        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500




# ------------------ UPDATE STUDENT ------------------
@students_api_bp.route('/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        data = request.get_json()

        if 'name' in data:
            student.name = data['name']

        if 'age' in data:
            age = data['age']
            if not isinstance(age, int) or age < 0:
                return jsonify({"error": "'age' must be a positive integer"}), 400
            student.age = age

        if 'courses' in data:
            course_names = data['courses']
            if not isinstance(course_names, list):
                return jsonify({"error": "'courses' must be a list of course names"}), 400
            student.courses.clear()
            for cname in course_names:
                course = Course.query.filter_by(name=cname).first()
                if course:
                    student.courses.append(course)
                else:
                    new_course = Course(name=cname)
                    db.session.add(new_course)
                    student.courses.append(new_course)

        db.session.commit()
        return jsonify(student.to_dict()), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# ------------------ DELETE STUDENT ------------------
@students_api_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
