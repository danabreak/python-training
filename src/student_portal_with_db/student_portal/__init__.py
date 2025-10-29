import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


db = SQLAlchemy()
login_manager = LoginManager()          # ← NEW
login_manager.login_view = "auth.login" # ← لما صفحة محمية تطلب تسجيل دخول

def create_app(config_object=None):
    app = Flask(__name__, template_folder='templates')
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'school.db')
    load_dotenv(os.path.join(base_dir, '.env'))  # ← NEW ✅


    app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET', 'dev-secret'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', f"sqlite:///{db_path}"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)         # ← NEW
    migrate = Migrate(app, db)  # ← NEW


 # لازم بعد init_app
    from .models import User            # ← NEW
    @login_manager.user_loader          # ← NEW
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .routes.students import students_bp
    from .routes.students_api import students_api_bp
    from .routes.auth import auth_bp              # ← NEW
    from .routes.dashboard import dashboard_bp    # ← NEW

    app.register_blueprint(students_bp)
    app.register_blueprint(students_api_bp)
    app.register_blueprint(auth_bp)               # ← NEW
    app.register_blueprint(dashboard_bp)          # ← NEW

    @app.route('/')
    def home():
     return render_template('home_guest.html')

    return app
