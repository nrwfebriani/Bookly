import streamlit as st

from hydralit import HydraHeadApp


class ProfilePage(HydraHeadApp):
    def run(self):
        st.title('Profile')
