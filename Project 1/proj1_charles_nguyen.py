import numpy as np


#initialize variables, 0 representing the empty space---------------------------------------------------------------------------------

#From google I got the two hardest puzzle instances to test on, 31 moves each
start = np.array([[8,6,7],[2,5,4],[3,0,1]]) 
#start = np.array([[6,4,7],[8,5,0],[3,2,1]]) 

goal = np.array([[1,2,3],[4,5,6],[7,8,0]])
tree = [(start, 0)]
visited = set()
solved = False
counter = 0




#Functions----------------------------------------------------------------------------------------------------------------------------

#Movement Functions
def move_left(state):
    new_state = state.copy()
    blank_position = np.where(new_state == 0)
    x = blank_position[1][0]
    y = blank_position[0][0]
    if x > 0:
        new_state[y, x], new_state[y, x-1] = new_state[y, x-1], new_state[y, x]
    return new_state

def move_up(state):
    new_state = state.copy()
    blank_position = np.where(new_state == 0)
    x = blank_position[1][0]
    y = blank_position[0][0]
    if y > 0:
        new_state[y, x], new_state[y-1, x] = new_state[y-1, x], new_state[y, x]
    return new_state

def move_right(state):
    new_state = state.copy()
    blank_position = np.where(new_state == 0)
    x = blank_position[1][0]
    y = blank_position[0][0]
    if x < 2:
        new_state[y, x], new_state[y, x+1] = new_state[y, x+1], new_state[y, x]
    return new_state

def move_down(state):
    new_state = state.copy()
    blank_position = np.where(new_state == 0)
    x = blank_position[1][0]
    y = blank_position[0][0]
    if y < 2:
        new_state[y, x], new_state[y+1, x] = new_state[y+1, x], new_state[y, x]
    return new_state


#Define Check Visited function which will search if a board state has been previously visited
def check_if_visited(state):
    copy = state.copy()
    if tuple(copy.flatten()) in visited: 
        #I am converting my arrays into tuple lists once they are added to visited to allow usage of the set() structure. 
        #I previously did not do this and it could not solve 31 moves in 10 minutes, but now that I am using a hashable structure it is much faster.
        return False
    else:
        visited.add(tuple(copy.flatten()))
        return True

#Define explore function which will search possible board states and append them to next row
def explore(master, state_index):
    print(f"Attempting explore #: {counter} Tree Length: {len(tree)}")

    new_state = master[state_index][0].copy()
    previous_state_index = master[state_index][1]
    
    #Try to move in all possible directions
    try_up = move_up(new_state)
    try_right = move_right(new_state)
    try_down = move_down(new_state)
    try_left = move_left(new_state)

    #Check if the move was successful and not redundant, then append to master list
    if len(try_up) and check_if_visited(try_up):
        master.append((try_up, state_index))
    if len(try_right) and check_if_visited(try_right):
        master.append((try_right, state_index))
    if len(try_down) and check_if_visited(try_down):
        master.append((try_down, state_index))
    if len(try_left) and check_if_visited(try_left):
        master.append((try_left, state_index))


#Define Check Solution function to check the current state vs the goal state
def check_solution(master, state_index, solved):
    if np.array_equal(master[state_index][0], goal):
        solved = True
        print("Solution found!")
    return solved

#Define backtrack function to backtrack through the master tree and order the sequence of moves to reach the goal
def backtrack_for_path(master, state_index):
    print("Attempting to backtrack")
    path = []
    complete = False
    i = state_index

    while not complete:
        previous_state = master[master[i][1]][0]
        i = master[i][1]
        path.append(previous_state)
        if np.array_equal(previous_state, start):
            complete = True

    path.reverse()
    path.append(goal)
    return path





#Main Loop----------------------------------------------------------------------------------------------

while not solved:
    solved = check_solution(tree, counter, solved)
    explore(tree, counter)
    counter = counter + 1


path = backtrack_for_path(tree, counter-1)
#print(tree)
print(f"Tree Length: {len(tree)}")
print("-----------Printing Path---------------")
print(path)
print(f"Total moves to solution: {len(path)-1}")
print(f"Total Explores: {counter}")
print(f"Visited Length: {len(visited)}")

#Saving out the .txt files afterwards-------------------------------------------------------------------
print("Saving out Nodes.txt ....")
with open("Nodes.txt", "w") as f:
    for i in visited:
        f.write(" ".join(map(str,i)) + "\n")
print("Done!...")

print("Saving out Nodes.txt ....")
with open("NodesInfo.txt", "w") as f:
    f.write("Node_index      Parent_Node_index          Node \n")
    for k, i in enumerate(tree):
        
        f.write("    " + str(k) + "                   ")
        f.write(str(i[1]) + "             ")
        flat = i[0].flatten(order='F')
        f.write(" ".join(map(str,flat)) + "\n")
print("Done!...")

print("Saving out nodePath.txt ....")
with open("nodePath.txt", "w") as f:
    for i in path:
        flat = i.flatten(order='F')
        f.write(" ".join(map(str,flat)) + "\n")
print("Done!...")
