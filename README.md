## Vehicle Movement Analysis and Insight Generation in a College Campus using Edge AI

Project Overview

This project aims to develop an Edge AI solution for analyzing vehicle movement in a college campus. The solution leverages cameras capturing vehicle photos and license plates to provide insights on:

Vehicle Movement Patterns: Analyze frequency and timing of vehicle entries/exits, identifying peak times and patterns.
Parking Occupancy: Monitor parking lot occupancy in real-time, highlighting frequently occupied lots and their usage patterns.
Vehicle Matching: Match captured vehicles to an approved database to identify unauthorized vehicles.
Benefits:

Improved campus security by identifying unauthorized vehicles.
Enhanced management of parking resources through real-time occupancy monitoring.
Data-driven insights for optimizing traffic flow and parking allocation.
Technical Approach

The project leverages the following technologies:

TensorFlow: A popular deep learning framework used for object detection in this project.
Tesseract OCR: An open-source optical character recognition (OCR) engine used for license plate recognition.
OpenCV: A computer vision library used for image processing tasks like resizing and grayscale conversion.
Matplotlib & Seaborn: Data visualization libraries used for exploratory data analysis (EDA).
TensorFlow Lite/OpenVINO (Optional): Frameworks for deploying the AI model on edge devices for real-time inference.
Project Structure

The project follows a step-by-step approach:

Load Dataset: Load image data (vehicles, license plates) and timestamps using Python and OpenCV.
Data Preprocessing: Preprocess images using OpenCV and tools like Pandas and NumPy for tasks like resizing, grayscale conversion, and handling missing values.
Exploratory Data Analysis (EDA): Utilize Matplotlib and Seaborn to visualize vehicle entry/exit times and parking occupancy trends.
Vehicle Matching: Implement vehicle matching using OpenCV for license plate recognition with Tesseract OCR and compare results against an approved vehicle database.
Insight Generation: Generate insights on movement patterns and parking data using Pandas and Matplotlib.
Scalable Deployment (Optional): Explore deploying the AI model on edge devices for real-time processing using TensorFlow Lite or OpenVINO (for future implementation).
