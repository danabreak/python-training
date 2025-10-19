from flask import render_template, request, redirect, url_for
from models import add_student, get_all_students, get_student_by_id, add_grade



def register_student_routes(app):


    # ----------show students----------
    @app.route("/students")
    def list_students():
        students = get_all_students()
        return render_template("students/list.html", students=students)


    # ----------add student----------
    @app.route("/students/register", methods=["GET", "POST"])
    def register_student():
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            location = request.form.get("location")
            birthdate = request.form.get("birthdate")
            try:
                add_student(name, email, location, birthdate)
                return redirect(url_for("list_students"))
            except ValueError as e:
                return f"Error: {e}", 400
        return render_template("students/register.html")


    # ----------show student details----------
    @app.route("/students/<int:sid>")
    def student_detail(sid):
        student = get_student_by_id(sid)
        if student is None:
            return "Student not found", 404
        return render_template("students/detail.html", student=student)


    # ----------add grade to a students----------
    @app.route("/students/<int:sid>/add_grade", methods=["POST"])
    def add_grade_route(sid):
        grade = request.form.get("grade")
        try:
            add_grade(sid, float(grade))
            return redirect(url_for("student_detail", sid=sid))
        except KeyError as e:
            return f"Error: {e}", 404
        except ValueError:
            return "Invalid grade", 400
