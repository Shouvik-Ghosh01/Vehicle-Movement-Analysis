import streamlit as st
import numpy as np
import cv2
from detect import run
import re
import string
import numpy as np
import pytesseract
import csv
import os
from tensorflow.lite.python.interpreter import Interpreter
import pandas as pd
from utils import display_heading
from menu import menu

# Dictionary mapping state codes to their corresponding states in India
state_codes = {
    'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CG': 'Chhattisgarh',
    'GA': 'Goa', 'GJ': 'Gujarat', 'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JK': 'Jammu and Kashmir',
    'JH': 'Jharkhand', 'KA': 'Karnataka', 'KL': 'Kerala', 'MP': 'Madhya Pradesh', 'MH': 'Maharashtra',
    'MN': 'Manipur', 'ML': 'Meghalaya', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OD': 'Odisha', 'PB': 'Punjab',
    'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TN': 'Tamil Nadu', 'TS': 'Telangana', 'TR': 'Tripura', 'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand', 'WB': 'West Bengal', 'AN': 'Andaman and Nicobar Islands', 'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli and Daman and Diu',
    'DL': 'Delhi', 'LD': 'Lakshadweep', 'PY': 'Puducherry'
}


def clean_number_plate(text):
    # Remove special characters from the beginning and end
    cleaned_text = text.strip(string.punctuation + '~' + '|' + '!' + '-' + '_' + '(' + ')' + '{' + '}')
    # Remove special characters except for alphanumeric and spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Remove any extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    if not cleaned_text:
        return cleaned_text  # Return immediately if cleaned_text is empty

    if cleaned_text[0] == 'I':
        cleaned_text = cleaned_text[1::]
    return cleaned_text


def correct_state_code(text):
    if len(text) < 3:
        return "", text
    # Check various possible combinations for a valid state code
    possible_codes = [text[:2], text[1:3], text[0] + text[2]]
    for code in possible_codes:
        if code in state_codes:
            corrected_text = text[:2] + text[2:]  # Only replace the state code part
            return code, corrected_text
    return None, text


def analyze_number_plate(text):
    # Clean the number plate text
    cleaned_text = clean_number_plate(text)
    # Correct the state code
    state_code, corrected_text = correct_state_code(cleaned_text)
    if state_code:
        state = state_codes[state_code]
        # Remove spaces from the corrected text
        corrected_text_without_spaces = corrected_text.replace(" ", "")
        return f"The number plate belongs to {state} with the state code {state_code}.", corrected_text_without_spaces


from datetime import datetime

# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# Load the TFLite model and allocate tensors
interpreter = Interpreter(model_path='detect.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
float_input = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5
min_conf = 0.99
# Authorized vehicles dataset path
authorized_dataset_path = "datasets/authorized_vehicles.csv"
# Ensure CSV file exists
if not os.path.exists(authorized_dataset_path):
    with open(authorized_dataset_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Vehicle Number", "Date Added"])


def run(image):
    # Resize and preprocess the image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std
    # Perform inference with the TensorFlow Lite model
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    boxes = interpreter.get_tensor(output_details[1]['index'])[0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0]  # Confidence of detected objects
    detected_texts = []  # Initialize a list to store detected texts
    # Extract the bounding boxes and labels from the results
    for i in range(len(scores)):
        if ((scores[i] > 0.5) and (scores[i] <= 1.0)):  # Reduced confidence threshold to 0.5
            # Get bounding box coordinates and draw box
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            # Crop the bounding box from the image for OCR
            roi = image[ymin:ymax, xmin:xmax]
            # Preprocess for OCR: convert to grayscale and apply threshold
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi_thresh = cv2.threshold(roi_gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            # Perform OCR on the cropped image
            text = pytesseract.image_to_string(roi_thresh,
                                               config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
            text = text.strip()
            if text:
                detected_texts.append(text)  # Append detected text to the list
                print(f"OCR Detected Text: {text}")  # Debugging: print detected text
    if not detected_texts:
        print("No valid vehicle number detected.")  # Debugging: no detections
    return detected_texts


def add_to_authorized_dataset(vehicle_number):
    """
    Adds a vehicle number to the authorized dataset.
    Parameters:
    vehicle_number (str): Detected vehicle number.
    """
    # Add to CSV without the date
    with open(authorized_dataset_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([vehicle_number])
    print(f"Vehicle Number '{vehicle_number}' has been added to the authorized dataset.\n")


def capture_and_process(image_path):
    """
    Processes an image, detects vehicle number plate, and adds the result to the authorized dataset.
    Parameters:
    image_path (str): Path to the image file.
    """
    # Load the image from the specified file path
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return
    # Pass the image to the model to get the detection result
    detected_texts = run(image)
    if detected_texts:
        for text in detected_texts:
            print(f"Detected Vehicle Number: {text}")
            add_to_authorized_dataset(text)