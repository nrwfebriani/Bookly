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
# db = SQLAlchemy()

app = Flask(__name__)

app.secret_key = "booklybagus"

# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql+mysqlconnector://powerpuffgirls:bookly123_@senpro-bookly.mysql.database.azure.com/db-bookly"

# app.config["MYSQL_HOST"] = "senpro-bookly.mysql.database.azure.com"
# app.config["MYSQL_USER"] = "powerpuffgirls"
# app.config["MYSQL_PASSWORD"] = "bookly123_"
# app.config["MYSQL_DB"] = "db-bookly"

config = {
    "host": "senpro-bookly.mysql.database.azure.com",
    "user": "powerpuffgirls",
    "password": "bookly123_",
    "database": "db-bookly",
    "client_flags": [mysql.connector.ClientFlag.SSL],
    "ssl_ca": "DigiCertGlobalRootCA.crt.pem",
}

mysql2 = MySQL(app)

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()


@app.route("/")
def home():
    return render_template(
        "home.html",
        book_name=list(popular_df["Book-Title"].values),
        author=list(popular_df["Book-Author"].values),
        image=list(popular_df["Image-URL-M"].values),
        votes=list(popular_df["num_ratings"].values),
        rating=list(popular_df["avg_ratings"].values.round(2)),
    )


@app.route("/home")
def home2():
    return render_template("home.html")


@app.route("/recommend")
def recommend():
    return render_template("recommend.html")


@app.route("/recommend_books", methods=["post"])
def recommend_book():
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
    return render_template("recommend.html", data=data)


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


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return render_template("login.html")


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        # # Retrieve the hashed password
        # hash = password + app.secret_key
        # hash = hashlib.sha1(hash.encode())
        # password = hash.hexdigest()
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM user WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return the result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            # Redirect to home page
            return "Logged in successfully!"
        else:
            # Account doesnt exist or username/password incorrect
            error = "Incorrect username/password!"
    return render_template("login.html", error=error)


# Route for handling the register page logic
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "name" in request.form
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
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            error = "Username must contain only characters and numbers!"
        elif not name or not username or not password or not email:
            error = "Please fill out the form!"
        else:
            # # Hash the password
            # hash = password + app.secret_key
            # hash = hashlib.sha1(hash.encode())
            # password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute(
                "INSERT INTO user VALUES (NULL, %s, %s, %s)",
                (
                    name,
                    username,
                    password,
                    email,
                ),
            )
            mysql2.connection.commit()
            error = "You have successfully registered!"
    elif request.method == "POST":
        # Form is empty... (no POST data)
        error = "Invalid Credentials. Please try again."
    # Show registration form with message (if any)
    return render_template("register.html", error=error)


if __name__ == "__main__":
    app.debug = True
    app.run()
