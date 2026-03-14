import numpy as np
import cv2
import heapq

#Initialize the some global variables. The open list will be a heapq, the closed list will be a dictionary, and a graph of all points visited will also be a dictionary
#Clearance is to specify how much of a buffer the obstacles have. This is a 2 unit (pixel) clearance pre-set.
clearance = 2
solved = False
oList = []
cList = dict()
graph = dict()


#Define code to get start and end point------------------------------------------------------------------------------------------------
#Define two functions that will get the start and goal points from user input. It checks to see if a point submitted is within an obstacle, outside of bounds, or in a improper format
def get_point_start():
    Input = False
    while not Input:
        try:
            x, y = map(int, input(f"Enter your starting point, bounds are x:(0 - 200) y:(0 - 50) (format: x y): ").split())
            
            # Check obstacles
            if (any(ob(x, y) for ob in obstacles)):
                print("Point is inside an obstacle or outside of bounds, choose a free space.")
                continue
            Input = True
            return (x, y)
        
        except ValueError:
            print("Invalid input, please follow the format")

def get_point_goal():
    Input = False
    while not Input:
        try:
            x, y = map(int, input(f"Enter your goal point, bounds are x:(0 - 200) y:(0 - 50) (format: x y): ").split())
            
            # Check obstacles
            if (any(ob(x, y) for ob in obstacles)):
                print("Point is inside an obstacle or outside of bounds, choose a free space.")
                continue
            Input = True
            return (x, y)
        
        except ValueError:
            print("Invalid input, please follow the format")

#Define obstacles as equations and store them in list-----------------------------------------------------------------------------------
def border(x, y): #Outer border of the workzone
    if x >= 0 and y >= 0 and x < 200 and y < 50:
        return False
    else:
        return True

def check_c(x, y): #Equation to check for the letter C
    outer_circle = (x-20)**2 + (y-25)**2 <= (12+clearance)**2 #Outer circle of C
    inner_circle = (x-20)**2 + (y-25)**2 <= (5)**2 #Inner Circle of C
    right_side = x > 24 #Cut off the right side of the circles to form a C

    return outer_circle and not inner_circle and not right_side

def check_n(x, y): #Equation to check for the letter N
    left_bar = 32-clearance <= x <= 36+clearance and 15-clearance <= y<= 35+clearance #Left bar of N
    right_bar = 49-clearance <= x <= 55+clearance and 15-clearance <= y<= 35+clearance #Right bar of N

    diagonal = (y - 34 - clearance) + 1.25*(x - 32 - clearance) < 5+clearance and -((y - 34) + 1.25*(x - 33)) < 5+clearance and 32-clearance <= x <= 55+clearance and 15-clearance <= y <= 35+clearance # Diagonal band across two bars for N

    return diagonal or left_bar or right_bar

def check_4(x, y): #Equation to check for number 4
    left_bar = 64-clearance <= x <= 69+clearance and 25-clearance <= y<= 35+clearance #Short left vertical bar of 4
    middle_bar = 64-clearance <= x <= 80+clearance and 25-clearance <= y<= 28+clearance #Horizontal middle bar of 4
    right_bar = 80-clearance <= x <= 85+clearance and 15-clearance <= y<= 35+clearance #Long right vertical bar of 4


    return left_bar or right_bar or middle_bar

def check_7(x, y): #Equation to check for number 4
    top_bar = 95-clearance <= x <= 110+clearance and 30-clearance <= y<= 35+clearance #Top horizontal bar of 7

    diagonal = abs((y - 34 - clearance) - 1.85*(x - 114 - clearance)) < 5+clearance+clearance and 95-clearance <= x <= 115+clearance and 15-clearance <= y <= 35+clearance #Diagonal band from top bar to bottom of 7

    return top_bar or diagonal

def check_first_3(x, y): #Equation to check for the first number 3 (Admittedly, this one does not look great, I had a hard time forming the number)
    top = (x-126)**2 + (y-27)**2 <= (8+clearance)**2 #Top outer circle of 3
    top_inner = (x-126)**2 + (y-27)**2 <= (3)**2 #Top inner circle of 3
    bottom = (x-126)**2 + (y-23)**2 <= (8+clearance)**2 #Bottom outer circle of 3
    bottom_inner = (x-126)**2 + (y-21)**2 <= (3)**2 #Bottom inner circle of 3

    middle_bar = 127-clearance <= x <= 130+clearance and 25-clearance <= y<= 25+clearance #Horizontal bar in the middle of the two vertically stacked circles to accentuate the 3

    cut_left = x > 123 #Cut off the left side to form a 3

    return (top or bottom ) and cut_left and not(top_inner or bottom_inner) or middle_bar

def check_second_3(x, y): #Equation to check for the second number 3
    top = (x-141)**2 + (y-27)**2 <= (8+clearance)**2 #Top outer circle of 3
    top_inner = (x-141)**2 + (y-27)**2 <= (3)**2 #Top inner circle of 3
    bottom = (x-141)**2 + (y-23)**2 <= (8+clearance)**2 #Bottom outer circle of 3
    bottom_inner = (x-141)**2 + (y-21)**2 <= (3)**2 #Bottom inner circle of 3

    middle_bar = 142-clearance <= x <= 145+clearance and 25-clearance <= y<= 25+clearance #Horizontal bar in the middle of the two vertically stacked circles to accentuate the 3

    cut_left = x > 138 #Cut off the left side to form a 3

    return (top or bottom ) and cut_left and not(top_inner or bottom_inner) or middle_bar


#We store all of the obstacle functions in a list so that we can iterate through it and check all of them in a cleaner way later on
obstacles = [border, check_c, check_n, check_4, check_7, check_first_3, check_second_3]




#Define obstacle checking-------------------------------------------------------------------------------------------------
#Takes a list of potential moves from explore() function and checks to see if each move is within an obstacle or not. It will then return a list of all moves not within an obstacle.
#Storing all of the functions in a list earlier makes this function much cleaner to write as opposed to making multiple nested "if" statements.
def check_obstacles(move_list):
    successful = []
    for i in move_list:
        x = i[0][0]
        y = i[0][1]
        if not(any(ob(x, y) for ob in obstacles)):
            successful.append(i)
    return successful




#Define move functions-------------------------------------------------------------------------------------------------
#Set of functions for all 8 movement choices. It will attempt the move and assign the cost for that move as well
def move_right(node):
    cost = 1
    new_node = node[0]
    return (new_node[0]+1, new_node[1]), cost

def move_down_right(node):
    cost = 1.4
    new_node = node[0]
    return (new_node[0]+1, new_node[1]-1), cost

def move_down(node):
    cost = 1
    new_node = node[0]
    return (new_node[0], new_node[1]-1), cost

def move_down_left(node):
    cost = 1.4
    new_node = node[0]
    return (new_node[0]-1, new_node[1]-1), cost

def move_left(node):
    cost = 1
    new_node = node[0]
    return (new_node[0]-1, new_node[1]), cost

def move_up_left(node):
    cost = 1.4
    new_node = node[0]
    return (new_node[0]-1, new_node[1]+1), cost

def move_up(node):
    cost = 1
    new_node = node[0]
    return (new_node[0], new_node[1]+1), cost

def move_up_right(node):
    cost = 1.4
    new_node = node[0]
    return (new_node[0]+1, new_node[1]+1), cost









#Check if the node is in the closed or open list------------------------------------------------------------------------
def check_if_seen(node_list, parent): #This function takes in a list of potential moves from explore() and checks if they've already been visited or not. It returns a list of moves that haven't been made/have cheaper costs than before
    not_visited = []
    for i in node_list: 
        if i[0] not in cList:#This if checks if the node is already in the closed list or not
            if i[0] in graph: #Check if this node has every been visited before in the graph, if it has then see if you can update the cost to a lower one
                current_cost = graph[i[0]]
                new_cost = parent[1][2] + i[1]
                if new_cost < current_cost:
                    graph[i[0]] = new_cost
                    not_visited.append(i)
            else: #If it hasn't been, then add it to the graph as well as the "not visited" list to add to open later
                graph[i[0]] = i[1]
                not_visited.append(i)
        else: #If it is in the closed list, then check to see if the new cost is cheaper than the cost it was already assigned. If it is, update it. Then re-add the cheaper cost into the "not-visited" list to go into the open list
            current_cost = cList[i[0]][0]
            new_cost = parent[1][2] + i[1]
            if new_cost < current_cost:
                cList[i[0]][0] = new_cost
                not_visited.append(i)
    return not_visited #Return a list of new/cheaper moves






#Define node creation in the open list---------------------------------------------------------------------------------------
def create_new_nodes(moves, parent): #Adds new nodes to the open list
    for i in moves:
        cost = parent[1][2] + i[1]
        node_to_be_added = ([i[0], parent[1][0], cost])
        heapq.heappush(oList, (node_to_be_added[2], node_to_be_added))




#Check if current node is the solution---------------------------------------------------------------------------------------
def check_if_solution(node): #Checks a node to see if it is the goal node
    if node[1][0] == goal_node:
        return True
    else:
        return False




#Backtrack from the solution to the start------------------------------------------------------------------------------------
def backtrack_for_path(node): #Backtracks from the current node to the start node, then returns the path.
    path = []
    path.append(node[1][0])
    path_complete = False
    total_cost = node[0]

    next_node = [1, node[1][0]]

    while not path_complete:
        next_node = cList[next_node[1]]
        if next_node[1] == None:
            path_complete = True
            
        else:
            path.append(next_node[1])


    path.reverse()
    print(f"Path: {path}  Cost: {total_cost}")
    return path
        




#Main explore function----------------------------------------------------------------------------------------------------------
def explore(node): #The explore function is the heart of this program. It will attempt to explore in all 8 directions from a inputted node, keeping only legal (not in obstacle or outside of zone) and new/cheaper moves and append them to the open list.
    attempted_moves = ([])
    
    #Attempt all 8 moves, storing them in the "attempted_moves" list
    try_right, R_Cost = move_right(node[1])
    attempted_moves.append([try_right, R_Cost])

    try_down_right, DR_Cost = move_down_right(node[1])
    attempted_moves.append([try_down_right, DR_Cost])

    try_down, D_Cost = move_down(node[1])
    attempted_moves.append([try_down, D_Cost])

    try_down_left, DL_Cost = move_down_left(node[1])
    attempted_moves.append([try_down_left, DL_Cost])

    try_left, L_Cost = move_left(node[1])
    attempted_moves.append([try_left, L_Cost])

    try_up_left, UL_Cost = move_up_left(node[1])
    attempted_moves.append([try_up_left, UL_Cost])

    try_up, U_Cost = move_up(node[1])
    attempted_moves.append([try_up, U_Cost])

    try_up_right, UR_Cost = move_up_right(node[1])
    attempted_moves.append([try_up_right, UR_Cost])

    #Filter out any moves that are inside obstacles from the attempted moves list
    legal_moves = check_obstacles(attempted_moves)

    #Filter out any moves that go to pre-visited nodes, updating the cost for any newly discovered cheaper paths
    successful_moves = check_if_seen(legal_moves, node)

    #Adds the fully filtered list of attempted moves to the open list.
    create_new_nodes(successful_moves, node)


#Visualization Function-------------------------------------------------------------------------------------------------
def visualize(path):
    #Since our zone only 50 pixels in the Y and 200 pixels in the X, we implement a scale to visualize increase the window size.
    scale = 3
    width = 200
    height = 50

    #Create an empty image that's the size of our workzone in pixels.
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    #Iterate through and draw all of the obstacles in the image. This will check all pixels and if they are within our obstacles list of functions draw them in black
    for x in range(width):
        for y in range(height):
            adjusted_y = height-y
            if any(ob(x, y) for ob in obstacles):

                img[adjusted_y,x] = (0,0,0)

    #This is the visualization of all nodes explored. It will go through and draw blue on every node in the "graph" dictionary
    for i in graph:
        x_graph = i[0]
        y = i[1]
        if y == 0:
            y = 1
        adjusted_y = 50-y
        img[adjusted_y,x_graph] = (255,0,0)
        cv2.waitKey(1)
        big_img = cv2.resize(img, (img.shape[1]*scale, img.shape[0]*scale), interpolation=cv2.INTER_NEAREST) #Here we re-size the image to a larger scale for viewing while keeping the pixel count
        cv2.imshow("Path", big_img)

    #This is the visualization of the shortest path found. It will go through and draw red on every node in the path list
    for x, y in path:
        if y == 0:
            y = 1
        adjusted_y = height-y
        img[adjusted_y,x] = (0,0,255)
        cv2.waitKey(10)
        big_img = cv2.resize(img, (img.shape[1]*scale, img.shape[0]*scale), interpolation=cv2.INTER_NEAREST) #Here we re-size the image to a larger scale for viewing while keeping the pixel count
        cv2.imshow("Path", big_img)

    cv2.destroyAllWindows()
    cv2.imshow("Path", big_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




#Theory:
#1. Pop open list node with lowest cost
#2. Check if the node is the closed list already, if it isn't, then add it to the closed list.
#3. Explore from that node, checking all adjacent nodes and adding the legal+new/cheaper ones to the open list
#4. Check if that node is the solution node
    #5. If yes, backtrack to the original start node
    #6. Draw a visualzation for the areas explored and the shortest path 

#Main Loop --------------------------------------------------------------------------------------------------------------------------------------------------------
#Get start and goal nodes from user input in the terminal
start = get_point_start()
goal_node = get_point_goal()
starting_node = [start, None, 0] #Coordinates, previous node, and cost

#Push the starting node to our open list
heapq.heappush(oList, (0, starting_node))

while not solved: #Iterate through the process outlined above until a solution is found

    active_node = heapq.heappop(oList)
    if active_node[1][0] not in cList:
        cList[active_node[1][0]] = (active_node[0], active_node[1][1])
    explore(active_node)
    if check_if_solution(active_node):
        solved = True
        print("Success! Node found!")
        answer = backtrack_for_path(active_node)
        print(f"Graph length:{len(graph)}")
        print(f"Open length:{len(oList)}")
        visualize(answer)
