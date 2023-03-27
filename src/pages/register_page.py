import streamlit as st

from hydralit import HydraHeadApp


class RegisterPage(HydraHeadApp):
    def run(self):
        st.title('Register')
