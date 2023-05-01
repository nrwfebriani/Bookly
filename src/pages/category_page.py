import streamlit as st
from hydralit import HydraApp
from hydralit import HydraHeadApp
from genre_page import GenrePage
from author_page import AuthorPage


class CategoryPage(HydraHeadApp):
    def run(self):
        app = HydraApp(title='Bookly')

        option = st.selectbox('Category', ('by Author', 'by Genre'))
        if option == 'by Author':
            app.run(AuthorPage)
