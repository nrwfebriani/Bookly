import streamlit as st
from hydralit import HydraHeadApp


class AuthorPage(HydraHeadApp):
    def run(self):
        st.title('Categorize by Author')
