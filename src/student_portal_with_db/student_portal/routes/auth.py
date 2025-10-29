from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from student_portal import db
from student_portal.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/login_register_guest.html", mode="register")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Welcome!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))
        flash("Invalid credentials", "error")
        return redirect(url_for("auth.login"))
    return render_template("auth/login_register_guest.html", mode="login")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
