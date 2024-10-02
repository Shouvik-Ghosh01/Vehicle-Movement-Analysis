import numpy as np
import csv
import cv2
import os
import pandas as pd
import sys
import glob
import random
import importlib.util
from datetime import datetime
import pytesseract
from tensorflow.lite.python.interpreter import Interpreter

import matplotlib
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'

interpreter = Interpreter(model_path='detect.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

float_input = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

def run(image):
    """
    Predicts and plots the bounding boxes on the given image using the trained TensorFlow Lite model.
    Also performs OCR on the detected bounding boxes to extract text.

    Parameters:
    image (ndarray): Image array in BGR format (OpenCV).

    Returns:
    tuple: A tuple containing the processed image and a list of detected texts.
    """

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
        if ((scores[i] > min_conf) and (scores[i] <= 1.0)):
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            # Crop the bounding box from the image for OCR
            roi = image[ymin:ymax, xmin:xmax]

            # Perform OCR on the cropped image
            text = pytesseract.image_to_string(roi, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
            detected_texts.append(text)  # Append detected text to the list

    return image, detected_texts