from flask import Flask, request, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def home2():
    return render_template("home.html")

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")


@app.route("/category")
def category():
    return render_template("category.html")


@app.route("/savedbooks")
def savedbooks():
    return render_template("savedbooks.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/bygenre")
def bygenre():
    return render_template("bygenre.html")


@app.route("/byauthor")
def byauthor():
    return render_template("byauthor.html")


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)

# Route for handling the register page logic
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("register.html", error=error)


if __name__ == "__main__":
    app.debug = True
    app.run()
