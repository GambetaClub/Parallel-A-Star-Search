from threading import Thread, Lock
from queue import Queue
import time
import threading, time, random
from typing import final

mutex = Lock()
finished = False

list1 = []
list2 = []


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class Path():
    def __init__(self, path=None, common_node=None, found=False):
        self.path = path
        self.common_node = common_node
        self.found = found

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
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    if t_number == 1:
        return path[::-1] # Return reversed path
    else:
        return path

def coordinateResults(result1, result2):
    final_path = []
    if(result1.found):
        print("THREAD #1 FOUND THE NODE IN COMMON")
        final_path = result1.path
        node_index = result2.path.index(result1.common_node.position)
        useful_part = result1.path[node_index:]
        final_path = final_path + useful_part
    else:
        print("THREAD #2 FOUND THE NODE IN COMMON")
        final_path = result2.path
        node_index = result1.path.index(result2.common_node.position)
        useful_part = result1.path[:node_index]
        final_path = useful_part + final_path
        
    return final_path


def BiAStar(maze, start, end):
    t1 = ThreadWithResult(target=aStar, args=(maze, start, end, list1, list2, 1))
    t2 = ThreadWithResult(target=aStar, args=(maze, end, start, list2, list1, 2))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return (coordinateResults(t1.result, t2.result))
        
def aStar(maze, start, end, self_list, other_list, t_number):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
	
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
    
        # This print statement is necessary. Don't delete it
        print("Working...")
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        
        # Loop until open list is empty
        if(len(open_list) > 1):
            
            # Loop through all nodes in open list
            for index, item in enumerate(open_list):
                    
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        self_list.append(current_node)
        
        """Check if they have found the same node"""
        if current_node in other_list:
            finished = True
            path = Path(createPath(current_node, t_number), current_node, True)
            return path
        
        # Found the goal
        if current_node == end_node:
            path = Path(createPath(current_node, t_number), current_node)
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
    if finished:
        path = Path(createPath(current_node, t_number), current_node)
        return path
    
    
def main():
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
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 10
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 11
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 12
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 13
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 14
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 15
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 16
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 17
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 18
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 19
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 20
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 21
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 22
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 23
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 24
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 25
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 26
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 27
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 28
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 29
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 30
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 31
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 32
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 33
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], # 34
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], # 35
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]] # 36
    
    start = (0,0)
    end = (36,10)
    
    path = BiAStar(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()