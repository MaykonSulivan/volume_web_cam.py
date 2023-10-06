import cv2
import mediapipe as mp
import numpy as np
import ctypes


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

volume = 0
min_volume = 0
max_volume = 100
step = 10


def set_system_volume(volume):
    volume = max(min(volume, max_volume), min_volume)
    ctypes.windll.user32.keybd_event(174, 0, 0, 0) 
    ctypes.windll.user32.keybd_event(174, 0, 2, 0)
    for _ in range(volume // step):
        ctypes.windll.user32.keybd_event(175, 0, 0, 0)  
        ctypes.windll.user32.keybd_event(175, 0, 2, 0)


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
        index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

        distance = np.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2)

       
        volume = int((distance / frame.shape[1]) * max_volume)

        set_system_volume(volume)

        cv2.putText(frame, f"Volume: {volume}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Volume Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
