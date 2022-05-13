# Imports
from random import randint
from time import sleep
from maze import Maze
import numpy as np
from PIL import Image as im
import cv2
import random
from tkinter import messagebox

def updateImage():
    global opencvImage
    opencvImage = maze.GetCv2Image()
    opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)

def verifyEnd(maze):
    if (maze.endPoint == maze.current):
        return True
    return False

def randomSearch(maze, delay):
    # Random move from the list of possible moves
    currentX, currentY = maze.current

    # Make a move and wait a delay
    validMoves = maze.GetValidMoves(currentX, currentY)
    move = validMoves[random.randint(0, len(validMoves)-1)]
    maze.UpdateCurrentPoint(move[0], move[1])
    updateImage()

    global nMoves
    nMoves += 1
    sleep(delay/1000)

def depthSearch(maze, delay):
    # TODO NOT YET IMPLEMENTED
    pass

def breadthSearch(maze, delay):
    # TODO NOT YET IMPLEMENTED
    pass

def greedySearch(maze, delay):
    # Euclidean distance
    def h(x):
        return ((x[0]-maze.endPoint[0])**2 + (x[1]-maze.endPoint[1])**2)**0.5

    visitedNodes = maze.visitedCells
    validMoves = []
    for visitedNode in visitedNodes:
        validMoves += maze.GetValidMoves(visitedNode[0], visitedNode[1])
    
    f = [h(move) for move in validMoves]
    for i in range(len(f)):
        if validMoves[i] in visitedNodes:
            f[i] = 999999999
        
    move = validMoves[f.index(min(f))]
    maze.UpdateCurrentPoint(move[0], move[1])
    updateImage()

    global nMoves
    nMoves += 1
    sleep(delay/1000)

def aStarSearch(maze, delay):
    # TODO NOT YET IMPLEMENTED
    pass

def manualSearch(maze, delay):
    pass

def nothing(x):
    pass

def changeActiveSearch(index):
    global activeSearchMethodIndex
    global searchMethods
    global activeSearchMethod
    activeSearchMethodIndex = index
    activeSearchMethod = searchMethods[activeSearchMethodIndex]

# Generate maze
width, height = 25, 25
maze = Maze()
maze.GenerateMaze(width, height)
title = 'Maze'
ImgHeight = 800
opencvImage = maze.GetCv2Image()
opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)

# Parameters
searchMethods = [manualSearch, randomSearch, depthSearch, breadthSearch, greedySearch, aStarSearch]
searchMethodsName = ["Manual Search", "Random Seach", "Depth Search", "Breadth Seatch", "Greedy Best First", "A* Search"]
activeSearchMethodIndex = 0
activeSearchMethod = searchMethodsName[activeSearchMethodIndex]
end = False
cv2.namedWindow(title)
cv2.createTrackbar('delay',title , 0, 1000, nothing)

# Track moves
nMoves = 0

# Main loop
while True:
    cv2.imshow(title, opencvImage)

    keyPressed = cv2.waitKey(1)
    if keyPressed == ord('q'):
        cv2.destroyAllWindows
        break
    
    # Generate a new maze
    if keyPressed == ord('g'):
        maze.GenerateMaze(width, height)
        activeSearchMethod = manualSearch
        end = False
        updateImage()

    # Reset the maze
    if keyPressed == ord('r'):
        maze.Restart()
        activeSearchMethod = manualSearch
        end = False
        updateImage()

    # Change active search method
    if keyPressed in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
        changeActiveSearch(keyPressed-ord('0')-1)

        # If the game started, restart it
        if len(maze.visitedCells) != 1:
            maze.Restart()
            end = False
            updateImage()

    if end == False:
        try:
            activeSearchMethod(maze, cv2.getTrackbarPos('delay', title))
        except:
            continue

        if keyPressed == ord('w'):
            nMoves += 1
            maze.MoveUp()
            updateImage()

        if keyPressed == ord('s'):
            nMoves += 1
            maze.MoveDown()
            updateImage()

        if keyPressed == ord('a'):
            nMoves += 1
            maze.MoveLeft()
            updateImage()

        if keyPressed == ord('d'):
            nMoves += 1
            maze.MoveRight()
            updateImage()

        end = verifyEnd(maze)
        if end:
            updateImage()
            messagebox.showinfo("End", f"Finished in {nMoves} moves with {searchMethodsName[activeSearchMethodIndex]}")
