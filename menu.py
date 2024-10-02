import streamlit as st

def menu():
    with open("style.css") as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/home.py", label="Home")
    st.sidebar.page_link("pages/register_vehicle.py", label="Register Vehicle")
    st.sidebar.page_link("pages/vehicle_log.py", label="Vehicle Log")
    st.sidebar.page_link("pages/vehicle_entry.py", label="Vehicle Entry")
    st.sidebar.page_link("pages/parking_insights.py", label="Parking Insights")