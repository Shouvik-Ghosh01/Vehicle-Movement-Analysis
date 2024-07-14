import random
from datetime import datetime, timedelta
import random
import csv
from string import ascii_uppercase
from datetime import datetime, timedelta


def generate_plate(state):
  """
  Generates a random number plate for the specified state.

  Args:
      state (str): The state code (OD, WB, or BR).

  Returns:
      str: The generated number plate.
  """
  series = ''.join(random.choices(ascii_uppercase, k=2))  # Two random uppercase letters
  number = random.randint(1000, 9999)  # Four-digit number between 1000 and 9999
  return f"{state}-{series}-{number}"


def generate_timestamps(start_date, end_date):
  """
  Generates two random timestamps within the specified date range with a significant time difference.

  Args:
      start_date (datetime): The start date (inclusive).
      end_date (datetime): The end date (inclusive).

  Returns:
      tuple: A tuple containing two datetime objects (in timestamp format without milliseconds).
  """
  time_delta = end_date - start_date  # Calculate total time difference
  total_seconds = time_delta.total_seconds()

  # Generate random time within the date range
  random_seconds = random.randint(0, int(total_seconds))
  in_timestamp = (start_date + timedelta(seconds=random_seconds)).isoformat(sep=' ')  # Remove milliseconds

  # Simulate significant variability in parking duration (e.g., 30 minutes to 8 hours)
  min_duration = timedelta(minutes=30)
  max_duration = timedelta(hours=8)
  parking_duration = timedelta(seconds=random.randint(min_duration.total_seconds(), max_duration.total_seconds()))

  # Ensure in_timestamp is before out_timestamp
  out_timestamp = (datetime.fromisoformat(in_timestamp) + parking_duration).isoformat(sep=' ')  # Remove milliseconds

  return in_timestamp, out_timestamp


states = ["OD", "WB", "BR"]
num_plates = 250

# Specify a reasonable date range (adjust as needed)
start_date = datetime(year=2024, month=7, day=1)  # Example: Start of July
end_date = datetime(year=2024, month=7, day=13)  # Example: Current date

# Generate and store data in CSV file
data = []
for _ in range(num_plates):
  state = random.choice(states)
  plate = generate_plate(state)
  in_timestamp, out_timestamp = generate_timestamps(start_date, end_date)
  data.append([plate, in_timestamp, out_timestamp])  # Append data with plate as first column

with open("parking_entries_exits.csv", "w", newline="") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["NumberPlate", "In Timestamp", "Out Timestamp"])  # Write header row
  writer.writerows(data)  # Write all generated data rows

print(f"Generated {num_plates} random number plates with timestamps stored in 'parking_entries_exits.csv'.")
