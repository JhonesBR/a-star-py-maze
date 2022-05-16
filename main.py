# Imports
from random import randint
from time import sleep
from maze import Maze
import numpy as np
from PIL import Image as im
import cv2
import random
from tkinter import messagebox
import matplotlib.pyplot as plt

def updateImage():
    text = searchMethodsName[activeSearchMethodIndex]
    font = cv2.FONT_HERSHEY_SIMPLEX
    opencvImage = cv2.resize(maze.cv2Image, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)
    
    description = np.zeros((int(ImgHeight*0.2), int(ImgHeight*height/width), 3), np.uint8)
    description.fill(255)
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = int((description.shape[1] - textsize[0]) / 2)
    textY = int((description.shape[0] + textsize[1]) / 2)
    cv2.putText(description, text, (textX, textY), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow(title, np.concatenate((opencvImage, description), axis=0))
    cv2.waitKey(1)

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

backtrack = 0
def depthSearch(maze, delay):
    current = maze.current
    global backtrack
    global nMoves
    validMoves = maze.GetValidMoves(current[0], current[1])
    newMoves = [move for move in validMoves if move not in maze.visitedCells]
    if len(newMoves) > 0:
        backtrack = 0
        move = newMoves[0]
        maze.UpdateCurrentPoint(move[0], move[1])
        nMoves += 1
        updateImage()
        sleep(delay/1000)
    else:
        while len(newMoves) == 0:
            backtrack += 1
            nMoves += 1
            current = maze.visitedCells[-backtrack]
            validMoves = maze.GetValidMoves(current[0], current[1])
            newMoves = [move for move in validMoves if move not in maze.visitedCells]
            sleep(delay/1000)
        move = newMoves[0]
        maze.UpdateCurrentPoint(move[0], move[1])
        nMoves += 1
        updateImage()
        sleep(delay/1000)

def breadthSearch(maze, delay):
    global nMoves
    validMoves = []
    for visitedCell in maze.visitedCells:
        validMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])
    newMoves = [move for move in validMoves if move not in maze.visitedCells]
    for move in newMoves:
        nMoves += 1
        maze.UpdateCurrentPoint(move[0], move[1])
        updateImage()
        if maze.current == maze.endPoint:
            return
        sleep(delay/1000)

def greedySearch(maze, delay):
    # Euclidean distance
    def h(x):
        return ((x[0]-maze.endPoint[0])**2 + (x[1]-maze.endPoint[1])**2)**0.5

    validMoves = []
    for visitedCell in maze.visitedCells:
        validMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])
    
    f = [h(move) for move in validMoves]
    for i in range(len(f)):
        if validMoves[i] in maze.visitedCells:
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
width, height = 100, 100
maze = Maze()
moreThanOnePath = True
maze.GenerateMaze(width, height, moreThanOnePath)
title = 'Maze'
ImgHeight = 500

opencvImage = maze.GetCv2Image()
opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)

# Parameters
searchMethods = [manualSearch, randomSearch, depthSearch, breadthSearch, greedySearch, aStarSearch]
searchMethodsName = ["Manual Search", "Random Seach", "Depth Search", "Breadth Seatch", "Greedy Best First", "A* Search"]
activeSearchMethodIndex = 0
activeSearchMethod = searchMethods[activeSearchMethodIndex]
end = False
cv2.namedWindow(title)
cv2.createTrackbar('delay',title , 0, 1000, nothing)
updateImage()

# Track moves
nMoves = 0

# Main loop
while True:
    keyPressed = cv2.waitKey(1)
    if keyPressed == ord('q'):
        cv2.destroyAllWindows
        break
    
    # Generate a new maze
    if keyPressed == ord('g'):
        maze.GenerateMaze(width, height, moreThanOnePath)
        changeActiveSearch(0)
        end = False
        updateImage()

    # Reset the maze
    if keyPressed == ord('r'):
        maze.Restart()
        changeActiveSearch(0)
        end = False
        updateImage()

    # Change active search method
    if keyPressed in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6')]:
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
            print("Error")

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
