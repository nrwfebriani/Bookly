import streamlit as st

from hydralit import HydraHeadApp


class SavedPage(HydraHeadApp):
    def run(self):
        st.title('Saved Books')
