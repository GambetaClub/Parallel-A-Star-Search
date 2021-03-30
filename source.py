from time import perf_counter

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

def createPath(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def aStar(maze, start, end):
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

    # Loop until you find the end
    while len(open_list) > 0:
        
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
        
        # Found the goal
        if current_node == end_node:
            path = createPath(current_node)
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
    
    t1_start = perf_counter()
    path = aStar(maze, start, end)
    t1_stop = perf_counter()
    
    print(path)
    print("Elapsed time during the whole program in seconds:",
                                        t1_stop-t1_start)


if __name__ == '__main__':
    main()