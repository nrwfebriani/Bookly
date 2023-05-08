from flask import Flask, request, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/recommend')
def recommend():
    return render_template("recommend.html")

@app.route('/category')
def category():
    return render_template("category.html")

@app.route('/savedbooks')
def savedbooks():
    return render_template("savedbooks.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
