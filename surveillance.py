import cv2
import mediapipe as mp
import numpy as np
import requests
import time

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

url = "${BACKEND_URL}/notifythreat"
# 
COOLDOWN_SECONDS = 10
last_alert_time = 0

previous_theft_possible = False
current_theft_possible = False

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    current_time = time.time()


    pose_results = pose.process(rgb_frame)
    hands_results = hands.process(rgb_frame)

    alert_triggered = False
    label = "Normal"
    color = (0, 0, 255) 
    current_hands_detected = hands_results.multi_hand_landmarks is not None


    left_hip = right_hip = None

    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
    
        left_hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w),
                    int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h))
        right_hip = (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * w),
                     int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * h))


    current_theft_possible = False
    if hands_results.multi_hand_landmarks and left_hip and right_hip:
        for hand_landmarks in hands_results.multi_hand_landmarks:
        
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            wrist_pos = (int(wrist.x * w), int(wrist.y * h))
            
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            grip_distance = np.linalg.norm(np.array([thumb.x, thumb.y]) - 
                            np.array([index.x, index.y])) * w

        
            dist_left = np.linalg.norm(np.array(wrist_pos) - np.array(left_hip))
            dist_right = np.linalg.norm(np.array(wrist_pos) - np.array(right_hip))
            min_dist = min(dist_left, dist_right)

            if min_dist < 50 and grip_distance < 30:
                current_theft_possible = True
                break


    if previous_theft_possible and not current_hands_detected:
        if (current_time - last_alert_time) > COOLDOWN_SECONDS:
            label = "Suspecious: Theft Detected!"
            color = (0, 165, 255) 
            alert_triggered = True


    if hands_results.multi_hand_landmarks and pose_results.pose_landmarks:
        mouth = (int(landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].x * w),
                 int(landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y * h))
        
        for hand_landmarks in hands_results.multi_hand_landmarks:
            index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pos = (int(index.x * w), int(index.y * h))
            distance = np.linalg.norm(np.array(index_pos) - np.array(mouth))
            
            if distance < 30:
                label = "Consuming"
                color = (0, 255, 0) 
                alert_triggered = True
                break


    previous_theft_possible = current_theft_possible


    if alert_triggered and (current_time - last_alert_time) > COOLDOWN_SECONDS:
    
        resized_frame = cv2.resize(frame, (320, 240))
        cv2.imwrite("alert.jpg", resized_frame)
        
    
        with open("alert.jpg", "rb") as f:
            files = {"file": f}
            data = {"description": f"Alert: {label}"}
            try:
                response = requests.post(url, files=files, data=data, timeout=5)
                print(f"Alert sent: {response.status_code}")
                last_alert_time = current_time
            except Exception as e:
                print(f"Alert failed: {str(e)}")


    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if hands_results.multi_hand_landmarks:
        for hand in hands_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)


    cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Security Monitor", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
