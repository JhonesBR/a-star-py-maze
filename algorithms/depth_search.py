from classes.variables import Variables
from util import update_image
from time import sleep


def depth_search(maze, delay, variables:Variables):
    # Variables
    variables.n_moves = 0
    path = [maze.start_point]
    backtrack = 0

    # While the end point isn't reached
    while maze.current != maze.end_point:
        # Get every valid move (not visited closed to visited cells)
        current = maze.current
        ValidMoves = maze.GetValidMoves(current[0], current[1])
        newMoves = [
            move for move in ValidMoves if move not in maze.visited_cells]
        if len(newMoves) > 0:
            backtrack = 0
            move = newMoves[0]
            maze.UpdateCurrentPoint(move[0], move[1])
            path.append(move)
            variables.n_moves += 1
            update_image(variables, maze)
            # Verify if the end point is reached
            if maze.current == maze.end_point:
                break
            sleep(delay/1000)
        else:
            # Backtrack
            while len(newMoves) == 0:
                backtrack += 1
                variables.n_moves += 1
                current = maze.visited_cells[-backtrack]
                ValidMoves = maze.GetValidMoves(current[0], current[1])
                newMoves = [
                    move for move in ValidMoves if move not in maze.visited_cells]
                sleep(delay/1000)
            move = newMoves[0]
            maze.UpdateCurrentPoint(move[0], move[1])
            path.append(move)
            variables.n_moves += 1
            update_image(variables, maze)
            sleep(delay/1000)

    # Highlight the path
    maze.HighlightPath(path)