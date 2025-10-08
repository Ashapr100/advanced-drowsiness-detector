# Driver Drowsiness Detection System

This Python application detects driver drowsiness using real-time webcam input. It uses Eye Aspect Ratio (EAR) calculated from facial landmarks to trigger a sound alert and send an emergency email when drowsiness is detected.

## 🚀 Features
- Real-time face and eye detection using dlib's 68-point model
- EAR-based drowsiness detection
- Audio alert using pygame (cooldown-enabled)
- Emergency email notification via Gmail SMTP
- Visual warning if no face is detected

## 🧰 Tech Stack
- **Language**: Python
- **Libraries**:
  - OpenCV (`cv2`) – real-time video processing
  - dlib – facial landmark detection
  - imutils – helper functions for image resizing
  - scipy – EAR (eye aspect ratio) distance calculation
  - pygame – for playing alert sounds
  - smtplib & email – sending emergency alerts via email
  - python-dotenv – to securely store email credentials

## 📦 Requirements
```bash
pip install -r requirements.txt
```

## 🔐 Environment Setup/variables
Create a `.env` file in the root folder with:
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECEIVER_EMAIL=receiver_email@gmail.com
```
 ⚠️ Keep this file private — it's already listed in `.gitignore`. 

Use a [Gmail App Password](https://myaccount.google.com/apppasswords) if using 2-Step Verification.

## 📂 Setup Instructions

1. Download the dlib facial landmark model file:  
   👉 [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
2. Extract it and place it in your project folder.
3. Add your alert sound file as:
   ```
   alarm.wav
   ```

## ▶️ Run the Script

## 📁 Project Structure

advanced-drowsiness-detector/
├── drowsiness_detector_advanced.py
├── alarm.wav
├── requirements.txt
├── README.md
├── shape_predictor_68_face_landmarks.dat  # Too large for GitHub
├── .env         # Not uploaded to GitHub
├── .env.example # .env file to securely store email credentials/ # Template for config
├── .gitignore
├── project-output/screenshots/
│   ├── alert_triggered.png
│   └── eye_detected.png

## 👨‍💻 Author
Akash Garimella 

## 📅 Date

Nov 2023 - June 2024
