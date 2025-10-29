from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
@login_required
def index():
    # نعرض home.html كما هو، بس صار محمي
    return render_template("home.html", username=getattr(current_user, "username", ""))
