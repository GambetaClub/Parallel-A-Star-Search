from threading import Thread
import concurrent.futures
finished = False

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
  

def aStar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
		
    # Create start and end node
    global finished
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
    while len(open_list) > 0 and not finished:
        
        print("Open List: ")
        for node in open_list:
            print("({}, {})".format(*node.position))

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            # if item.f == current_node.f:
            #     print("HAY UNA DISPUTA!")
            #     with concurrent.futures.ThreadPoolExecutor() as executor:
            #         thread = executor.submit(aStar, maze, item.position, end)
            #         path = thread.result()
            #         print(path)
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        
        print("Current node --> ({}, {})".format(*current_node.position))

        # Found the goal
        if current_node == end_node:
            finished = True
            print("Finished! {}" .format(finished))
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

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

def sayHello(name):
  print("Hello from a thread {}!".format(name))
  return "Hello from outside of a thread."

def main():
		#    0  1  2  3  4  5  6  7  8  9	
    maze = [[0, 1, 0, 0, 1, 0, 0, 0, 0, 0], # 0
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], # 1
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 2
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 4
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 5
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 6
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 7
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] # 9

    start = (0, 0)
    end = (9,9)
    
    finished = False
    path = aStar(maze, start, end)
    
    print(path)


if __name__ == '__main__':
    main()