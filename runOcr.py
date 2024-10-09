import numpy as np
import csv
import cv2
import os
import pandas as pd
import sys
import glob
import cvzone
import random
import importlib.util
from datetime import datetime
import pytesseract
from tensorflow.lite.python.interpreter import Interpreter

import matplotlib
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'

modelpath = 'detect.tflite'
lblpath = 'labelmap.txt'
min_conf = 0.99
cap = cv2.VideoCapture('datasets/demo.mp4')

interpreter = Interpreter(model_path=modelpath)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

float_input = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

list1 = []
processed_numbers = set()

with open("datasets/car_plate_data.csv", "a", newline='') as csvfile:


    csvfile.seek(0, 2)
    if csvfile.tell() == 0:
        writer = csv.writer(csvfile)
        writer.writerow(["NumberPlate", "Timestamp"])

with open(lblpath, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

while (True):
    ret, frame = cap.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imH, imW, _ = frame.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std


    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    classes = interpreter.get_tensor(output_details[3]['index'])[0]
    scores = interpreter.get_tensor(output_details[0]['index'])[0]

    detections = []

    for i in range(len(scores)):
        if ((scores[i] > min_conf) and (scores[i] <= 1.0)):

            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW))+25)
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),(xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),2)  # Draw label text
            detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])

            crop = frame[ymin:ymax, xmin:xmax]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 10, 20, 20)

            text = pytesseract.image_to_string(gray).strip()
            text = text.replace('(', '').replace(')', '').replace(',', '').replace(']', '')
            print(text)

            if text not in processed_numbers:
                processed_numbers.add(text)
                list1.append(text)
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Open the CSV file in append mode
                with open("datasets/car_plate_data.csv", "a", newline='') as csvfile:

                    writer = csv.writer(csvfile)

                    writer.writerow([text, current_datetime])

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
                cv2.imshow('crop', crop)

    cv2.imshow('output', frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()