import csv
from datetime import datetime

def match_and_assign_parking(file1, file2, output_file, parking_data_file):

  # Data structures
  parking_data = {"A": 50, "B": 50, "C": 50, "D": 50, "Visitor": 50}  # Available slots per parking lot type
  assigned_parking = {}  # Dictionary to store assigned parking (numberplate: lot)
  unmatched_plates = set()  # Set to store unmatched number plates

  # Read approved vehicles data
  with open(file2, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
      numberplate, parking_lot = row[0], row[1]
      assigned_parking[numberplate] = parking_lot

  # Read parking entries (assuming numberplate in first column, timestamp in second column)
  with open(file1, 'r') as csvfile:
    reader = csv.reader(csvfile)
    timestamp = None  # Initialize timestamp outside the loop
    for row in reader:
      if len(row) < 2:  # Check if there are at least 2 columns
          print(f"Warning: Invalid row in 'parking_entries_exits.csv' - Missing columns.")
          continue  # Skip rows with missing columns

      numberplate1, timestamp_str = row[0], row[1]
      unmatched_plates.add(numberplate1)  # Initially all plates are unmatched

      try:
          timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # Assuming timestamp format
      except ValueError:
          print(f"Warning: Invalid timestamp format for '{numberplate}' in 'parking_entries_exits.csv'.")
          continue  # Skip entries with invalid timestamps

      # Check for assigned parking lot
      if numberplate1 in assigned_parking:
        parking_lot = assigned_parking[numberplate1]
        if parking_data[parking_lot] > 0:
          parking_data[parking_lot] -= 1  # Reduce available slots if not full
          unmatched_plates.remove(numberplate1)  # Remove from unmatched if matched

  # Write assigned parking results
  with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Number Plate", "Assigned Parking Lot", "Available Slots", "Timestamp"])
    for numberplate1, parking_lot in assigned_parking.items():
      if numberplate1 not in unmatched_plates:  # Only include matched plates
        available_slots = parking_data[parking_lot]
        writer.writerow([numberplate1, parking_lot, available_slots, timestamp])

  # Write remaining parking slots data
  with open(parking_data_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Parking Lot Type", "Available Slots", "Timestamp"])

    # Use the previously captured timestamp from processing entries
    writer.writerow([parking_lot, slots, timestamp] for parking_lot, slots in parking_data.items())

# Example usage (replace with your file paths)
file1 = "parking_entries_exits.csv"
file2 = "approved_vehicles.csv"
output_file = "assigned_parking.csv"
parking_data_file = "parking_data.csv"

match_and_assign_parking(file1, file2, output_file, parking_data_file)

print(f"Matching and parking lot assignment completed. Results saved to '{output_file}'.")
print(f"Parking data saved to '{parking_data_file}'.")
