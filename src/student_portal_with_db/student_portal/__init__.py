import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object=None):
    app = Flask(__name__, template_folder='templates')
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'school.db')

    app.config.update(
    SECRET_KEY = 'secret',
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
)

    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)

    from .routes.students import students_bp
    from .routes.students_api import students_api_bp

    app.register_blueprint(students_bp)
    app.register_blueprint(students_api_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app
