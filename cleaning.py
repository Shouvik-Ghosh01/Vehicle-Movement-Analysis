import pandas as pd


def read_csv_with_encoding_test(filename):
  """
  Attempts to read a CSV file using different encodings to handle potential encoding issues.

  Args:
      filename (str): The name of the CSV file to read.

  Returns:
      pandas.DataFrame: The DataFrame containing the data from the CSV file,
                         or None if reading fails with all attempted encodings.
  """
  encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
  for encoding in encodings:
    try:
      df = pd.read_csv(filename, encoding=encoding)
      return df
    except UnicodeDecodeError:
      pass  # Continue trying other encodings

  print(f"Failed to read CSV '{filename}' with any of the attempted encodings: {encodings}")
  return None


def clean_car_plate_data(filename):
  """
  Reads a CSV file using different encodings, filters rows with missing timestamps or
  number plates less than 5 characters, and saves the cleaned data to a new CSV file.

  Args:
      filename (str): The name of the CSV file to read.

  Returns:
      None
  """

  try:
    # Read the CSV data using different encodings
    df = read_csv_with_encoding_test(filename)

    if df is not None:
      # Filter rows with conditions
      df_filtered = df[(df['Timestamp'].notna()) & (df['NumberPlate'].str.len() >= 5)]

      # Save the cleaned DataFrame to a new CSV file
      df_filtered.to_csv("car_plate_data_cleaned.csv", index=False)
      print("Car plate data cleaned and saved to 'car_plate_data_cleaned.csv'.")

  except FileNotFoundError:
    print(f"Error: CSV file '{filename}' not found. Please check the file path.")
  except pd.errors.EmptyDataError:
    print(f"Error: CSV file '{filename}' is empty. No data to clean.")


# Specify your CSV file name
csv_file = "car_plate_data.csv"
clean_car_plate_data(csv_file)
