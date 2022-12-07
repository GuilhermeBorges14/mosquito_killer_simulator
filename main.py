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

    # mediapipe Hands model
    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 

        while cap.isOpened():

            # set the name of window
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            # fills the window with the size of the screen
            cv2.setWindowProperty(window_name, cv2.WND_PROP_ASPECT_RATIO , cv2.WINDOW_NORMAL)

            # get the frame of the camera capture
            _, frame = cap.read()
            
            # flip() method is used to flip(reverse) a 2D array, to make a "mirror effect". 
            image = cv2.flip(frame, 1)            

            # shape() function returns the dimensions of a given image like the height, width and number of channels in the image
            # the "[:2]" expression is called slicing, and in this case, get oly the 2 first elements from array
            frame_height, frame_width = image.shape[:2]

            # process the image
            results = hands.process(image)

            draw_debug_lines(image, frame_width, frame_height)

            mosquito_array = create_mosquito(mosquito_array, number_of_mosquitos, initial_mosquito_axes_value,initial_mosquito_axes_value)

            mosquito_array, image = draw_mosquito(mosquito_array,image, frame_width, frame_height)

            if results.multi_hand_landmarks:

                # here, we multiply the x axis per image width and y axis per image height
                mesh_points=np.array([np.multiply([p.x, p.y], [frame_width, frame_height]).astype(int) for p in results.multi_hand_landmarks[0].landmark])

                distance = normalize_distance(mesh_points[INDEX_FINGER_TIP], mesh_points[THUMB_TIP])

                mosquito_array, counter = kill_mosquito(mosquito_array, counter,  distance, mesh_points[INDEX_FINGER_TIP][0], mesh_points[THUMB_IP][0], mesh_points[INDEX_FINGER_TIP][1], mesh_points[THUMB_IP][1])
                
                image = draw_hands(image, mesh_points, results.multi_hand_landmarks)

                image = draw_close_button(image, frame_height, frame_width, close_button, mesh_points[INDEX_FINGER_TIP], cap)

            image = draw_score(image, counter)

            # imshow() method is used to display an image in a window
            cv2.imshow(window_name, image)

            # waitkey() method allows users to display a window for given milliseconds or until any key is pressed
            if cv2.waitKey(10) & 0xFF == ord(close_key):
                break

show_frame()

# closes video file or capturing device
cap.release()

# destroys all the windows we created
cv2.destroyAllWindows()
