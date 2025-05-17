# CCTV Surveillance & Theft Detection System

A real-time CCTV surveillance system designed to monitor suspicious activities related to theft and unauthorized consumption using computer vision and pose estimation. This project leverages **MediaPipe** for pose and hand landmark detection, **OpenCV** for video capture and display, and integrates with a backend server to notify about detected threats.

---

## 🔍 Project Description

This CCTV surveillance system continuously monitors a video feed from a camera and analyzes human body and hand movements to detect suspicious behaviors such as:

- **Potential theft attempts**: Detects if a hand is near the hip with a gripping gesture, indicating possible pocket theft.
- **Unauthorized consumption**: Detects if a finger is close to the mouth, indicating possible eating or consumption within the monitored area.
  
When suspicious activity is detected, the system captures an alert frame and sends it to a backend server via a secure HTTP POST request for further action (e.g., notifications or logging).

---

## ⚙️ Features

- Real-time human pose and hand landmark detection using **MediaPipe**.
- Intelligent detection of theft-related gestures based on hand proximity to hip and finger grip.
- Detection of consumption behavior by tracking finger-to-mouth distance.
- Visual annotations on live video feed with labels indicating current status.
- Cooldown mechanism to avoid repeated alerts within a short time window.
- Automatic alert image capture and upload to a backend notification endpoint.
- Easy integration with any REST API backend for alert management.

---

## 🛠 Tech Stack

- **Python 3**
- **OpenCV** for video capturing and image processing
- **MediaPipe** for pose and hand tracking
- **NumPy** for numerical operations
- **Requests** for HTTP requests to backend server

---

## 🚀 How It Works

1. The system initializes the webcam and processes each video frame.
2. It uses MediaPipe Pose to identify body landmarks and MediaPipe Hands for hand landmarks.
3. For each detected hand, it calculates distances between the wrist and hips, and between thumb and index finger to detect gripping.
4. If gripping near the hip is detected, it marks a possible theft situation.
5. If the finger is close to the mouth, it detects consumption.
6. When suspicious activity occurs and cooldown time has passed, an alert image is saved and sent to the backend URL.
7. The live feed displays annotated landmarks and current status labels.

---

## 🔧 Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/cctv-surveillance.git
   cd cctv-surveillance

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows

3. **Install dependencies:**
   ```bash
   pip install opencv-python mediapipe numpy requests
   
4. **Configure the backend URL:**
   ```bash
   Edit the script and update the url variable to your backend notification endpoint.
   
5. **Run the surveillance system:**
   ```bash
   python surveillance.py

6. **Press 'q' to quit the live video feed.**

   ## ⚠️ Notes

- Ensure your camera is properly connected and accessible by OpenCV.
- The detection thresholds (distances, cooldown) can be adjusted in the script for your specific environment.
- The backend endpoint must be configured to accept image uploads with appropriate security measures.

---

## 🖼️ Screenshot

![Security Monitor Screenshot](https://github.com/yourusername/cctv-surveillance/blob/main/screenshot.png)

---

## 📄 License

MIT License

---

## 📞 Contact

For any questions or suggestions, please contact [Shantanu Yadav](mailto:shantanuyadavsocial@gmail.com).
