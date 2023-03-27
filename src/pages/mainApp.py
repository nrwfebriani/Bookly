import streamlit as st
from hydralit import HydraApp
from author_page import AuthorPage
from genre_page import GenrePage
from login_page import LoginPage
from profile_page import ProfilePage
from recommend_page import RecommendPage
from register_page import RegisterPage
from saved_page import SavedPage

if __name__ == '__main__':
    app = HydraApp(title='Bookly')

    app.add_app('Author', app=AuthorPage())
    app.add_app('Genre', app=GenrePage())
    app.add_app('Recommend Me', app=RecommendPage())
    app.add_app('Saved Books', app=SavedPage())
    app.add_app('Profile', app=ProfilePage())
    app.add_app('Register', app=RegisterPage())
    app.add_app('Login', app=LoginPage())

    app.run()
