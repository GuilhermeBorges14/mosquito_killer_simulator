import numpy as np
import cv2
from mosquito import *
from constants import *

# this function add a mask with mosquito image above the frame image
def add_mask(x, y, original_image, img_overlay, alpha_mask):

    # array filled with zeros
    mask = np.zeros(original_image.shape, np.uint8)

    # array filled with ones
    inverted_mask = np.ones(original_image.shape, np.uint8)

    # divide by 255 to get colors in the range of 0 and 1
    # in this case, to transform the (255,255,255) values (white color) to (1,1,1)
    alpha_image = alpha_mask / 255.0

    # invert the alpha image. Where was 1 is 0, and where was 0 now is 1
    inverted_alpha_image = 1.0 - alpha_image

    # get the mosquito position in the screen
    y_initial, y_final =  y - int(img_overlay.shape[0] / 2) , y + int(img_overlay.shape[0] / 2) 
    x_initial, x_final =  x - int(img_overlay.shape[1] / 2) ,  x + int(img_overlay.shape[1] / 2) 

    if(y_final >= original_image.shape[0] or x_final >= original_image.shape[1] or x == 0  or y == 0):
        return original_image

    # add the mosquito image in mask (zeros mask)
    mask[y_initial:y_final, x_initial:x_final, :] = img_overlay

    # add the mosquito inverted alpha image (mosquito filled with black color) in inverted mask (ones mask)
    inverted_mask[y_initial:y_final, x_initial:x_final, :] = inverted_alpha_image

    # here, we multiply the values of original image per inverted alpha mask values
    # to remove mosquito space
    original = original_image * inverted_mask

    # here, we sum the images to add mask with mosquito image in original image
    sum_images = original + mask

    # here, we converted to uint8
    final_image = np.uint8(sum_images)

    return final_image

# this function creates a mosquito
def create_mosquito(mosquito_array, number, x_axes, y_axes):

    if(mosquito_array.size < number):

        for num in range(number):
            new_mosquito = Mosquito(f"mosquito_{num}", x_axes, y_axes)
            if(mosquito_array.size < number):
                mosquito_array = np.append(mosquito_array, new_mosquito)

    return mosquito_array

# this function makes a mosquito movement
def mosquito_movement(mosquito_array, frame_width, frame_height):

    if(mosquito_array.size > 0):
        for num in range(mosquito_array.size):
            if(mosquito_array[num].y_axes == 0 and mosquito_array[num].x_axes == 0):
                # when mosquito object is created, give the first random number for position
                mosquito_array[num].y_axes = np.random.randint(frame_width * inital_porcentage, frame_width * final_porcentage)
                mosquito_array[num].x_axes = np.random.randint(frame_height * inital_porcentage, frame_height * final_porcentage)
            elif(mosquito_array[num].x_axes > frame_width * final_porcentage or mosquito_array[num].x_axes < frame_width * inital_porcentage or mosquito_array[num].y_axes > frame_height * final_porcentage or mosquito_array[num].y_axes < frame_height * inital_porcentage):
                # if mosquito get out of this values (the blue rectangle), he's removed from array
                mosquito_array = np.delete(mosquito_array, num)
                break
            else:
                # give the "mosquito random movement" for an alredy created mosquito
                mosquito_array[num].x_axes += np.random.randint(low_random_number, high_random_number)
                mosquito_array[num].y_axes += np.random.randint(low_random_number, high_random_number)

    return mosquito_array

# this function draws mosquito in the screen
def draw_mosquito(mosquito_array, image, frame_width, frame_height):
    # get the mosquito image
    mosquito_image = cv2.imread('assets/mosquito.jpg')
    # get the mosquito alpha image
    alpha_image = cv2.imread('assets/alpha.jpg')

    # resize the size os images
    mosquito_image = cv2.resize(mosquito_image, (resize_mosquito,resize_mosquito))
    alpha_image = cv2.resize(alpha_image, (resize_mosquito,resize_mosquito))
    
    mosquito_array = mosquito_movement(mosquito_array, frame_width, frame_height)
                
    if(mosquito_array.size > 0):
        for num in range(mosquito_array.size):
            
            # get the mosquito axis (x and y) to use in add_mask function
            mosquito_position = np.array([mosquito_array[num].x_axes, mosquito_array[num].y_axes])

            x = mosquito_position[0]
            y = mosquito_position[1]

            final_image = add_mask(x, y, image, mosquito_image, alpha_image)

            image = final_image 
    
    return mosquito_array, image

# this function removes an mosquito from array and add 1 to counter
def kill_mosquito(mosquito_array, counter, distance, x_initial, x_final, y_initial, y_final):
    # if mosquito position is between thumb and index finger, he's removed
    for num in range(mosquito_array.size):
        if(mosquito_array[num].x_axes >= x_initial and mosquito_array[num].x_axes <=x_final):
            if(mosquito_array[num].y_axes >= y_initial and mosquito_array[num].y_axes <= y_final):
                if(distance <= close_finger_value):
                    mosquito_array = np.delete(mosquito_array, num)
                    counter += 1
                    break

    return mosquito_array, counter


