import csv
from datetime import datetime

def match_and_assign_parking(file1, file2, output_file, parking_data_file):

  # Data structures
  parking_data = {"A": 50, "B": 50, "C": 50, "D": 50, "Visitor": 50}  # Available slots per parking lot type
  assigned_parking = {}  # Dictionary to store assigned parking (numberplate: lot)
  entry_data = {}  # Dictionary to store entry data (numberplate: {timestamp: "in", ...})

  # Read approved vehicles data
  with open(file2, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
      numberplate, parking_lot = row[0], row[1]
      assigned_parking[numberplate] = parking_lot

  # Read parking entries (assuming numberplate in first column, exit timestamp in third column)
  with open(file1, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      if len(row) < 3:  # Check if there are at least 3 columns
          print(f"Warning: Invalid row in 'parking_entries_exits.csv' - Missing columns.")
          continue  # Skip rows with missing columns

      numberplate, timestamp_str, _ = row[0], row[2], row[1]  # Ignore unnecessary second column

      try:
          timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # Assuming timestamp format
      except ValueError:
          print(f"Warning: Invalid timestamp format for '{numberplate}' in 'parking_entries_exits.csv'.")
          continue  # Skip entries with invalid timestamps

      # Check entry/exit status based on presence in 'entry_data'
      if numberplate in entry_data:
          entry_data[numberplate]["out_timestamp"] = timestamp  # Update exit timestamp
          parking_data[assigned_parking[numberplate]] += 1  # Increase slot count for assigned lot
          del entry_data[numberplate]  # Remove entry data after exit
      else:
          entry_data[numberplate] = {"in_timestamp": timestamp}  # Store entry timestamp

  # Write assigned parking results (considering only entries with both timestamps)
  with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Number Plate", "Assigned Parking Lot", "Available Slots", "Entry Timestamp", "Exit Timestamp"])
    for numberplate, parking_lot in assigned_parking.items():
      if numberplate in entry_data and "out_timestamp" in entry_data[numberplate]:
        available_slots = parking_data[parking_lot]
        entry_timestamp = entry_data[numberplate]["in_timestamp"]
        exit_timestamp = entry_data[numberplate]["out_timestamp"]
        writer.writerow([numberplate, parking_lot, available_slots, entry_timestamp, exit_timestamp])

  # Write updated parking slots data
  with open(parking_data_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Parking Lot Type", "Available Slots", "Timestamp"])
    writer.writerow([parking_lot, slots, timestamp] for parking_lot, slots in parking_data.items())

# Example usage (replace with your file paths)
file1 = "parking_entries_exits.csv"
file2 = "approved_vehicles.csv"
output_file = "assigned_parking.csv"
parking_data_file = "parking_data.csv"

match_and_assign_parking(file1, file2, output_file, parking_data_file)

print(f"Matching and parking lot assignment completed. Results saved to '{output_file}'.")
print(f"Parking data saved to '{parking_data_file}'.")
