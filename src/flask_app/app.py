from flask import Flask, render_template

app = Flask(__name__)

# صفحة رئيسية لطيفة
@app.route("/")
def home():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>My Flask App</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root { --bg:#f7f7fb; --card:#fff; --text:#222; --muted:#666; --accent:#6a5acd; }
    body { margin:0; font-family:system-ui, Arial, sans-serif; background:var(--bg); color:var(--text); }
    header { padding:28px; color:#fff; background:linear-gradient(135deg, #6a5acd, #00bcd4); }
    main { max-width:760px; margin:36px auto; background:var(--card); padding:28px; border-radius:16px;
           box-shadow:0 8px 24px rgba(0,0,0,.08); }
    h1 { margin:0 0 4px; }
    .muted { color:#e8f7ff; opacity:.9; }
    .btn { display:inline-block; margin-top:14px; padding:10px 16px; border-radius:10px; color:#fff;
           text-decoration:none; background:var(--accent); }
    code { background:#f0f0f5; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <header>
    <h1>Welcome to my Flask App 🎉</h1>
    <div class="muted">Lightweight • Simple • Fast</div>
  </header>
  <main>
    <h2>Home</h2>
    <p>Try the hello route with your name:</p>
    <p><code>/hello/Dana</code> → <a class="btn" href="/hello/Dana">Open</a></p>
  </main>
</body>
</html>
    """

# صفحة ترحيب باسم في المسار
@app.route("/hello/<name>")
def say_hello(name):
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Hello {name}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{ margin:0; font-family:system-ui, Arial, sans-serif; background:#f7f7fb; color:#222; }}
    main {{ max-width:760px; margin:60px auto; background:#fff; padding:28px; border-radius:16px;
           box-shadow:0 8px 24px rgba(0,0,0,.08); }}
    a.btn {{ display:inline-block; margin-top:14px; padding:10px 16px; border-radius:10px; color:#fff;
            text-decoration:none; background:#6a5acd; }}
  </style>
</head>
<body>
  <main>
    <h1>Hello, {name}! 👋</h1>
    <p>Nice to meet you.</p>
    <a class="btn" href="/">Back to Home</a>
  </main>
</body>
</html>
    """

if __name__ == "__main__":
    # debug=True = مفعّل الـ auto-reload + صفحة أخطاء مفيدة أثناء التطوير
    app.run(debug=True)
