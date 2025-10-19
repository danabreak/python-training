from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev" 

students = [] 

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        sid   = request.form.get("sid", "").strip()
        email = request.form.get("email", "").strip()

        errors = []
        if not name: errors.append("Name is required.")
        if not sid: errors.append("Student ID is required.")
        if not email or "@" not in email: errors.append("Valid email is required.")

        if errors:
            for e in errors: flash(e)
            return render_template("form.html")

        students.append({"name": name, "sid": sid, "email": email})
        return redirect(url_for("list_students"))

    return render_template("form.html")

@app.get("/students")
def list_students():
    return render_template("students.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
