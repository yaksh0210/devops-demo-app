from flask import Flask, render_template, request, redirect, session, url_for
import redis

app = Flask(__name__)
app.secret_key = "devops-secret"

cache = redis.Redis(host='redis', port=6379)

USER = "admin"
PASS = "admin123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USER and request.form["password"] == PASS:
            session["user"] = USER
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    cache.incr("hits")
    hits = cache.get("hits").decode()

    return render_template("home.html", hits=hits, user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)