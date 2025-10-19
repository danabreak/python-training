from flask import Flask, render_template
from students import register_student_routes
import datetime

app = Flask(__name__)

register_student_routes(app)

@app.route("/")
def home():
    return render_template("home.html", current_year=datetime.datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)
