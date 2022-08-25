from classes.variables import Variables
from util import update_image
from time import sleep
import random
import cv2


def random_search(maze, delay, variables:Variables):
    # Variables
    variables.n_moves = 0
    path = []

    # While the end point isn't reached (or key "s" is pressed)
    while maze.current != maze.end_point:
        if cv2.waitKey(1) == ord('s'):
            return

        # Make a random move
        current = maze.current
        ValidMoves = maze.GetValidMoves(current[0], current[1])
        move = ValidMoves[random.randint(0, len(ValidMoves)-1)]
        maze.UpdateCurrentPoint(move[0], move[1])
        if move not in path:
            path.append(move)
        variables.n_moves += 1
        update_image(variables, maze)
        sleep(delay/1000)

    # Highlight the path
    maze.HighlightPath(path)