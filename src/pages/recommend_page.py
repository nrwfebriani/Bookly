import streamlit as st

from hydralit import HydraHeadApp


class RecommendPage(HydraHeadApp):
    def run(self):
        st.title('Recommend Me')
