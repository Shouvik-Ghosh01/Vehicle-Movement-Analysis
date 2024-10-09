import streamlit as st
import pandas as pd
from datetime import datetime
from utils import display_heading
from menu import menu

# Load authorized vehicles and parking data CSV files
authorized_vehicles_df = pd.read_csv('datasets/authorized_vehicles.csv')
vehicle_logs_df = pd.read_csv('datasets/indian_vehicle_parking_data.csv')

def main():
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    menu()
    display_heading()

    st.title("Parking Insights")
    st.markdown("This page provides insights into parking data.")

    # Date selection for maximum parked hour
    st.header("Find Hour with Maximum Cars Parked")
    max_parked_date = st.date_input("Select a date for max parked hour", datetime.today(), key="max_parked_date")

    max_parked_date = datetime.combine(max_parked_date, datetime.min.time())  # Set time to midnight

    vehicle_logs_df['In Time'] = pd.to_datetime(vehicle_logs_df['In Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')


    logs_on_date = vehicle_logs_df[pd.to_datetime(vehicle_logs_df['In Time']).dt.date == max_parked_date.date()]

    if not logs_on_date.empty:
        # Group by hour and count number of vehicles parked
        logs_on_date['Hour'] = pd.to_datetime(logs_on_date['In Time']).dt.hour
        hour_counts = logs_on_date['Hour'].value_counts()

        if not hour_counts.empty:
            max_hour = hour_counts.idxmax()
            st.success(f"The hour with the maximum number of cars parked on {max_parked_date.date()} is {max_hour}:00.")
        else:
            st.info("No parking data available for this date.")
    else:
        st.info("No parking data available for this date.")

    # Date and time selection for parking slot occupancy
    st.header("Parking Slot Occupancy")
    occupancy_date = st.date_input("Select a date for occupancy", datetime.today(), key="occupancy_date")
    occupancy_time = st.time_input("Select a time for occupancy", key="occupancy_time")
    occupancy_datetime = datetime.combine(occupancy_date, occupancy_time)

    # Button to trigger search
    search_button = st.button("Search", key="search_occupancy")

    if search_button:
        # Assuming vehicle_logs_df is your DataFrame containing datetime strings
        vehicle_logs_df['Out Time'] = pd.to_datetime(vehicle_logs_df['Out Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

        # Ensure 'Out Time' is in datetime format
        vehicle_logs_df['Out Time'] = pd.to_datetime(vehicle_logs_df['Out Time'], errors='coerce')

        # Filter logs for the selected date and time
        logs_at_time = vehicle_logs_df[(pd.to_datetime(vehicle_logs_df['In Time']) <= occupancy_datetime) &
                                       (vehicle_logs_df['Out Time'] >= occupancy_datetime)]

        latest_logs = logs_at_time.sort_values(by='In Time').drop_duplicates(subset='Slot Number', keep='last')

        if not latest_logs.empty:
            st.subheader("Current Parking Slot Occupancy")
            # Sort by 'In Time' in ascending order before displaying
            latest_logs_sorted = latest_logs.sort_values(by='In Time')
            # Format date columns
            latest_logs_sorted['In Time'] = latest_logs_sorted['In Time'].dt.strftime('%d-%m-%Y %H:%M:%S')
            latest_logs_sorted['Out Time'] = latest_logs_sorted['Out Time'].dt.strftime('%d-%m-%Y %H:%M:%S')
            st.table(latest_logs_sorted[['Slot Number', 'Vehicle Number', 'In Time', 'Out Time']].reset_index(drop=True))
        else:
            st.info("No parking data available at this time or the selected date and time.")

    # Vehicle search by plate number and date
    st.header("Search Vehicle by Plate Number and Date")
    vehicle_plate = st.text_input("Enter Vehicle Number Plate", key="vehicle_plate")
    search_date = st.date_input("Select a date for search", datetime.today(), key="search_date")

    if st.button("Search", key="search_number"):
        # Filter logs for the selected vehicle and date
        vehicle_logs_filtered = vehicle_logs_df[(vehicle_logs_df['Vehicle Number'] == vehicle_plate) &
                                                (pd.to_datetime(vehicle_logs_df['In Time']).dt.date == search_date)]

        if not vehicle_logs_filtered.empty:
            st.success(f"Parking records found for Vehicle {vehicle_plate} on {search_date}:")
            # Sort by 'In Time' in ascending order before displaying
            vehicle_logs_filtered_sorted = vehicle_logs_filtered.sort_values(by='In Time')
            # Format date columns
            vehicle_logs_filtered_sorted['In Time'] = pd.to_datetime(vehicle_logs_filtered_sorted['In Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
            vehicle_logs_filtered_sorted['Out Time'] = pd.to_datetime(vehicle_logs_filtered_sorted['Out Time'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
            st.table(vehicle_logs_filtered_sorted[['Slot Number', 'In Time', 'Out Time']].reset_index(drop=True))
        else:
            st.info(f"No parking record found for Vehicle {vehicle_plate} on {search_date}.")



if __name__ == "__main__":
    main()
