from threading import Thread
import concurrent.futures
import time 

finished = False
threads = []

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
    return path[::-1] # Return reversed path

def aStar(maze, start, end, thread_number):
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
    counter = 1

    # Loop until you find the end
    while len(open_list) > 0 and not finished:
        # print("FROM THREAD {}".format(thread_number))
        
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        print("Open list count: {} \n".format(len(open_list)))
        
        if(len(open_list) > 1):
            for index, item in enumerate(open_list):
                if item.f == current_node.f and item != current_node:
                    print(f"#{counter}~THERE IS A DISPUTE!")
                    print("#{}~Current node: -> ({}) -> F = {}" .format(counter, current_node.position, current_node.f))
                    print("#{}~Item node: -> ({}) -> F = {}\n" .format(counter, item.position, item.f))
                    
                    """SAYS HELLO FROM THREAD"""
                    t = Thread(target=sayHello, args=("Mariano", len(threads)+1))
                
                    threads.append(t)
                    t.start()
                    # t = Thread(target=aStar, args=(maze, item.position, end, len(threads+1)))     
                    # thread = executor.submit(aStar, maze, item.position, end)
                    # result = thread.result()
                    # print(result)
                    # Putting the path together
                    
                    # return path
                    
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        
        print(" #{}~NODE CHOSEN --> ({}, {}) \n\n".format(counter, *current_node.position))

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

        print("OPEN LIST")
        for node in open_list:
            print("#{}~({}, {}) ~ F = {}".format(counter, *node.position, node.f))
        print()
        counter+=1
    
    for t in threads:
        t.join()

def sayHello(name, thread_number):
    """This funtion was created with the intention of showing when a
    thread would be created to divide the problem into subproblems"""
    time.sleep(1.0)
    print(f"Hello from thread #{thread_number} {name}!")

"""NOTE THAT THERE ARE CASES WHERE THERE IS A DISPUT, HOWEVER THOSE NODES ARE
NOT THE ONES THAT ARE GOING TO BE CHOSEN AT THE END. THE MAY HAVE THE SAME F COST,
HOWEVER, THAT DOESN"T MEAN THAT AT THAT POINT THERE IS A BOTTLE NECK. THUS, THERE
NO POINT TO PARALELLIZE THAT PART SINCE THERE IS NOTHING TO SPEED UP."""

def main():
		#    0  1  2  3  4  5  6  7  8  9  10	
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 1
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 2
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 3
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 4
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 5
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 6
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 7
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 8
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] # 10

    start = (5, 0)
    end = (5,10)
    
    finished = False
    path = aStar(maze, start, end, 0)
    
    print(path)


if __name__ == '__main__':
    main()