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

def calculate_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2)

def is_finger_straight(hand_landmarks, finger_tip_idx, finger_pip_idx):
    finger_tip = hand_landmarks.landmark[finger_tip_idx]
    finger_pip = hand_landmarks.landmark[finger_pip_idx]
    return finger_tip.y < finger_pip.y  # Straight if the tip is higher than the PIP joint

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
            middle_finger_tip = hand_landmarks.landmark[12]
            ring_finger_tip = hand_landmarks.landmark[16]
            pinky_finger_tip = hand_landmarks.landmark[20]

            index_finger_pip = hand_landmarks.landmark[6]
            middle_finger_pip = hand_landmarks.landmark[10]
            ring_finger_pip = hand_landmarks.landmark[14]
            pinky_finger_pip = hand_landmarks.landmark[18]

            # Calculate the position on the screen
            screen_x = int(index_finger_tip.x * screen_w * 2)  # Speed up cursor movement
            screen_y = int(index_finger_tip.y * screen_h * 2)  # Speed up cursor movement

            # Ensure the cursor stays within screen bounds
            screen_x = min(max(screen_x, 0), screen_w)
            screen_y = min(max(screen_y, 0), screen_h)

            # Move the mouse cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate the distance between the index finger tip and thumb tip
            distance_thumb_index = calculate_distance(index_finger_tip, thumb_tip)

            # Trigger a mouse click if the distance is below a certain threshold
            if distance_thumb_index < 0.1:  # Adjust the threshold as needed
                pyautogui.click()
                pyautogui.sleep(1)  # Prevent multiple clicks in a short period

            # Check the states of the fingers
            index_straight = is_finger_straight(hand_landmarks, 8, 6)
            middle_straight = is_finger_straight(hand_landmarks, 12, 10)
            ring_straight = is_finger_straight(hand_landmarks, 16, 14)
            pinky_straight = is_finger_straight(hand_landmarks, 20, 18)

            # Scroll based on the number of straight fingers
            if index_straight and middle_straight and ring_straight and not pinky_straight:
                pyautogui.scroll(10)  # Scroll up
            elif index_straight and middle_straight and not ring_straight and not pinky_straight:
                pyautogui.scroll(-10)  # Scroll down

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
