import numpy as np
import mediapipe as mp
import cv2
import math
from constants import *

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def draw_debug_lines(image, frame_width, frame_height):

    top_initial_point = np.array([int(frame_width * inital_porcentage), int(frame_height * inital_porcentage)])

    bottom_final_point= np.array([int(frame_width * final_porcentage), int(frame_height * final_porcentage)])

    image = cv2.rectangle(image, top_initial_point, bottom_final_point, blue, 1, default_line)

# this function return the distance based in two points
def euclidean_distance(point1, point2):
    # ravel() returns 1D array with all the input-array elements
    x1, y1 =point1.ravel()
    x2, y2 =point2.ravel()
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

# this function returns the distance between the top and bottom points normalized
def normalize_distance(top_point, bottom_point):
    min_value = 15.0
    max_value = 100.0
    total_distance = euclidean_distance(top_point, bottom_point)

    normalized_distance = (total_distance - min_value) / (max_value - min_value)
    
    return normalized_distance

def draw_hands(image, mesh_points, landmark_results):
    # draw lines in index and thumb fingers
    image = cv2.line(image, mesh_points[THUMB_TIP], mesh_points[THUMB_IP], pink, 14, default_line)
    image = cv2.line(image, mesh_points[INDEX_FINGER_TIP], mesh_points[INDEX_FINGER_DIP], pink, 14, default_line)

    # draw the lines and circles based in all hand landmarks
    for _, hand in enumerate(landmark_results):
        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=pink, thickness=default_thickness, circle_radius=2),
                                mp_drawing.DrawingSpec(color=white, thickness=default_thickness, circle_radius=2),
                                    )

    return image

def draw_score(image, counter):
    image = cv2.putText(image,f"Score: {counter}", (10,60), cv2.FONT_ITALIC, font_size, green, default_thickness, default_line)
    
    return image

def draw_close_button(image, frame_height, frame_width, close_button, finger_position, cap):
    x_pos = finger_position[0]
    y_pos = finger_position[1]

    x_initial = int(frame_width * 0.9)
    X_final = int(frame_width * 0.95)

    y_initial = int(frame_height * 0.06)
    y_final = int(frame_height * 0.12)

    x_text = int(frame_width * 0.918)
    y_text = int(frame_height * 0.1)

    # if the index finger is inside of close button, the window would be closed
    if(x_pos > x_initial and x_pos < X_final):
        if(y_pos > y_initial and y_pos < y_final):
            close_button = -1
            cap.release()

    top_initial_point = np.array([x_initial, y_initial])

    bottom_final_point= np.array([X_final, y_final])

    textfinal_point= np.array([x_text, y_text])

    # draw the X inside the button
    image = cv2.putText(image,"X", textfinal_point, font_family, font_size, black, default_thickness, default_line)
    # draw the close button lines
    image = cv2.rectangle(image,top_initial_point , bottom_final_point, red, close_button, default_line)

    return image