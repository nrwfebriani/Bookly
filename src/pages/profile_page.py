import streamlit as st
from hydralit import HydraHeadApp
from hydralit import HydraApp
from register_page import RegisterPage
from login_page import LoginPage

class ProfilePage(HydraHeadApp):
    def run(self):
        st.title('Profile')
        app = HydraApp(title='Bookly')
        
        # option = st.selectbox('Profile', ('Register','Login'))
