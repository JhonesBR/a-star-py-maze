from classes.variables import Variables
from util import update_image
from time import sleep


def greedy_search(maze, delay, variables:Variables):
    # Euclidean distance
    def h(x):
        return ((x[0]-maze.end_point[0])**2 + (x[1]-maze.end_point[1])**2)**0.5

    # Variables
    variables.n_moves = 0
    path = []

    # While the end point isn't reached
    while maze.current != maze.end_point:
        # Get every valid move (not visited closed to visited cells)
        ValidMoves = []
        for visitedCell in maze.visited_cells:
            ValidMoves += maze.GetValidMoves(visitedCell[0], visitedCell[1])

        # Calculate f(x) for every valid move (f(x) -> h(x))
        f = [h(move) for move in ValidMoves]
        for i in range(len(f)):
            # Set the f(x) of already visited cells to infinity
            if ValidMoves[i] in maze.visited_cells:
                f[i] = 999999999

        # Move to the cell with the lowest f(x) and verify if the end point is reached
        move = ValidMoves[f.index(min(f))]
        maze.UpdateCurrentPoint(move[0], move[1])
        path.append(move)
        update_image(variables, maze)
        variables.n_moves += 1
        if maze.current == maze.end_point:
            break
        sleep(delay/1000)

    # Highlight the path
    path.append(maze.start_point)
    maze.HighlightPath(path)