# Imports
from random import randint
from time import sleep
from maze import Maze
from node import Node
import numpy as np
from PIL import Image as im
import cv2
import random
from tkinter import messagebox
import matplotlib.pyplot as plt

def updateImage():
    # Generate description text
    text = searchMethodsName[activeSearchMethodIndex]
    font = cv2.FONT_HERSHEY_SIMPLEX
    description = np.zeros((int(ImgHeight*0.2), int(ImgHeight*height/width), 3), np.uint8)
    description.fill(255)
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = int((description.shape[1] - textsize[0]) / 2)
    textY = int((description.shape[0] + textsize[1]) / 2)
    cv2.putText(description, text, (textX, textY), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Resize and show the image
    opencvImage = cv2.resize(maze.cv2Image, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)
    cv2.imshow(title, np.concatenate((opencvImage, description), axis=0))
    cv2.waitKey(1)

def randomSearch(maze, delay):
    # Variables
    global nMoves
    path = []
    
    # While the end point isn't reached (or key "s" is pressed)
    while maze.current != maze.endPoint:
        if cv2.waitKey(1) == ord('s'):
            return
            
        # Make a random move
        current = maze.current
        validMoves = maze.GetValidMoves(current[0], current[1])
        move = validMoves[random.randint(0, len(validMoves)-1)]
        maze.UpdateCurrentPoint(move[0], move[1])
        if move not in path:
            path.append(move)
        nMoves += 1
        updateImage()
        sleep(delay/1000)
        
    # Highlight the path
    maze.highlightPath(path)


def depthSearch(maze, delay):
    # Variables
    global backtrack
    global nMoves
    path = []
    backtrack = 0
    
    # While the end point isn't reached
    while maze.current != maze.endPoint:
        # Get every valid move (not visited closed to visited cells)
        current = maze.current
        validMoves = maze.GetValidMoves(current[0], current[1])
        newMoves = [move for move in validMoves if move not in maze.visitedCells]
        if len(newMoves) > 0:
            backtrack = 0
            move = newMoves[0]
            maze.UpdateCurrentPoint(move[0], move[1])
            path.append(move)
            nMoves += 1
            updateImage()
            # Verify if the end point is reached
            if maze.current == maze.endPoint:
                break
            sleep(delay/1000)
        else:
            # Backtrack
            while len(newMoves) == 0:
                backtrack += 1
                nMoves += 1
                current = maze.visitedCells[-backtrack]
                validMoves = maze.GetValidMoves(current[0], current[1])
                newMoves = [move for move in validMoves if move not in maze.visitedCells]
                sleep(delay/1000)
            move = newMoves[0]
            maze.UpdateCurrentPoint(move[0], move[1])
            path.append(move)
            nMoves += 1
            updateImage()
            sleep(delay/1000)
            
    # Highlight the path
    maze.highlightPath(path)

def breadthSearch(maze, delay):
    # Variables
    global nMoves
    path = []
    
    # While the end point isn't reached
    while maze.current != maze.endPoint:
        # Get every valid move (not visited closed to visited cells)
        validMoves = []
        for visitedCell in maze.visitedCells:
            validMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])
        newMoves = [move for move in validMoves if move not in maze.visitedCells]
        
        # Make every valid move and verify if the end point is reached
        for move in newMoves:
            nMoves += 1
            path.append(move)
            maze.UpdateCurrentPoint(move[0], move[1])
            updateImage()
            if maze.current == maze.endPoint:
                break
            sleep(delay/1000)
            
    # Highlight the path
    maze.highlightPath(path)

def greedySearch(maze, delay):
    # Euclidean distance
    def h(x):
        return ((x[0]-maze.endPoint[0])**2 + (x[1]-maze.endPoint[1])**2)**0.5

    # Variables
    global nMoves
    path = []
    
    # While the end point isn't reached
    while maze.current != maze.endPoint:
        # Get every valid move (not visited closed to visited cells)
        validMoves = []
        for visitedCell in maze.visitedCells:
            validMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])
        
        # Calculate f(x) for every valid move (f(x) -> h(x))
        f = [h(move) for move in validMoves]
        for i in range(len(f)):
            # Set the f(x) of already visited cells to infinity
            if validMoves[i] in maze.visitedCells:
                f[i] = 999999999
        
        # Move to the cell with the lowest f(x) and verify if the end point is reached
        move = validMoves[f.index(min(f))]
        maze.UpdateCurrentPoint(move[0], move[1])
        path.append(move)
        updateImage()
        nMoves += 1
        if maze.current == maze.endPoint:
            break
        sleep(delay/1000)
        
    # Highlight the path
    maze.highlightPath(path)

def aStarSearch(maze, delay):
    # TODO: Implement A* search
    pass

def manualSearch(maze, delay):
    # Controled by the main loop and object
    pass

def nothing(x):
    pass

def changeActiveSearch(index):
    # Update the search method based on index
    global activeSearchMethodIndex
    global searchMethods
    global activeSearchMethod
    activeSearchMethodIndex = index
    activeSearchMethod = searchMethods[activeSearchMethodIndex]

# Parameters
width, height = 100, 100
moreThanOnePath = True
title = 'Maze'
ImgHeight = 500

# Variables
searchMethods = [manualSearch, randomSearch, depthSearch, breadthSearch, greedySearch, aStarSearch]
searchMethodsName = ["Manual Search", "Random Seach", "Depth Search", "Breadth Seatch", "Greedy Best First", "A* Search"]
activeSearchMethodIndex = 0
activeSearchMethod = searchMethods[activeSearchMethodIndex]
end = False
nMoves = 0

# Generation
maze = Maze()
maze.GenerateMaze(width, height, moreThanOnePath)
opencvImage = maze.GetCv2Image()
opencvImage = cv2.resize(opencvImage, (ImgHeight, int(ImgHeight*height/width)), interpolation = cv2.INTER_AREA)
cv2.namedWindow(title)
cv2.createTrackbar('delay',title , 0, 1000, nothing)
updateImage()

# Main loop
while True:
    # Get Key Pressed
    keyPressed = cv2.waitKey(1)
    
    # 'q' --> Quit
    if keyPressed == ord('q'):
        cv2.destroyAllWindows
        break
    
    # 'g' --> Generate new maze
    if keyPressed == ord('g'):
        maze.GenerateMaze(width, height, moreThanOnePath)
        changeActiveSearch(0)
        end = False
        updateImage()

    # 'r' --> Restart
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
            
        # Activate the selected search method
        try:
            activeSearchMethod(maze, cv2.getTrackbarPos('delay', title))
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            break

    if end == False:
        # w --> Move up
        if keyPressed == ord('w'):
            nMoves += 1
            maze.MoveUp()
            updateImage()

        # s --> Move down
        if keyPressed == ord('s'):
            nMoves += 1
            maze.MoveDown()
            updateImage()

        # a --> Move left
        if keyPressed == ord('a'):
            nMoves += 1
            maze.MoveLeft()
            updateImage()

        # d --> Move right
        if keyPressed == ord('d'):
            nMoves += 1
            maze.MoveRight()
            updateImage()

        # Verify ending
        if maze.current == maze.endPoint:
            end = True
            updateImage()
            messagebox.showinfo("End", f"Finished in {nMoves} moves with {searchMethodsName[activeSearchMethodIndex]}")
