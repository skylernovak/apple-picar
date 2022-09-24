from cmath import inf
import numpy as np
import math
from enum import Enum

class Direction(Enum):
    UP = 0
    LEFT = 90
    DOWN = 180
    RIGHT = 270

    

def h(pos, target, npMap):
    if npMap[pos[0], pos[1]]:
        return (float(inf), float(inf))
    #Euclidean
    eucl = round(math.sqrt((target[0] - pos[0])**2 + (target[1] - pos[1])**2))
    #manhattan
    manh = abs(target[0] - pos[0]) + abs(target[1] - pos[1])
    return (eucl, manh)


def a_star_alg(start, end, heuristic, npMap):
    if heuristic == "manhattan":
        h_index = 1
    else :
        h_index = 0
    # open_list is a list of nodes which have been visited, but who's neighbors
    # haven't all been inspected, starts off with the start node
    # closed_list is a list of nodes which have been visited
    # and who's neighbors have been inspected
    open_list = set([start])
    closed_list = set([])

    # g contains current distances from start_node to all other nodes
    # the default value (if it's not found in the map) is +infinity
    g = {}
    g[start] = 0

    # parents contains an adjacency map of all nodes
    parents = {}
    parents[start] = start

    while len(open_list) > 0:
        curr = None 
        
        # find a node with the lowest value of f() - evaluation function
        for v in open_list:
            if curr == None or g[v] + h(v, end, npMap)[h_index] < g[curr] + h(curr, end, npMap)[h_index]:
                curr = v
        
        if curr == None:
            print('Path does not exist!')
            return None

        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if curr == end:
            reconst_path = []

            while parents[curr] != curr:
                reconst_path.append((curr[0] - 50, curr[1]))
                curr = parents[curr]

            reconst_path.append((start[0] - 50, start[1]))

            reconst_path.reverse()

            print('Path found: {}'.format(reconst_path))
            return reconst_path

        # for all neighbors of the current node do
        left = (curr[0]-1, curr[1]) if curr[0]-1 >= 0 else None
        right = (curr[0]+1, curr[1]) if curr[0]+1 < 100 else None
        up = (curr[0], curr[1]+1) if curr[1]+1 < 100 else None
        down = (curr[0], curr[1]-1) if curr[1]-1 >= 0 else None
        neighbors = [left, right, up, down]

        for neighbor in neighbors:
            if neighbor is None:
                continue
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as it's parent
            if neighbor is not None and neighbor not in closed_list and neighbor not in open_list:
                open_list.add(neighbor)
                parents[neighbor] = curr
                g[neighbor] = g[curr] + 1

            #check if quicker to first visit n, then ,
            #if yes : update parent data and g data
            #      if node was in closed_list, move to open_list
            else:
                if g[neighbor] > g[curr] + 1:
                    g[neighbor] = g[curr] + 1
                    parents[neighbor] = curr

                    if neighbor in closed_list:
                        closed_list.remove(neighbor)
                        open_list.add(neighbor)
        
        #remove curr from open_list, add to closed_list, because all neighbors were inspected
        open_list.remove(curr)
        closed_list.add(curr)

def next_dir(start, end):
    y = end[1] - start[1]
    x = end[0] - start[0]
    if (x, y) == (0, 1):
        return Direction.UP
    elif (x, y) == (0, -1):
        return Direction.DOWN
    elif (x, y) == (1, 0):
        return Direction.RIGHT
    elif (x, y) == (-1, 0):
        return Direction.LEFT
    else:
        raise Exception("next_dir failed for start:{0} and end:{1}".format(start, end))


turn_Map = {270: Direction.RIGHT, 90: Direction.LEFT, 0: Direction.UP, 180: Direction.DOWN}


curr_dir = Direction.UP

coords = [(0,0), (0, -1), (-1, -1), (-1, -2)]


def actions(coords):
    global curr_dir
    action_list = []
    for i in range(0, len(coords)-1):
        start= coords[i]
        end = coords[i+1]
        new_dir = next_dir(start, end)
        turn_action = turn_Map[(new_dir.value - curr_dir.value + 360)% 360]
        curr_dir = new_dir
        if (turn_action == Direction.RIGHT):
            action_list.append(["RIGHT", "FORWARD"])
        elif (turn_action == Direction.LEFT):
            action_list.append(["LEFT", "FORWARD"])
        elif (turn_action == Direction.DOWN):
            action_list.append(["LEFT", "LEFT", "FORWARD"])
        else :
            action_list.append(["FORWARD"])
    return action_list

def resetToNorth():
    global curr_dir
    new_dir = Direction.UP
    turn_action = turn_Map[(new_dir.value - curr_dir.value + 360)% 360]
    curr_dir = Direction.UP
    actionList = []
    if (turn_action == Direction.RIGHT):
        actionList.append("RIGHT")
    elif (turn_action == Direction.LEFT):
        actionList.append("LEFT")
    elif (turn_action == Direction.DOWN):
        actionList.append("LEFT")
        actionList.append("LEFT")
    return actionList

    


