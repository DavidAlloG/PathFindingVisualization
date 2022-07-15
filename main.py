import curses, queue, time

maze = [
    ["#", " ", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "X"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


def print_maze(maze, stdscr, path=[]):
    """Function to print the path in a fancy way"""
    blue = curses.color_pair(1)
    red = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i,j*2,"X",red) #Double space between cols to improve visualization
            else:
                stdscr.addstr(i,j*2,value,blue)

def find_start(maze, start_str):
    """Returns row, col of the start point"""
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start_str:
                return i, j
    return None

def find_neighbors(maze, row, col):
    """Returns all neighbors, valid or invalid"""
    neighbors = [] #Initialize neighbors

    #Conditions to add neighbors
    if row > 0:
        neighbors.append((row-1,col))
    if row + 1 < len(maze):
        neighbors.append((row+1,col))
    if col > 0:
        neighbors.append((row,col-1))
    if col + 1 < len(maze[0]):
        neighbors.append((row,col+1))

    return neighbors   


def find_path(maze, stdscr):
    """Return the shortest path between the start "O" and end "x" """
    start_str = 'O'
    end_str = 'X'
    start_ind = find_start(maze, start_str) #Start index

    q = queue.Queue() #Create a queue -> First in First out 
    q.put((start_ind, [start_ind])) #First element includes index and second element the path followed to reach the index

    visited = set() #To store visited points
    visited.add(start_ind)

    while not q.empty(): #Loop while till we reach end or visit all points
        current_ind, path = q.get() #Extract the first stored element of the queue
        row, col = current_ind

        #Printing actual path
        stdscr.clear()
        print_maze(maze,stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        #End Condition
        if maze[row][col] == end_str:
            return path
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors: #Loop through all neighbors
            if neighbor in visited: #Invalid neighbor
                continue
            r,c = neighbor
            if maze[r][c] == '#': #Invalid neighbor
                continue
            new_path = path + [neighbor] #Add valid neighbor to the path 
            q.put((neighbor, new_path)) #Put neighbor and it's path on the queue
            visited.add(neighbor) #Add the neighbor to the visited ones
    return None #If we exit the while loop without find 'X' 



def main(stdscr): #stdscr: standard screen => Creates an screen on the terminal till the program finishes
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #Blue font and Black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  #Red font and Black background
    
    path = find_path(maze, stdscr)
    stdscr.getch() #Waiting for a key to be pressed to pass this line
    print('Path solution to the maze:\n', path)


if __name__ == '__main__':
    curses.wrapper(main)  #Initializes curses screen and calls main function
