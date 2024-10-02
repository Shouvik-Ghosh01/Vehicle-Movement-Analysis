import streamlit as st
from utils import display_heading
from menu import menu


def main():
    with open("style.css") as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    menu()
    display_heading()
    # Adding space before the title
    st.markdown("<br>", unsafe_allow_html=True)

    st.title('Welcome to the Vehicle Registration and Monitoring App')

    # Adding space after the title
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        This application helps you register new vehicles and log their entry and exit times.
        Please select an option below to proceed.
    """)

    # Adding space after the title
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Custom CSS for centering and styling the cards
    st.markdown("""
        <style>
        div[data-testid="column"] {
            border: 2px solid #e6e6e6;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 8px 8px 0px 0px #4717F6;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create a 2x2 grid layout for the cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        css_car = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <i class="fa-solid fa-car fa-3x"></i>
        '''
        st.write(css_car, unsafe_allow_html=True)
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.subheader("Register Vehicle")
        st.write("Easily register your vehicle in minutes via our intuitive system")
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.page_link("pages/register_vehicle.py", label='Register Now', icon=":material/arrow_forward:", help=None, disabled=False, use_container_width=None)

    with col2:
        css_log = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <i class="fa-solid fa-table-list fa-3x"></i>
        '''
        st.write(css_log, unsafe_allow_html=True)
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.subheader("Vehicle Log")
        st.write("Keep track of your vehicle's parking activity and check records")
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.page_link("pages/vehicle_log.py", label='View Log', icon=":material/arrow_forward:", help=None, disabled=False, use_container_width=None)

    with col3:
        css_entry = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <i class="fa-solid fa-right-to-bracket fa-3x"></i>
        '''
        st.write(css_entry, unsafe_allow_html=True)
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.subheader("Vehicle Entry")
        st.write("Streamline the parking entry system with our automated process")
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.page_link("pages/vehicle_entry.py", label='Enter Parking', icon=":material/arrow_forward:", help=None, disabled=False, use_container_width=None)

    with col4:
        css_stats = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <i class="fa-solid fa-chart-line fa-3x"></i>
        '''
        st.write(css_stats, unsafe_allow_html=True)
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.subheader("Parking Insights")
        st.write("Gain valuable insights into campus parking trends and utilisation")
        st.markdown("""
            <br>
        """, unsafe_allow_html=True)
        st.page_link("pages/parking_insights.py", label='View Insights', icon=":material/arrow_forward:", help=None, disabled=False, use_container_width=None)

    st.markdown("""
        <br><br>
        ## About the Campus Parking Management System
        <br>
        The Campus Parking Management System is designed to streamline vehicle registration and monitoring on campus. 
        It comprises four key sections:
        <br><br>
        1. <b>Register Your Vehicle:</b> Easily register your vehicle in the system.
        <br><br>
        2. <b>Vehicle Log:</b> View and manage logs of vehicle entry and exit times.
        <br><br>
        3. <b>Vehicle Entry:</b> Record vehicle entry in real-time.
        <br><br>
        4. <b>Parking Insights:</b> Gain insights into parking usage and availability.
        <br><br>
    """, unsafe_allow_html=True)



if __name__ == '__main__':
    main()
