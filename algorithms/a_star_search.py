from classes.variables import Variables
from util import update_image
from visualize import Th
from classes.node import Node
from time import sleep
import random


def a_star_search(maze, delay, variables:Variables, wrong=False):
    # h(x) --> Euclidean distance
    def h(x):
        if wrong:
            return (((x[0]-maze.end_point[0])**2 + (x[1]-maze.end_point[1])**2)**0.5) * (len(maze.maze)**2 * random.random())
        return ((x[0]-maze.end_point[0])**2 + (x[1]-maze.end_point[1])**2)**0.5

    def coordToNode(coord, prev=None):
        return Node(prev, coord)

    variables.n_moves = 0
    open_list, closed_list = [], []
    start_node = coordToNode(maze.start_point)
    end_node = coordToNode(maze.end_point)
    closed_list.append(start_node)
    for neighbor in maze.GetValidMoves(start_node.position[0], start_node.position[1]):
        open_list.append(coordToNode(neighbor, start_node))

    while len(open_list) > 0:
        if maze.current == end_node.position:
            break

        # Calculate open_list f(x)
        for node in open_list:
            node.g = node.parent.g + 1
            node.h = h(node.position)
            node.f = node.g + node.h
            if node in closed_list:
                node.f = 999999999

        # Move to lowest f(x)
        open_listFs = [node.f for node in open_list]
        node_to_move = open_list[open_listFs.index(min(open_listFs))]
        maze.UpdateCurrentPoint(node_to_move.position[0], node_to_move.position[1])
        update_image(variables, maze)
        sleep(delay/1000)

        # Move it to the closed list
        closed_list.append(node_to_move)
        open_list.remove(node_to_move)

        # Append all valid moves from that node to the open list
        for neighbor in maze.GetValidMoves(node_to_move.position[0], node_to_move.position[1]):
            # Avoid nodes with same coords in open list
            closed_list_positions = [node.position for node in closed_list]
            open_list_positions = [node.position for node in open_list]
            if neighbor not in closed_list_positions and neighbor not in open_list_positions:
                open_list.append(coordToNode(neighbor, node_to_move))

    # Highlight the optimal path
    path = []
    current = node_to_move
    while current is not None:
        variables.n_moves += 1
        path.append(current.position)
        current.highlighted = True
        current = current.parent
    maze.HighlightPath(path)
    update_image(variables, maze)

    # Visualize the path
    visualization = Th(open_list, closed_list, "A* Search", ("8051" if wrong else "8050"))
    visualization.start()