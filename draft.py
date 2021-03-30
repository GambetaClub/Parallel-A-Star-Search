from threading import Thread
from queue import Queue
import time
import threading, time
from typing import final

finished = False

list1 = []
list2 = []


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def isValidNode(maze, node):
	if maze[node.position[0]][node.position[1]] != 0:
		return False
	else:
		return True

def createPath(current_node, t_number):
    """Creates path from the current node"""
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    if t_number == 1:
        return path[::-1] # Return reversed path
    else:
        return path

def coordinateResults(path1, path2):
    """Coordinates both paths"""
    temp = path1 + path2
    final_list = []
    [final_list.append(x) for x in temp if x not in final_list]
    return final_list

def BiAStar(maze, start, end):
    t1 = ThreadWithResult(target=aStar, args=(maze, start, end, list1, list2, 1))
    t2 = ThreadWithResult(target=aStar, args=(maze, end, start, list2, list1, 2))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    path = coordinateResults(t1.result, t2.result)
    return path
        
def aStar(maze, start, end, self_list, other_list, t_number):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
	
    # Check if both destination and origin are valid nodes
    if(not isValidNode(maze, start_node) or not isValidNode(maze, end_node)):
      print("The start and end nodes are not walkable nodes.")
      return 
    
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    counter = 1
    global finished

    # Loop until you find the end
    while len(open_list) > 0 and not finished:
        
        # This print statement is necessary for the functioning
        print("Thread #{} is working...".format(t_number))
        
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        
        # Loop until open list is empty
        if(len(open_list) > 1):
            
            # Loop through all nodes in open list and 
            # grabs the one with smallest f
            for index, item in enumerate(open_list):
                    
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        self_list.append(current_node.position)
        
        # Check if threads have found the same node and return
        # the path created so far
        if current_node.position in other_list:
            finished = True
            path = createPath(current_node, t_number)
            return path
        
        # Found the goal
        if current_node == end_node:
            path = createPath(current_node, t_number)
            return path
            
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the closed list
            if child in closed_list:
                continue
            
            # Child is already in the open list
            if child in open_list:
                continue
          
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            
            # Add the child to the open list
            open_list.append(child)

        # Keeps track of the number of iterations
        counter+=1
    
    # Return if the other thread found the same node
    if finished:
        path = createPath(current_node, t_number)
        return path

def main():
		#    0  1  2  3  4  5  6  7  8  9  10	
    maze = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], # 0
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1], # 1
            [0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1], # 2
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], # 3
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1], # 4
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], # 5
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], # 6
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0], # 7
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0], # 8
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 9
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]] # 10
    
    start = (0,0)
    end = (0,5)
    
    path = BiAStar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()