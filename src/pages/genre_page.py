import streamlit as st
from hydralit import HydraHeadApp


class GenrePage(HydraHeadApp):
    def run(self):
        st.title('Categorize by Genre')
