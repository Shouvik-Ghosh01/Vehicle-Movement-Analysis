# utils.py
import streamlit as st

def display_heading():
    with open("style.css") as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
        
    st.markdown(
        """
        <h1 style="text-align: center; color: #ff4b4b;">CAMPUS PARKING SYSTEM</h1>
        """,
        unsafe_allow_html=True
    )
