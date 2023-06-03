from flask import Flask, request, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_ratings'].values.round(2))
                           )

@app.route("/home")
def home2():
    return render_template("home.html")

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

@app.route("/recommend_books", methods=['post'])
def recommend_book():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
      item = []
      temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
      item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

      data.append(item)
    
    print(data)
    return render_template('recommend.html',data=data)

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
