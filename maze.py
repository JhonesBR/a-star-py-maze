# Inspiration https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
import random
from colorama import Fore
import numpy as np
from PIL import Image as im
import cv2

class Maze:
    maze = []
    wall = '■'
    cell = '☐'
    unvisited = "u"
    height = 0
    width = 0
    visitedCells = []
    current = [0, 0]
    
    def __init__(self):
        pass
        
    def GenerateMaze(self, width, height):
        self.maze = []
        self.height = height
        self.width = width
        
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
            
        # Determine start and end points
        for col in range(self.width):
            if self.maze[0][col] == self.cell:
                self.startPoint = [0, col]
                self.current = [0, col]
    
        for col in range(self.width):
            if self.maze[self.width-1][col] == self.cell:
                self.endPoint = [self.width-1, col]

    def __repr__(self):
        repr = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == "u"):
                    repr += Fore.WHITE + str(self.maze[i][j])
                elif (self.maze[i][j] == self.cell):
                    repr += Fore.GREEN + str(self.maze[i][j])
                else:
                    repr += Fore.RED + str(self.maze[i][j])
                
            repr += "\n"
        return repr
    
    def GetCv2Image(self):
        mazeR = self.GetMazeRepr()
        pixels = []
        for i in range(len(mazeR)):
            line = []
            for j in range(len(mazeR[0])):
                if mazeR[i][j] == self.GetCellChar():
                    line.append((255, 255, 255));
                elif mazeR[i][j] == self.GetWallChar():
                    line.append((0, 0, 0))
                else:
                    line.append((50, 50, 50))
            
                if [i, j] in self.visitedCells:
                    line[-1] = (0, 255, 0)
                    
                if [i, j] == self.current:
                    line[-1] = (255, 0, 0)
                    
            pixels.append(line)
        array = np.array(pixels, dtype=np.uint8)
        return cv2.cvtColor(np.array(im.fromarray(array).convert('RGB')), cv2.COLOR_RGB2BGR)
    
    def GetMazeRepr(self):
        return self.maze
    
    def GetCellChar(self):
        return self.cell
    
    def GetWallChar(self):
        return self.wall
    
    def GetHeight(self):
        return self.height
    
    def GetWidth(self):
        return self.width

    def UpdateCurrentPoint(self, x, y):
        self.visitedCells.append([x, y])
        self.current = [x, y]