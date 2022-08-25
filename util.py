from classes.variables import Variables
import numpy as np
import cv2

def update_image(variables:Variables, maze):#, maze, title, img_height, width, height, search_methods_name, active_search_methodIndex):
    # Generate description text
    text = variables.search_methods_name[variables.active_search_methodIndex]
    font = cv2.FONT_HERSHEY_SIMPLEX
    description = np.zeros(
        (int(variables.img_height*0.2), int(variables.img_height*variables.height/variables.width), 3), np.uint8)
    description.fill(255)
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = int((description.shape[1] - textsize[0]) / 2)
    textY = int((description.shape[0] + textsize[1]) / 2)
    cv2.putText(description, text, (textX, textY),
                font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Resize and show the image
    opencvImage = cv2.resize(maze.cv2Image, (variables.img_height, int(
        variables.img_height*variables.height/variables.width)), interpolation=cv2.INTER_AREA)
    cv2.imshow(variables.title, np.concatenate((opencvImage, description), axis=0))
    cv2.waitKey(1)



def change_active_search(variables:Variables, index):
    # Update the search method based on index
    variables.active_search_methodIndex = index
    variables.active_search_method = variables.search_methods[variables.active_search_methodIndex]