# Imports
from algorithms.manual_search import manual_search
from algorithms.random_search import random_search
from algorithms.depth_search import depth_search
from algorithms.breadth_search import breadth_search
from algorithms.greedy_search import greedy_search
from algorithms.a_star_search import a_star_search
from util import change_active_search
from tkinter import messagebox
from classes.maze import Maze
from util import update_image
from util import Variables
import cv2

def nothing(x):
    pass

# Parameters
maze_size = 20
img_px_size = 500


# Define the search algorithms and variables
variables = Variables()
variables.search_methods = [manual_search, random_search, depth_search,
                            breadth_search, greedy_search, a_star_search, a_star_search]
variables.search_methods_name = ["Manual Search", "Random Search", "Depth-first Search (DFS)",
                                "Breadth-first Search (BFS)", "Greedy Best-first Search", "A* Search", 'A* Search (Wrong)']
variables.width = maze_size
variables.height = maze_size
variables.img_height = img_px_size

# Generation
maze = Maze()
maze.GenerateMaze(variables.width, variables.height, variables.more_than_one_path, 5)
opencvImage = maze.GetCv2Image()
opencvImage = cv2.resize(
    opencvImage,
    (variables.img_height, int(variables.img_height*variables.height/variables.width)),
    interpolation=cv2.INTER_AREA
)
cv2.namedWindow(variables.title)
cv2.createTrackbar('delay', variables.title, 0, 1000, nothing)
update_image(variables, maze)

# Main loop
while cv2.getWindowProperty(variables.title, cv2.WND_PROP_VISIBLE) >= 1:
    # Get Key Pressed
    key_pressed = cv2.waitKey(1)

    # 'q' --> Quit
    if key_pressed == ord('q'):
        cv2.destroyAllWindows()
        break

    # 'g' --> Generate new maze
    if key_pressed == ord('g'):
        maze.GenerateMaze(variables.width, variables.height, variables.more_than_one_path)
        change_active_search(variables, 0)
        variables.end = False
        update_image(variables, maze)

    # 'r' --> Restart
    if key_pressed == ord('r'):
        maze.Restart()
        change_active_search(variables, 0)
        variables.end = False
        update_image(variables, maze)

    # Change active search method
    if key_pressed in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7')]:
        change_active_search(variables, key_pressed-ord('0')-1)

        # If the game started, restart it
        if len(maze.visited_cells) != 1:
            maze.Restart()
            variables.end = False
            update_image(variables, maze)

        # Activate the selected search method
        try:
            if key_pressed == ord('7'):
                variables.active_search_method(maze, cv2.getTrackbarPos('delay', variables.title), variables, wrong=True)
            else:
                variables.active_search_method(maze, cv2.getTrackbarPos('delay', variables.title), variables)
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            break

    if variables.end == False:
        # w --> Move up
        if key_pressed == ord('w'):
            variables.n_moves += 1
            maze.MoveUp()
            update_image(variables, maze)

        # s --> Move down
        if key_pressed == ord('s'):
            variables.n_moves += 1
            maze.MoveDown()
            update_image(variables, maze)

        # a --> Move left
        if key_pressed == ord('a'):
            variables.n_moves += 1
            maze.MoveLeft()
            update_image(variables, maze)

        # d --> Move right
        if key_pressed == ord('d'):
            variables.n_moves += 1
            maze.MoveRight()
            update_image(variables, maze)

        # Verify ending
        if maze.current == maze.end_point:
            variables.end = True
            update_image(variables, maze)
            messagebox.showinfo(
                "End", f"Finished in {variables.n_moves} moves with {variables.search_methods_name[variables.active_search_methodIndex]}")
            variables.n_moves = 0

cv2.destroyAllWindows()