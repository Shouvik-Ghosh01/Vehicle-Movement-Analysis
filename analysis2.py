import csv
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_parking_occupancy(file1, file2):

  # Data structures
  parking_data = {"A": [], "B": [], "C": [], "D": [], "Visitor": []}  # List of timestamps per lot
  assigned_parking = {}  # Dictionary to store assigned parking (numberplate: lot)

  # Read approved vehicles data
  with open(file2, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
      numberplate, parking_lot = row[0], row[1]
      assigned_parking[numberplate] = parking_lot

  # Read parking entries (assuming numberplate in first column, timestamp in second/third column)
  with open(file1, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      if len(row) < 3:  # Check if there are at least 3 columns
          print(f"Warning: Invalid row in 'parking_entries_exits.csv' - Missing columns.")
          continue  # Skip rows with missing columns

      numberplate, timestamp_str, exit_str = row[0], row[1], row[2]  # Assuming timestamps in second/third column

      try:
          timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # Assuming timestamp format
      except ValueError:
          print(f"Warning: Invalid timestamp format for '{numberplate}' in 'parking_entries_exits.csv'.")
          continue  # Skip entries with invalid timestamps

      # Extract parking lot and append timestamp based on entry/exit
      parking_lot = assigned_parking.get(numberplate)  # Get assigned lot for numberplate
      if parking_lot and exit_str:  # Check for assigned lot and exit timestamp
        try:
          exit_timestamp = datetime.strptime(exit_str, "%Y-%m-%d %H:%M:%S")  # Assuming exit timestamp format
          parking_data[parking_lot].append(exit_timestamp - timestamp)  # Append duration (exit - entry)
        except ValueError:
          print(f"Warning: Invalid exit timestamp format for '{numberplate}' in 'parking_entries_exits.csv'.")
      elif parking_lot:  # Entry (assuming no exit timestamp means entry)
        parking_data[parking_lot].append(timestamp)

    # ... (rest of the code)

    # Calculate average parking duration per lot (handling timedelta objects)
    average_durations = {
        lot: sum(durations.total_seconds() / 3600 for durations in parking_data[lot]) / len(parking_data[lot])
        for lot, durations in parking_data.items() if durations}

  # ... (rest of the code)

  # Visualization - bar plot using Seaborn
  plt.figure(figsize=(10, 6))
  sns.barplot(x=average_durations.keys(), y=average_durations.values())
  plt.xlabel("Parking Lot")
  plt.ylabel("Average Parking Duration (hours)")
  plt.title("Average Parking Duration per Lot")
  plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
  plt.tight_layout()
  plt.show()

# Example usage (replace with your file paths)
file1 = "parking_entries_exits.csv"
file2 = "approved_vehicles.csv"

analyze_parking_occupancy(file1, file2)

print("Parking lot occupancy analysis complete. Visualization displayed.")
