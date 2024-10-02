import streamlit as st
import pandas as pd
from dateutil.parser import parse
from utils import display_heading
from menu import menu

# Load authorized vehicles and parking data CSV files
authorized_vehicles_df = pd.read_csv('datasets/authorized_vehicles.csv')
vehicle_logs_df = pd.read_csv('datasets/indian_vehicle_parking_data.csv')

def calculate_parking_time(row):
    in_time = parse(row['In Time'])
    out_time = parse(row['Out Time'])
    total_parking_time = out_time - in_time
    return total_parking_time

def format_parking_time(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes"

def format_datetime(dt):
    return dt.strftime('%d-%m-%Y %H:%M:%S')

def main():
    with open("../style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
        
    menu()
    display_heading()

    st.title("Vehicle Log")
    st.markdown("This page logs vehicle entry and exit times.")
    
    # Initialize session state to hold log data if not already initialized
    if 'vehicle_logs' not in st.session_state:
        st.session_state.vehicle_logs = []

    # Form to input vehicle details
    with st.form("log_entry_form"):
        plate_number = st.text_input("Vehicle Number Plate")
        submitted = st.form_submit_button("Check Log")

        if submitted:
            # Check if vehicle is authorized
            if plate_number in authorized_vehicles_df['Plate_Number'].values:
                st.success(f"Vehicle {plate_number} is authorized.")

                # Fetch logs for the vehicle from vehicle_logs_df
                vehicle_logs = vehicle_logs_df[vehicle_logs_df['Vehicle Number'] == plate_number]

                if not vehicle_logs.empty:
                    st.markdown("### Vehicle Logs")
                    
                    # Calculate total parking time for each log
                    vehicle_logs['Total Parking Time'] = vehicle_logs.apply(calculate_parking_time, axis=1)
                    
                    # Format Total Parking Time for display
                    vehicle_logs['Total Parking Time'] = vehicle_logs['Total Parking Time'].apply(format_parking_time)

                    # Format In Time and Out Time
                    vehicle_logs['In Time'] = pd.to_datetime(vehicle_logs['In Time']).apply(format_datetime)
                    vehicle_logs['Out Time'] = pd.to_datetime(vehicle_logs['Out Time']).apply(format_datetime)

                    # Sort vehicle logs by 'In Time' from oldest to newest
                    vehicle_logs.sort_values(by='In Time', inplace=True)

                    # Display the logs in a tabular format without showing index numbers
                    st.table(vehicle_logs[['Slot Number', 'In Time', 'Out Time', 'Total Parking Time']].reset_index(drop=True))
                else:
                    st.info("No logs found for this vehicle in the last 30 days.")
                
            else:
                st.error(f"Vehicle {plate_number} is not authorized.")

    st.markdown("<br><br>", unsafe_allow_html=True)
        
    # GitHub link and icon using HTML and CSS for styling
    github_link = "https://github.com/roysammy123/Vehicle-Movement-Analysis-and-Insight-Generation-Intel-Unnati-Industrial-Program"
    github_icon = "https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg"

    # Contributors section
    contributors = [
        {"name": "Soumyajit Roy", "github": "https://github.com/roysammy123"},
        {"name": "Manav Malhotra", "github": "https://github.com/Manav173"},
        {"name": "Ishtaj Kaur Deol", "github": "https://github.com/Ishtaj"},
        {"name": "Swarnav Kumar", "github": "https://github.com/Swarnav-Kumar"}
    ]

    contributors_html = " ".join([
        f'<a href="{contributor["github"]}" target="_blank" class="contributor-button">{contributor["name"]}</a>'
        for contributor in contributors
    ])

    st.markdown(f"""
    <style>
    .github-link {{
        display: inline-block;
        background-color: #A239CA;
        color: #ffffff !important;
        padding: 10px 20px;
        font-size: 18px;
        text-decoration: none;
        border-radius: 5px;
        text-align: center;
    }}
    .github-link img {{
        vertical-align: middle;
        margin-left: 10px;
    }}
    .contributor-button {{
        display: inline-block;
        background-color: #4717F6;
        padding: 8px 16px;
        font-size: 14px;
        text-decoration: none;
        border-radius: 5px;
        margin: 8px 8px;
        margin-bottom: 0;  /* Remove bottom margin */
    }}
    .contributor-button:hover {{
        background-color: #0056b3;
    }}
    .contributor-button:visited,
    .contributor-button:active,
    .contributor-button:focus {{
        color: #ffffff;
        text-decoration: none;
    }}
    </style>

    <p style='text-align: center; margin-top: 32px'>
    <a href="{github_link}" target="_blank" class="github-link">
        View on GitHub <img src="{github_icon}" alt="GitHub" width="20" height="20">
    </a>
    </p>
    <br>

    <div style="text-align: center; margin-top: 16px;">
        <p style="font-size: 16px;"><b>Contributors:</b></p>
        <div style="display: inline-block;">{contributors_html}</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
