from flask import Flask, request, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import mysql.connector
from mysql.connector import errorcode
from flask_mysqldb import MySQL

popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

app = Flask(__name__)

app.secret_key = "booklybagus"

config = {
    "host": "senpro-bookly.mysql.database.azure.com",
    "user": "powerpuffgirls",
    "password": "bookly123_",
    "database": "db-bookly",
    "client_flags": [mysql.connector.ClientFlag.SSL],
    "ssl_ca": "DigiCertGlobalRootCA.crt.pem",
}

mysql2 = MySQL(app)

conn = mysql.connector.connect(**config)


@app.route("/")
def home():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template(
        "home.html",
        book_name=list(popular_df["Book-Title"].values),
        author=list(popular_df["Book-Author"].values),
        image=list(popular_df["Image-URL-M"].values),
        votes=list(popular_df["num_ratings"].values),
        rating=list(popular_df["avg_ratings"].values.round(2)),
        username=username,
    )


@app.route("/recommend")
def recommend():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template("recommend.html", username=username)


@app.route("/recommend_books", methods=["post"])
def recommend_book():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    user_input = request.form.get("user_input")
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
    )[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)

    print(data)
    return render_template("recommend.html", data=data, username=username)


@app.route("/category")
def category():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template("category.html", username=username)


@app.route("/savedbooks")
def savedbooks():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template("savedbooks.html", username=username)


@app.route("/profile")
def profile():
    if "name" in session and "username" in session and "email" in session:
        name = session["name"]
        username = session["username"]
        email = session["email"]
        return render_template(
            "profile.html", name=name, username=username, email=email
        )
    else:
        return render_template("profile.html", name="", username="", email="")


@app.route("/bygenre")
def bygenre():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template("bygenre.html", username=username)


@app.route("/byauthor")
def byauthor():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    return render_template("byauthor.html", username=username)


@app.route("/logout")
def logout():
    if "username" in session and "email" in session:
        username = session["username"]
    else:
        username = ""
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    cursor = conn.cursor(dictionary=True)
    error = ""
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            "SELECT * FROM user WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return the result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            # Create session data, we can access this data in other routes
            a = user["id"]
            b = user["username"]
            c = user["email"]
            d = user["name"]
            session["loggedin"] = True
            session["id"] = a
            session["username"] = b
            session["email"] = c
            session["name"] = d
            # Redirect to home page
            msg = "Logged in successfully!"
        else:
            # Account doesnt exist or username/password incorrect
            msg = "Incorrect username/password!"
    cursor.close()
    return render_template("login.html", msg=msg)


# @app.route("/loginapp")
# def loginapp():
#     return render_template("login.html")


# Route for handling the register page logic
@app.route("/register", methods=["GET", "POST"])
def register():
    cursor = conn.cursor(dictionary=True)
    error = ""
    msg = ""
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        # Create variables for easy access
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            error = "Account already exists!"
        elif not name or not username or not password or not email:
            error = "Please fill out the form!"
        else:
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute(
                "INSERT INTO user VALUES (NULL, %s, %s, %s, %s)",
                (
                    name,
                    username,
                    password,
                    email,
                ),
            )
            conn.commit()
            msg = "You have successfully registered!"
    elif request.method == "POST":
        # Form is empty... (no POST data)
        error = "Invalid Credentials. Please try again."
    # Show registration form with message (if any)
    cursor.close()
    return render_template("register.html", error=error, msg=msg)


if __name__ == "__main__":
    app.debug = True
    app.run()
