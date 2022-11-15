import os, sys, queue
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Hide the pygame welcome printing
DIRPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRPATH)
import pygame

#this is just for the lols
#Display settings
WIDTH = 7000
ROWS = 63
ICON = 'labyrinth.ico'
CAPTION = 'A* - Path Finding Algorithm'
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))
pygame.display.flip()

#Define Colors RGB
RED = (255,0,0); GREEN = (0,255,0); BLUE = (0,0,255)
YELLOW = (255,255,0); WHITE = (255,255,255)
BLACK = (0,0,0); PURPLE = (128,0,128); ORANGE = (255,165,0)
GREY = (128,128,128); TURQUOISE = (64,224,208)

class Node:
    """Create the Node class as a cell of a 2D grid"""
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def getPosition(self):
        return self.row, self.col
    
    def isClosed(self):
        return self.color == RED
    def isOpen(self):
        return self.color == GREEN
    def isBarrier(self):
        return self.color == BLACK
    def isStart(self):
        return self.color == ORANGE
    def isEnd(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
    def setClosed(self):
        self.color = RED
    def setOpen(self):
        self.color = GREEN
    def setBarrier(self):
        self.color = BLACK
    def setStart(self):
        self.color = ORANGE
    def setEnd(self):
        self.color = TURQUOISE
    def setPath(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x,self.y,self.width,self.width))
    
    def updateNeighbors(self,grid):
        self.neighbors = []
        if (self.row < self.total_rows-1) and not (grid[self.row+1][self.col].isBarrier()): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if (self.row > 0) and not (grid[self.row-1][self.col].isBarrier()): #UP
            self.neighbors.append(grid[self.row-1][self.col])

        if (self.col < self.total_rows-1) and not (grid[self.row][self.col+1].isBarrier()): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if (self.col > 0) and not (grid[self.row][self.col-1].isBarrier()): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other): #Compare Nodes
        return False

def distance(p1, p2):
    """Approximate distance between points"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def createGrid(rows, width):
    """Initializes the grid"""
    grid = []
    gap = width//rows #Width of each node
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def drawGrid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0,i*gap), (width,i*gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j*gap,0), (j*gap,width))

def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)
    drawGrid(window, rows, width)
    pygame.display.update()

def getClickPosition(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x//gap
    col = y//gap
    return row, col

def reconstructPath(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.setPath()
        draw()



def algorithm(draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = distance(start.getPosition(), end.getPosition())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get(): #If I need to quit while algo is working
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstructPath(came_from, end, draw)
            end.setEnd()
            start.setStart()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + distance(neighbor.getPosition(), end.getPosition())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.setOpen()

        draw()

        if current != start:
            current.setClosed()
        
    return False


def main(window, width, ROWS):
    grid = createGrid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get(): #Loop through all events
            
            if event.type == pygame.QUIT: #Closing the window
                run = False

            if pygame.mouse.get_pressed()[0]:#Left-click
                pos = pygame.mouse.get_pos()
                row, col = getClickPosition(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    node.setStart()
                elif not end and node != start:
                    end = node
                    node.setEnd()
                elif node != start and node != end:
                    node.setBarrier()

            elif pygame.mouse.get_pressed()[2]:#Right-click
                pos = pygame.mouse.get_pos()
                row, col = getClickPosition(pos, ROWS, width)
                node = grid[row][col]
                if node == start:
                    start = None
                if node == end:
                    end = None
                node.reset()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid) 
                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = createGrid(ROWS, width)
    
    pygame.quit()
    sys.exit()



main(WINDOW, WIDTH, ROWS)