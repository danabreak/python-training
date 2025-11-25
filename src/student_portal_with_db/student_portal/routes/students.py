# routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from student_portal import db
from student_portal.models import Student, Course
from flask_login import current_user

from ._decorators import role_required   

students_bp = Blueprint(
    'students',
    __name__,
    url_prefix='/students',
    template_folder='../templates'
)




@students_bp.route('/', methods=['GET'])
@login_required
def list_students():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Student.query

    if q:
        query = query.filter(Student.name.ilike(f"%{q}%"))

    students = query.order_by(Student.id.desc()).paginate(page=page, per_page=5)

    return render_template(
        'students/list.html',
        students=students,
        q=q
    )






@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')  
def add_student():
    courses = Course.query.all()

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        age_raw = request.form.get('age') or '0'
        try:
            age = int(age_raw)
        except ValueError:
            age = 0

        if not name:
            flash('Name is required', 'error')
            return render_template('students/add.html', courses=courses)

        student = Student(name=name, age=age)
        db.session.add(student)

        for cid in request.form.getlist('courses'):
            c = Course.query.get(int(cid))
            if c:
                student.courses.append(c)

        db.session.commit()
        flash('Student added', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/add.html', courses=courses)


@students_bp.route('/me', methods=['GET'])
@login_required
@role_required('student') 
def me():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash("Your student profile is not linked yet.", "warning")
        return redirect(url_for('dashboard.index'))

    return render_template('students/me.html', student=student)



@students_bp.route("/courses", methods=["GET"])
@login_required
@role_required("student")
def browse_courses():
    from student_portal.models import Course, EnrollmentRequest

    student = current_user.student

    # كل الكورسات
    all_courses = Course.query.all()

    # الطلبات الحالية للطالب
    requests = {req.course_id: req.status for req in student.enrollment_requests}

    # الكورسات اللي هو منضم إلها بالفعل
    enrolled = {c.id for c in student.courses}

    return render_template(
        "students/browse_courses.html",
        courses=all_courses,
        requests=requests,
        enrolled=enrolled
    )



@students_bp.route("/request-enroll/<int:course_id>", methods=["POST"])
@login_required
@role_required("student")
def request_enroll(course_id):
    from student_portal.models import Course, EnrollmentRequest

    student = current_user.student
    course = Course.query.get_or_404(course_id)

    # الطالب مسجّل بالفعل؟
    if course in student.courses:
        flash("You are already enrolled in this course.", "info")
        return redirect(url_for("students.browse_courses"))

    # عنده طلب pending؟
    existing = EnrollmentRequest.query.filter_by(
        student_id=student.id,
        course_id=course.id,
        status="pending"
    ).first()

    if existing:
        flash("You already requested enrollment for this course.", "info")
        return redirect(url_for("students.browse_courses"))

    # إنشاء الطلب
    req = EnrollmentRequest(
        student_id=student.id,
        course_id=course.id,
        status="pending"
    )

    db.session.add(req)
    db.session.commit()

    flash("Enrollment request sent.", "success")
    return redirect(url_for("students.browse_courses"))



@students_bp.route("/my-courses")
@login_required
@role_required("student")
def my_courses():
    student = current_user.student

    # الكورسات التي هو مسجل فيها فعلياً
    enrolled_courses = student.courses

    return render_template(
        "students/my_courses.html",
        courses=enrolled_courses
    )


@students_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
@role_required('student')
def edit_profile():
    student = current_user.student
    user = current_user

    if request.method == "POST":
        # تعديل الاسم
        new_name = request.form.get("name", "").strip()
        age_raw = request.form.get("age", "0").strip()

        try:
            new_age = int(age_raw)
        except:
            new_age = student.age

        if new_name:
            student.name = new_name
        student.age = new_age

        # رفع الصورة
        file = request.files.get("profile_pic")
        if file and file.filename:
            import os
            from werkzeug.utils import secure_filename

            filename = secure_filename(file.filename)
            save_path = os.path.join('student_portal', 'static', 'uploads', 'profile_pics', filename)

            file.save(save_path)

            user.profile_pic = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('students.me'))

    return render_template('students/edit_profile.html', student=student, user=user)


