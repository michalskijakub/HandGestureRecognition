import mediapipe as mp
import cv2
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def process_frame(frame, hands):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    gesture_message = "Brak gestu"
    detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and \
               hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and \
               hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and \
               hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                detected = True

                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x and \
                   hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x and \
                   hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x:
                    gesture_message = "Wykryto gest: Kciuk skierowany w prawo"
                elif hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x and \
                     hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x and \
                     hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x:
                    gesture_message = "Wykryto gest: Kciuk skierowany w lewo"

    return frame, gesture_message, detected

mode = input('Wybierz tryb pracy: z - zdjecie, k - kamera:  ')

if mode == 'k':
    cap = cv2.VideoCapture(0)
    last_gesture_time = None
    last_gesture = None
    current_gesture = None
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Nie można odczytać klatki z kamery.")
                break

            frame, gesture_message, detected = process_frame(frame, hands)
            if detected:
                if last_gesture != gesture_message:
                    last_gesture_time = time.time()
                    last_gesture = gesture_message
                elif time.time() - last_gesture_time >= 2 and last_gesture == gesture_message:
                     if current_gesture != gesture_message and (gesture_message == "Wykryto gest: Kciuk skierowany w prawo" or gesture_message == "Wykryto gest: Kciuk skierowany w lewo"):
                        print(gesture_message)
                        current_gesture = gesture_message
            else:
                last_gesture = None
                current_gesture = None

            cv2.imshow('Hand Gestures Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()

elif mode == 'z':
    numer = 0
    ran = 24
    for i in range(ran):
        numer += 1
        img_path = ADD YOUR IMG PATH'
        print(numer)
        frame = cv2.imread(img_path)
        if frame is None:
            print("Nie można załadować zdjęcia.")
            continue
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            frame, gesture_message, detected = process_frame(frame, hands)
            print(gesture_message)
            
            cv2.imshow('Hand Gestures Recognition', frame)
            cv2.waitKey(0)

cv2.destroyAllWindows()
