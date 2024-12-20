import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam and screen size
cam = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# Scaling factor for cursor movement
scaling_factor = 1.5  # Reduced this value for slower cursor movement


def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2)


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    frame_h, frame_w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the index finger tip (landmark 8) and thumb tip (landmark 4)
            index_finger_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Calculate the position on the screen
            screen_x = int(index_finger_tip.x * screen_w * scaling_factor)
            screen_y = int(index_finger_tip.y * screen_h * scaling_factor)

            # Ensure the cursor stays within screen bounds
            screen_x = min(max(screen_x, 0), screen_w)
            screen_y = min(max(screen_y, 0), screen_h)

            # Move the cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Check distance between thumb and index finger for click
            distance_thumb_index = calculate_distance(thumb_tip, index_finger_tip)
            if distance_thumb_index < 0.05:
                pyautogui.click()
                pyautogui.sleep(1)

            # Get the coordinates of the middle finger tip (landmark 12) and ring finger tip (landmark 16)
            middle_finger_tip = hand_landmarks.landmark[12]
            ring_finger_tip = hand_landmarks.landmark[16]

            # Check distance between middle finger and ring finger for scroll
            distance_middle_ring = calculate_distance(middle_finger_tip, ring_finger_tip)
            if distance_middle_ring < 0.05:
                pyautogui.scroll(-10)  # Scroll down
                pyautogui.sleep(1)

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
