import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import pygame
import time

# Initialize pygame and load sound once
pygame.mixer.init()
alert_sound = pygame.mixer.Sound("C:/Users/user/Downloads/alarm.wav")  # Replace with your actual path

# Email setup (secure in production with environment variables)
sender_email = "akashgarimella11@gmail.com"
receiver_email = "akashgarimella04@gmail.com"
password = "ratt fltl qvhb eejs"  # Use an app password if 2FA is enabled

def send_email():
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Emergency: Drowsiness Alert"
    msg.attach(MIMEText("The driver appears to be drowsy or unresponsive.", 'plain'))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("📧 Emergency email sent.")
    except Exception as e:
        print(f"Email failed: {e}")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Thresholds and counters
EAR_THRESHOLD = 0.25
SOUND_FRAMES = 20
EMAIL_FRAMES = 150
sound_counter = 0
email_counter = 0
sound_playing = False
last_sound_time = 0
COOLDOWN_SECONDS = 5  # Wait time before alarm can restart

# Initialize Dlib's face detector
predictor_path = "C:/Users/user/Downloads/shape_predictor_68_face_landmarks.dat"
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor(predictor_path)
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

cap = cv2.VideoCapture(0)
print("👁️ Drowsiness Detector running. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect(gray, 0)
    eyes_detected = False
    current_time = time.time()

    for face in faces:
        shape = predict(gray, face)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

        if ear < EAR_THRESHOLD:
            sound_counter += 1
            email_counter += 1

            if sound_counter >= SOUND_FRAMES and not sound_playing:
                if current_time - last_sound_time > COOLDOWN_SECONDS:
                    alert_sound.play(-1)
                    sound_playing = True
                    last_sound_time = current_time
                    print("🔊 Alert sound triggered.")

            if email_counter >= EMAIL_FRAMES:
                send_email()
                email_counter = 0
        else:
            sound_counter = 0
            email_counter = 0
            if sound_playing:
                alert_sound.stop()
                sound_playing = False
                print("🔇 Alert sound stopped.")

        eyes_detected = True

    if not eyes_detected:
        cv2.putText(frame, "No eyes detected. Adjust your face position.",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    frame = cv2.flip(frame, 1)
    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting system...")
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()