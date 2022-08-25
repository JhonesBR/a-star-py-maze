from classes.variables import Variables
from util import update_image
from time import sleep


def breadth_search(maze, delay, variables:Variables):
    # Variables
    variables.n_moves = 0
    path = [maze.start_point]

    # While the end point isn't reached
    while maze.current != maze.end_point:
        # Get every valid move (not visited closed to visited cells)
        ValidMoves = []
        for visitedCell in maze.visited_cells:
            ValidMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])
        newMoves = [
            move for move in ValidMoves if move not in maze.visited_cells]

        # Make every valid move and verify if the end point is reached
        for move in newMoves:
            variables.n_moves += 1
            path.append(move)
            maze.UpdateCurrentPoint(move[0], move[1])
            update_image(variables, maze)
            if maze.current == maze.end_point:
                break
            sleep(delay/1000)

    # Highlight the path
    maze.HighlightPath(path)