from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to my Flask App! 🎉</h1>"

@app.route("/hello/<name>")
def say_hello(name):
    return f"<h2>Hello, {name}! 👋</h2>"

if __name__ == "__main__":
    app.run(debug=True)
