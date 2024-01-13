import pygame
import math
from queue import PriorityQueue

pygame.init()
font = pygame.font.Font(None, 32)

WIDTH = 600
TEXT_HEIGHT = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH + TEXT_HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('helvetica', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

# colors
RED = (255, 0, 0) #closed
GREEN = (0, 255, 0) #open
BLUE = (0, 0, 255) 
YELLOW = (255, 255, 0) #path
WHITE = (255, 255, 255) #empty
BLACK = (0, 0, 0) #barrier
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0) #start
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208) #end

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.f_score = float("inf")
        self.g_score = float("inf")

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # top-left
            self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier(): # top-right
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): # bottom-left
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # bottom-right
            self.neighbors.append(grid[self.row + 1][self.col + 1])

    def __lt__(self, other):
        return self.f_score < other.f_score
    
# heuristic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #euclidean distance
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# draw shortest path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        next_node = came_from[current]
        if next_node not in came_from:  # Stop if the next node is the start node
            break
        current = next_node
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    open_set = PriorityQueue() # open set
    open_set.put((0, start)) # add start node to open set
    came_from = {} # dictionary to keep track of path
    start.g_score = 0
    start.f_score = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} # keep track of items in priority queue

    # loop open set until empty
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[1] # get node with lowest f score
        open_set_hash.remove(current) # remove node from open set

        if current == end: # path found
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors: # check neighbors of current node
            if neighbor.row == current.row or neighbor.col == current.col:
                temp_g_score = current.g_score + 1 
            else:
                temp_g_score = current.g_score + 1.4 # diagonal g score

            # if g score is less than current g score
            if temp_g_score < neighbor.g_score: 
                came_from[neighbor] = current 
                neighbor.g_score = temp_g_score 
                neighbor.f_score = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
                if neighbor not in open_set_hash: # if neighbor is not in open set
                    open_set.put((neighbor.f_score, neighbor)) 
                    open_set_hash.add(neighbor) 
                    neighbor.make_open() # make neighbor open
        
        draw()

        if current != start: # if current node is not start node
            current.make_closed() # make current node closed

    return False

# make grid array
def make_grid(rows, width):
    grid = []
    gap = width // rows # integer division
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows) # create node object
            grid[i].append(node)
    return grid

# draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows 
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # vertical lines

# update display
def draw(win, grid, rows, width):
    win.fill(WHITE) # fill window with white
    for row in grid: # draw each node
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width) # draw grid lines

    # Draw buttons
    astar_btn = Button(GREY, 20, WIDTH + 10, 50, 30, 'A*')
    dijkstra_btn = Button(GREY, 80, WIDTH + 10, 80, 30, 'Dijkstra')
    astar_btn.draw(win)
    dijkstra_btn.draw(win)

    # Draw text box
    font = pygame.font.Font(None, 20)
    lines = [
        'press SPACE to start program, or ENTER to clear board',
        'Add start and end nodes, and barriers',
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, BLACK, WHITE)
        text_rect = text.get_rect()
        text_rect.topleft = (dijkstra_btn.x + dijkstra_btn.width + 10, win.get_rect().bottom - 20 - (i * 22))
        win.blit(text, text_rect)

    pygame.display.update()

# get mouse position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue

            # left mouse button
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                if pos[1] > WIDTH:
                    pass
                else:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()

            # right mouse button
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                # check if mouse is in text box
                if pos[1] > WIDTH:
                    pass
                else:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                    node.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_RETURN:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)