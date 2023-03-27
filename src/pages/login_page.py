import streamlit as st
from hydralit import HydraHeadApp


class LoginPage(HydraHeadApp):
    def run(self):
        st.title('Login')
