import cv2

THUMB_IP = 3
THUMB_TIP = 4
INDEX_FINGER_DIP = 7
INDEX_FINGER_TIP = 8

window_name = 'Hand Tracking'

close_key = 'q'

number_of_mosquitos = 3

low_random_number = -10
high_random_number = 15

initial_mosquito_axes_value = 0

close_finger_value = 0.22

inital_porcentage = 0.15
final_porcentage = 0.85

blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
black = (0,0,0)
pink = (255,0,255)
white = (255,255,255)

font_family = cv2.FONT_ITALIC
font_size = 0.6

default_line = cv2.LINE_AA
default_thickness = 1

resize_mosquito = 44
