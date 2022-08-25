# Inspiration https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
from PIL import Image as im
from typing import List
import numpy as np
import random
import cv2

class Maze:
    maze = []
    wall = '■'
    cell = '☐'
    unvisited = "u"
    height = 0
    width = 0
    visited_cells = []
    current = [0, 0]
    cv2Image = []

    # BGR
    WALL_COLOR = (0, 0, 0)
    CELL_COLOR = (255, 255, 255)
    CURRENT_COLOR = (0, 0, 255)
    VISITED_COLOR = (180, 180, 180)
    HIGHLIGHTED_COLOR = (0, 0, 255)

    def __init__(self):
        pass
        
    def GenerateMaze(self, width:int, height:int, more_than_one_path:bool=False, openCoeff:int=5):
        self.maze = []
        self.height = height
        self.width = width
        self.visited_cells = []
        
        # Find number of surrounding cells
        def surroundingCells(rand_wall):
            s_cells = 0
            if (self.maze[rand_wall[0]-1][rand_wall[1]] == self.cell):
                s_cells += 1
            if (self.maze[rand_wall[0]+1][rand_wall[1]] == self.cell):
                s_cells += 1
            if (self.maze[rand_wall[0]][rand_wall[1]-1] == self.cell):
                s_cells +=1
            if (self.maze[rand_wall[0]][rand_wall[1]+1] == self.cell):
                s_cells += 1

            return s_cells
        
        # Denote all cells as unvisited
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(self.unvisited)
            self.maze.append(line)
            
        # Randomize starting point and set it a cell
        starting_height = int(random.random()*height)
        starting_width = int(random.random()*width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == width-1):
            starting_width -= 1
            
        starting_height = random.randint(1, height-2)
        starting_width = random.randint(1, width-2)
            
        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])
        
        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = self.wall
        self.maze[starting_height][starting_width - 1] = self.wall
        self.maze[starting_height][starting_width + 1] = self.wall
        self.maze[starting_height + 1][starting_width] = self.wall

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == "u" and self.maze[rand_wall[0]][rand_wall[1]+1] == self.cell):
                    # Find the number of surrounding cells
                    s_cells = surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])


                        # Bottom cell
                        if (rand_wall[0] != height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                    
                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == "u" and self.maze[rand_wall[0]+1][rand_wall[1]] == self.cell):

                    s_cells = surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == "u" and self.maze[rand_wall[0]-1][rand_wall[1]] == self.cell):

                    s_cells = surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[0] != height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)


                    continue

            # Check the right wall
            if (rand_wall[1] != width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == "u" and self.maze[rand_wall[0]][rand_wall[1]-1] == self.cell):

                    s_cells = surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[1] != width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)
            
        # Mark the remaining unvisited cells as walls
        for i in range(0, height):
            for j in range(0, width):
                if (self.maze[i][j] == "u"):
                    self.maze[i][j] = self.wall

        # Set entrance and exit
        for i in range(0, width):
            if (self.maze[1][i] == self.cell):
                self.maze[0][i] = self.cell
                break

        for i in range(width-1, 0, -1):
            if (self.maze[height-2][i] == self.cell):
                self.maze[height-1][i] = self.cell
                break
        
        # Open paths if more_than_one_path is True
        if more_than_one_path:
            walls = []
            for col in range(1, width-1):
                for row in range(1, height-1):
                    if self.maze[row][col] == self.wall:
                        walls.append([row, col])
            random.shuffle(walls)
            for i in walls[:int(len(walls)/openCoeff)]:
                self.maze[i[0]][i[1]] = self.cell

        # Determine start and end points
        for col in range(self.width):
            if self.maze[0][col] == self.cell:
                self.start_point = [0, col]
                self.current = [0, col]
    
        for col in range(self.width):
            if self.maze[self.width-1][col] == self.cell:
                self.end_point = [self.width-1, col]

        print(f"Start Point --> {self.start_point}")
        print(f"End Point --> {self.end_point}")

        self.GenerateCv2Image()
        
        # Set initial points as visited
        self.UpdateCurrentPoint(self.current[0], self.current[1])
        
    def Restart(self):
        self.visited_cells = []
        self.current = self.start_point
        self.GenerateCv2Image()
        self.UpdateCurrentPoint(self.current[0], self.current[1])
    
    def GetCv2Image(self):
        mazeR = self.maze
        pixels = []
        for i in range(len(mazeR)):
            line = []
            for j in range(len(mazeR[0])):
                if mazeR[i][j] == self.cell:
                    line.append(self.CELL_COLOR);
                elif mazeR[i][j] == self.wall:
                    line.append(self.WALL_COLOR)
            
                if [i, j] in self.visited_cells:
                    line[-1] = self.VISITED_COLOR
                    
                if [i, j] == self.current:
                    line[-1] = self.CURRENT_COLOR
                    
            pixels.append(line)
        array = np.array(pixels, dtype=np.uint8)
        return cv2.cvtColor(np.array(im.fromarray(array).convert('RGB')), cv2.COLOR_RGB2BGR)
    
    def GenerateCv2Image(self):
        mazeR = self.maze
        pixels = []
        for i in range(len(mazeR)):
            line = []
            for j in range(len(mazeR[0])):
                if mazeR[i][j] == self.cell:
                    line.append(self.CELL_COLOR);
                elif mazeR[i][j] == self.wall:
                    line.append(self.WALL_COLOR)
            
                if [i, j] in self.visited_cells:
                    line[-1] = self.VISITED_COLOR
                    
                if [i, j] == self.current:
                    line[-1] = self.CURRENT_COLOR
                    
            pixels.append(line)
        array = np.array(pixels, dtype=np.uint8)
        self.cv2Image = cv2.cvtColor(np.array(im.fromarray(array).convert('RGB')), cv2.COLOR_RGB2BGR)

    def UpdateCurrentPoint(self, x:int, y:int):
        self.cv2Image[self.current[0]][self.current[1]] = self.VISITED_COLOR
        self.current = [x, y]
        self.cv2Image[x, y] = self.CURRENT_COLOR
        if self.current not in self.visited_cells:
            self.visited_cells.append(self.current)

    def HighlightPath(self, path:List[List[int]]):
        for node in path:
            self.cv2Image[node[0]][node[1]] = self.HIGHLIGHTED_COLOR
        # self.cv2Image[self.end_point[0]][self.end_point[1]] = [0, 0, 255]

    def MoveUp(self):
        x, y = self.current[0]-1, self.current[1]
        if self.ValidMove(x, y):
            self.UpdateCurrentPoint(x, y)

    def MoveDown(self):
        x, y = self.current[0]+1, self.current[1]
        if self.ValidMove(x, y):
            self.UpdateCurrentPoint(x, y)

    def MoveRight(self):
        x, y = self.current[0], self.current[1]+1
        if self.ValidMove(x, y):
            self.UpdateCurrentPoint(x, y)

    def MoveLeft(self):
        x, y = self.current[0], self.current[1]-1
        if self.ValidMove(x, y):
            self.UpdateCurrentPoint(x, y)

    def ValidMove(self, x:int, y:int):
        # Cant move beyond boundaries
        if (x < 0 or x >= self.height or y < 0 or y >= self.width):
            return False
        # Cant move to wall
        if (self.maze[x][y] == self.wall):
            return False
        return True

    def GetValidMoves(self, x:int, y:int):
        # All directions [r, u, l, d]
        suposedValid = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
        
        # Return array of possible directions to go ex. [up, down]
        return [move for move in suposedValid if self.ValidMove(move[0], move[1])]