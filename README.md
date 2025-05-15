# AI-Enchaned-Pothole-Detection-System
AI-Powered Real-Time Pothole Detection System

An embedded computer vision system for detecting and classifying potholes using YOLOv8 and GPS logging.

Table of Contents
	•	Overview
	•	Features
	•	System Architecture
	•	Requirements
	•	Installation
	•	How to Use
	•	Dataset
	•	Training
	•	Results
	•	Contributors
	•	License

⸻

Overview

This project presents a low-cost, real-time pothole detection system based on the YOLOv8 deep learning model and NEO-6M GPS logging. It identifies potholes and road defects such as cracks and raveling, classifies them by severity, and records their GPS coordinates for maintenance planning or alerting drivers.

Tested on a Raspberry Pi 4, it operates with a USB camera and a GPS module in edge environments, designed for smart city and road safety applications.

⸻

Features
	•	Real-time object detection using YOLOv8
	•	Supports detection of 5 defect classes:
	•	Pothole
	•	Longitudinal Cracking
	•	Transverse Cracking
	•	Alligator Cracking
	•	Raveling
	•	GPS-based location tagging using NEO-6M via Arduino Nano
	•	Tkinter-based GUI with detection logs and preview
	•	Excel logging with embedded images and GPS data
	•	Compatible with webcam, IP camera, or video file input

⸻

System Architecture
	•	Camera Input → YOLOv8 → Detection & Classification
	•	GPS Module (NEO-6M) → Arduino → Raspberry Pi
	•	YOLO Inference + Data Logging → GUI & Excel Output

⸻

Requirements
	•	Python 3.8+
	•	Raspberry Pi 4 / PC with OpenCV-compatible camera
	•	Libraries:
	•	ultralytics, opencv-python, pillow, openpyxl, pyserial, tkinter, pandas
⸻

How to Use
	1.	Connect GPS module via Arduino (TX/RX to USB Serial).
	2.	Run the main interface:

python pothole_detector_app.py


	3.	Load a YOLOv8 model (trained .pt file).
	4.	Choose input (Camera, Video, or Image).
	5.	Start detection and view results in real time.
	6.	Detected defects will be logged with images and GPS in Excel.

⸻

Dataset
	•	Uses a custom dataset with 5 labeled road damage classes.
	•	Structure defined in data.yaml:

nc: 5
names: ['Pothole', 'Longitudinal Cracking', 'Transverse Cracking', 'Alligator Cracking', 'Raveling']



⸻

Training

To retrain or fine-tune your model:

from ultralytics import YOLO
model = YOLO('path/to/your_model.pt')
model.train(data='data.yaml', epochs=59, imgsz=640, batch=4, device='cpu')


⸻

Results
	•	Accuracy: 89% True Positives
	•	GPS Accuracy: ±2.5 meters
	•	Real-Time Performance: ~15–20 FPS on Raspberry Pi
	•	Logging: Excel with timestamp, GPS, class, confidence, image

⸻

Contributors
	•	Fatimaalzahraa Mohamed
Supervisor: Dr. Khaled Elgeneidy
[Faculty of Engineering, Civil Dept.]

⸻
