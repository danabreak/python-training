# routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from student_portal import db
from student_portal.models import Student, Course
from flask_login import current_user

from student_portal.forms.edit_profile_form import EditProfileForm

from ._decorators import role_required   

students_bp = Blueprint(
    'students',
    __name__,
    url_prefix='/students',
    template_folder='../templates'
)







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
    form = EditProfileForm()

    if form.validate_on_submit():
        # 1) تحديث الاسم + العمر
        student.name = form.name.data
        student.age = form.age.data

        # 2) حفظ الصورة إذا تم رفعها
        file = form.profile_pic.data
        if file:
            from werkzeug.utils import secure_filename
            import os

            filename = secure_filename(file.filename)
            upload_dir = os.path.join("student_portal", "static", "uploads", "profile_pics")

            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            # حفظ اسم الملف في جدول User
            user.profile_pic = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('students.me'))

    # لما الصفحة تنفتح أول مرة: تحميل البيانات القديمة بالـ form
    if request.method == "GET":
        form.name.data = student.name
        form.age.data = student.age

    return render_template("students/edit_profile.html", form=form)
