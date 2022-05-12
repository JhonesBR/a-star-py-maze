# Imports
from ast import While
from time import sleep
from maze import Maze
import numpy as np
from PIL import Image as im
import cv2

# Generate maze
width, height = 20, 20
maze = Maze()
maze.GenerateMaze(width, height)
title = 'Maze'
ImgHeight = 500
opencvImage = maze.GetCv2Image()
opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)

while True:
    cv2.imshow(title, opencvImage)
    
    keyPressed = cv2.waitKey(1)
    if keyPressed == ord('q'):
        cv2.destroyAllWindows
        break
    
    # Generate and update image
    if keyPressed == ord('g'):
        maze.GenerateMaze(width, height)
        opencvImage = maze.GetCv2Image()
        opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)