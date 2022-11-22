import numpy as np
import cv2
from mosquito import *
from constants import *

def add_mask(x, y, original_image, img_overlay, alpha_mask):

    mask = np.zeros(original_image.shape, np.uint8)
    inverted_mask = np.ones(original_image.shape, np.uint8)

    alpha_image = alpha_mask / 255.0
    inverted_alpha_image = 1.0 - alpha_image

    y_initial, y_final =  y - int(img_overlay.shape[0] / 2) , y + int(img_overlay.shape[0] / 2) 
    x_initial, x_final =  x - int(img_overlay.shape[1] / 2) ,  x + int(img_overlay.shape[1] / 2) 

    if(y_final >= original_image.shape[0] or x_final >= original_image.shape[1] or x == 0  or y == 0):
        return original_image

    mask[y_initial:y_final, x_initial:x_final, :] = img_overlay

    inverted_mask[y_initial:y_final, x_initial:x_final, :] = inverted_alpha_image

    # here, we multiply the values of original image per inverted alpha mask values
    # to remove mosquito space
    original = original_image * inverted_mask

    # here, we sum the images to add mask with mosquito image in original image
    sum_images = original + mask

    # here, we converted to uint8
    final_image = np.uint8(sum_images)

    return final_image

def create_mosquito(mosquito_array, number, x_axes, y_axes):

    if(mosquito_array.size < number):

        for num in range(number):
            new_mosquito = Mosquito(f"mosquito_{num}", x_axes, y_axes)
            if(mosquito_array.size < number):
                mosquito_array = np.append(mosquito_array, new_mosquito)

    return mosquito_array

def mosquito_movement(mosquito_array, frame_width, frame_height):

    if(mosquito_array.size > 0):
        for num in range(mosquito_array.size):
            if(mosquito_array[num].y_axes == 0 and mosquito_array[num].x_axes == 0):
                mosquito_array[num].y_axes = np.random.randint(frame_width * inital_porcentage, frame_width * final_porcentage)
                mosquito_array[num].x_axes = np.random.randint(frame_height * inital_porcentage, frame_height * final_porcentage)
            elif(mosquito_array[num].x_axes > frame_width * final_porcentage or mosquito_array[num].x_axes < frame_width * inital_porcentage or mosquito_array[num].y_axes > frame_height * final_porcentage or mosquito_array[num].y_axes < frame_height * inital_porcentage):
                mosquito_array = np.delete(mosquito_array, num)
                break
            else:
                mosquito_array[num].x_axes += np.random.randint(low_random_number, high_random_number)
                mosquito_array[num].y_axes += np.random.randint(low_random_number, high_random_number)

    return mosquito_array

def draw_mosquito(mosquito_array, image, frame_width, frame_height):
    mosquito_image = cv2.imread('assets/mosquito.jpg')
    alpha_image = cv2.imread('assets/alpha.jpg')

    mosquito_image = cv2.resize(mosquito_image, (resize_mosquito,resize_mosquito))
    alpha_image = cv2.resize(alpha_image, (resize_mosquito,resize_mosquito))
    
    mosquito_array = mosquito_movement(mosquito_array, frame_width, frame_height)
                
    if(mosquito_array.size > 0):
        for num in range(mosquito_array.size):
            
            mosquito_position = np.array([mosquito_array[num].x_axes, mosquito_array[num].y_axes])

            x = mosquito_position[0]
            y = mosquito_position[1]

            final_image = add_mask(x, y, image, mosquito_image, alpha_image)

            image = final_image 
    
    return mosquito_array, image

    
def kill_mosquito(mosquito_array, counter, distance, x_initial, x_final, y_initial, y_final):

    for num in range(mosquito_array.size):
        if(mosquito_array[num].x_axes >= x_initial and mosquito_array[num].x_axes <=x_final):
            if(mosquito_array[num].y_axes >= y_initial and mosquito_array[num].y_axes <= y_final):
                if(distance <= close_finger_value):
                    mosquito_array = np.delete(mosquito_array, num)
                    counter += 1
                    break

    return mosquito_array, counter


