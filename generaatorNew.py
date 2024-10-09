import csv
import random
from datetime import datetime, timedelta

# Number of days to simulate
num_days = 197
# Number of entries per day
entries_per_day = 100
# Start date for simulation
start_date = datetime(2024, 1, 1)  # Change as needed
# List of authorized vehicle numbers
authorized_vehicle_numbers = [
    "MH46X9996", "MH14EU3498", "DL3CAY9324", "MH12JC2813", "HR696969",
    "KL55R2473", "HR26CT6702", "TN52U1580", "KL16J3636", "HR26DG6167",
    "TN66U8215", "MH06AW8929", "MH02BM5048", "KL10AV6342", "DL7CN5617",
    "TN74AL5074", "MH20CS9817", "HR26BP3543", "TN38BY4191", "MH20CS4946",
    "MH20BY3665", "KL43B2344", "MH20EE7597", "HR26CM6005", "MH02CT2727",
    "MH20BG20", "HR26DG6167"
]


# Function to generate random datetime within a specific date range
def random_datetime(date):
    return datetime(date.year, date.month, date.day, random.randint(8, 18), random.randint(0, 59),
                    random.randint(0, 59))


# Function to check if the new time slot overlaps with existing slots for the given parking slot
def is_time_slot_available(slot, in_time, out_time, slot_usage):
    for existing_in_time, existing_out_time in slot_usage.get(slot, []):
        if not (out_time <= existing_in_time or in_time >= existing_out_time):
            return False
    return True


# Generate dummy data
data = []
slot_usage = {i: [] for i in range(1, 16)}  # Initialize usage dictionary for 100 slots
for i in range(num_days):
    current_date = start_date + timedelta(days=i)
    for _ in range(entries_per_day):
        vehicle_number = random.choice(authorized_vehicle_numbers)
        in_time = random_datetime(current_date)

        # Randomly decide whether out time is on the same day or different day
        if random.random() < 0.8:  # 80% chance of same day out time
            out_time = in_time + timedelta(hours=random.randint(1, 6))
        else:  # 20% chance of different day out time
            out_time = in_time + timedelta(days=random.randint(1, 3), hours=random.randint(1, 6))
        # Find a free slot
        available_slot = None
        for slot in range(1, 16):
            if is_time_slot_available(slot, in_time, out_time, slot_usage):
                available_slot = slot
                break

        # If no slots are available, skip this entry
        if available_slot is None:
            continue

        # Record the usage of the slot
        slot_usage[available_slot].append((in_time, out_time))
        # Add the data entry
        data.append([vehicle_number, in_time.strftime('%m-%d-%Y %H:%M:%S'), out_time.strftime('%m-%d-%Y %H:%M:%S'),
                     available_slot])
# Write data to CSV file
csv_filename = 'datasets/indian_vehicle_parking_data.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Vehicle Number', 'In Time', 'Out Time', 'Slot Number'])
    writer.writerows(data)
print(f"Dummy dataset for {num_days} days with different dates generated and saved to {csv_filename}.")