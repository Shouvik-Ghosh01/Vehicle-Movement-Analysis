import cv2
import numpy as np
import pytesseract
import csv
import os
from tensorflow.lite.python.interpreter import Interpreter
import pandas as pd
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
            text = pytesseract.image_to_string(roi_thresh, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
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
    else:
        print("No vehicle number detected.")

    # Display the processed image with bounding boxes
    cv2.imshow('Vehicle Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Replace with the actual image path
    image_path = 'datasets/pic1.webp'
    capture_and_process(image_path)
