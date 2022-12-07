import mediapipe as mp
import cv2
import numpy as np
from mosquito import *
from utils import *
from mosquito_actions import *
from constants import *

mp_hands = mp.solutions.hands

# global vars
cap = cv2.VideoCapture(0)

close_button = 1

counter = 0

mosquito_array = np.array([])


def show_frame():
    global mosquito_array, counter, close_button

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 

        while cap.isOpened():

            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_ASPECT_RATIO , cv2.WINDOW_NORMAL)

            _, frame = cap.read()
            
            image = cv2.flip(frame, 1)            

            frame_height, frame_width = image.shape[:2]

            results = hands.process(image)

            draw_debug_lines(image, frame_width, frame_height)

            mosquito_array = create_mosquito(mosquito_array, number_of_mosquitos, initial_mosquito_axes_value,initial_mosquito_axes_value)

            mosquito_array, image = draw_mosquito(mosquito_array,image, frame_width, frame_height)

            if results.multi_hand_landmarks:
                mesh_points=np.array([np.multiply([p.x, p.y], [frame_width, frame_height]).astype(int) for p in results.multi_hand_landmarks[0].landmark])

                distance = normalize_distance(mesh_points[INDEX_FINGER_TIP], mesh_points[THUMB_TIP])

                mosquito_array, counter = kill_mosquito(mosquito_array, counter,  distance, mesh_points[INDEX_FINGER_TIP][0], mesh_points[THUMB_IP][0], mesh_points[INDEX_FINGER_TIP][1], mesh_points[THUMB_IP][1])
                
                image = draw_hands(image, mesh_points, results.multi_hand_landmarks)

                image = draw_close_button(image, frame_height, frame_width, close_button, mesh_points[INDEX_FINGER_TIP], cap)

            image = draw_score(image, counter)

            cv2.imshow(window_name, image)

            if cv2.waitKey(10) & 0xFF == ord(close_key):
                break

show_frame()

cap.release()
cv2.destroyAllWindows()
