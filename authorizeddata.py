import random
import csv

def generate_approved_vehicle_database(num_vehicles):
  """
  This function generates a sample approved vehicle database with license plates and additional information.

  Args:
      num_vehicles (int): The number of vehicles to generate entries for.

  Returns:
      dict: A dictionary containing the approved vehicle database.
  """
  parking_lots = ["A", "B", "C", "D", "Visitor"]  # Sample parking lot areas
  vehicle_types = ["Car", "Truck", "Motorcycle"]  # Sample vehicle types
  permit_types = ["Student", "Staff", "Faculty", "Visitor"]  # Sample permit types

  database = {}

  for i in range(num_vehicles):
    # Generate random license plate (replace with desired format)
    license_plate = f"ABC{i:03d}"  # Example format with leading zeros

    # Randomly assign parking lot, vehicle type, and permit type
    parking_lot = parking_lots[random.randint(0, len(parking_lots)-1)]
    vehicle_type = vehicle_types[random.randint(0, len(vehicle_types)-1)]
    permit_type = permit_types[random.randint(0, len(permit_types)-1)]

    # Create a dictionary entry with additional information, including license plate
    vehicle_data = {
      "NumberPlate": license_plate,
      "Parking Lot": parking_lot,
      "Vehicle Type": vehicle_type,
      "Permit Type": permit_type
    }

    database[license_plate] = vehicle_data

  return database

def save_to_csv(data, filename):
  """
  This function saves the provided data dictionary to a CSV file, including the license plate.

  Args:
      data (dict): The data dictionary to be saved.
      filename (str): The desired filename for the CSV file.
  """
  # Get field names from the dictionary structure
  fieldnames = list(data.values())[0].keys()

  # Open the CSV file for writing
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write each data entry as a row in the CSV file, including the license plate
    for license_plate, vehicle_data in data.items():
      # Combine license plate with other data before writing
      combined_data = {"NumberPlate": license_plate}
      combined_data.update(vehicle_data)  # Update with remaining data
      writer.writerow(combined_data)

# Example usage with 200 vehicles
approved_vehicles = generate_approved_vehicle_database(200)

# Save the data with license plate to a CSV file named "approved_vehicles.csv"
save_to_csv(approved_vehicles, "approved_vehicles.csv")

print("Approved vehicle database saved to approved_vehicles.csv")
