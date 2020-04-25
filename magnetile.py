import pygame
from random import seed
from random import randint
import time
import enum

# seed random number generator
seed(time.time())

display_width = 1280
display_height = 800

tile_width = 50
tile_height = 1.6*tile_width
board_col_nb = 18
board_row_nb = 9
#board_col_nb = 6 #FOR TESTING
#board_row_nb = 2 #FOR TESTING

tool_bar_height = 50

color_black = (0,0,0)
color_white = (255,255,255)
color_gray = (175, 185, 204)
color_red = (237, 125, 119)
color_green = (119, 237, 131)
color_blue = (119, 160, 237)
color_yellow = (237, 215, 119) 
background = color_white

##########RAND
colors_rand_arr = [color_red, color_green, color_blue, color_yellow]
def get_random_color():
    r = randint(0, 3)
    return colors_rand_arr[r]
##############

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('MagneTile')
clock = pygame.time.Clock()

class Tile:
    """ Represents a Tile in space """
    x_offset = 0
    y_offset = tool_bar_height
    i = 0
    j = 0
    rect = pygame.Rect(0,0,0,0)
    color = color_red

    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.rect = pygame.Rect((i*tile_width + self.x_offset,j*tile_height + self.y_offset),(tile_width, tile_height))
        self.color = color

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, pygame.Rect(self.rect))

    def move(self, i, j):
        self.i = i
        self.j = j
        self.rect = pygame.Rect((i*tile_width + self.x_offset,j*tile_height + self.y_offset),(tile_width, tile_height))

    def is_in_place(self):
        return self.rect.x == self.i*tile_width and self.rect.y == self.j*tile_height

    def fall_to(self, i, j):
        """Draws the tile falling toward (i,j)"""
        if self.rect.y >= j*tile_height + self.y_offset:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x,curr_y + 5),(tile_width, tile_height))
            return False

    def slide_left_to(self, i, j):
        """Draws the tile sliding left toward (i,j)"""
        if self.rect.x <= i*tile_width + self.x_offset:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x - 5,curr_y),(tile_width, tile_height))
            return False

    def  __str__(self):
        return "TILE("+str(self.i)+","+str(self.j)+")"

class Tile_Movement():
    tile = Tile(0,0,color_white)
    from_source = (0,0)
    to_dest = (0,0)

    def __init__(self, tile, dest):
        self.tile = tile
        self.from_source = (tile.i, tile.j)
        self.to_dest = dest

    def __str__(self):
        return "Movement from "+str(self.tile)+" to "+str(self.to_dest)

class Text_Button:
    x = 0
    y = 0
    text_color = color_black
    background_color = color_white
    rect = pygame.Rect(0,0,0,0)
    btn_render = None

    def __init__(self, x, y, text):
        """ (x,y) are coordinated of center of the button"""
        font_btn = pygame.font.SysFont('Comic Sans MS', 30)
        self.btn_render = font_btn.render(text, True, self.text_color, self.background_color)
        width = self.btn_render.get_rect().width
        height = self.btn_render.get_rect().height
        print ("INNER height "+str(height))
        self.x = x - width / 2
        self.y = y - height / 2
        self.rect = pygame.Rect(self.x,self.y,width,height)

    def draw(self):
        gameDisplay.blit(self.btn_render,(self.x,self.y))

    def collides_with(self, coord):
        return self.rect.collidepoint(coord)

class History_Step:
    cluster = []
    neighbors_moves = [] #Tile_Movement list

    def __init__(self, cluster):
        self.cluster = cluster
        self.neighbors_moves = []

    def add_move(self, tile, dest):
        self.neighbors_moves.append(Tile_Movement(tile, dest))

    def add_moves(self, moves):
        self.neighbors_moves = self.neighbors_moves + moves

class History:
    steps = []

    def __init__(self):
        self.steps = []

    def get_current_step(self):
        if self.steps == []:
            return None
        else:
            return self.steps[-1]

    def undo_last_step(self):
        return self.steps.pop()

    def add_new_step(self, cluster):
        self.steps.append(History_Step(cluster))

    def add_tile_movements_to_current_step(self,moves):
        curr = self.get_current_step()
        if curr != None:
            self.get_current_step().add_moves(moves)

class GameOver(enum.Enum):
   WIN = 1
   LOSE = 2
   PLAYING = 3

class Direction(enum.Enum):
   LEFT = 1
   UP = 2
   RIGHT = 3
   DOWN = 4

board = []
restart_button = Text_Button(display_width / 2, display_height / 2 , "Restart")
undo_button = Text_Button(display_width / 2, 15 , "Undo")

###
# Populates the board with random color tiles
###
def initialize_board():
    global board
    board = []
    for i in range(board_col_nb):
        board.append([])
        for j in range(board_row_nb):
            board[i].append(Tile(i,j,get_random_color()))

###
# Draws the board on the surface
###
def draw_board():
    for i in range(board_col_nb):
        for j in range(board_row_nb):
            if board[i][j] is not None:
                board[i][j].draw()

###
# Get the tile that matches the coordinates, or None if no tiles are found 
###
def get_tile_from_coord(coord):
    for i in range(board_col_nb):
        for j in range(board_row_nb):
            if board[i][j] is not None and board[i][j].rect.collidepoint(coord):
                return board[i][j]
    return None

###
# Get the neighbors of a tile that are of the same color
###
def get_tile_same_color_neighbors(tile):
    i = tile.i
    j = tile.j

    n = []
    coord_to_check = []

    if i > 0:
        if i < len(board) - 1:
            if j > 0:
                if j < len(board[0]) - 1:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i,j+1))
                    coord_to_check.append((i-1,j))
                    coord_to_check.append((i+1,j))
                else:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i-1,j))
                    coord_to_check.append((i+1,j))
            else:
                coord_to_check.append((i,j+1))
                coord_to_check.append((i-1,j))
                coord_to_check.append((i+1,j))
        else:
            if j > 0:
                if j < len(board[0]) - 1:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i,j+1))
                    coord_to_check.append((i-1,j))
                else:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i-1,j))
            else:
                coord_to_check.append((i,j+1))
                coord_to_check.append((i-1,j))
    else:
        if j > 0:
                if j < len(board[0]) - 1:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i,j+1))
                    coord_to_check.append((i+1,j))
                else:
                    coord_to_check.append((i,j-1))
                    coord_to_check.append((i+1,j))
        else:
            coord_to_check.append((i,j+1))
            coord_to_check.append((i+1,j))

    for c in coord_to_check:
        tile_to_check = board[c[0]][c[1]]
        if tile_to_check is not None and tile_to_check.color == tile.color:
            n.append(tile_to_check)

    return n

connected_neighbors = set()
affected_columns = set()
###
# Depth first search algoritm to get the tiles of the sale color
###
def dfs(visited, tile):
    if tile not in visited:
        visited.add(tile)
        connected_neighbors.add(tile)
        affected_columns.add(tile.i)
        for neighbour in get_tile_same_color_neighbors(tile):
            dfs(visited, neighbour)

def get_connected_tiles(tile):
    global connected_neighbors
    global affected_columns
    connected_neighbors = set()
    affected_columns = set()
    dfs(set(),tile)
    return (connected_neighbors, affected_columns)


###
# Creates list of Tile_movement representing a move the tiles need to make
###

def compute_downward_movements(affected_columns):
    moves = []
    for i in affected_columns:
        dest_j = 0
        found_space = False
        empty_tiles = 0
        for j in range(len(board[i]) - 1, -1, -1): 
            if board[i][j] is None and not found_space:
                dest_j = j
                found_space = True
            if board[i][j] is not None and found_space:
                empty_tiles = empty_tiles + (dest_j - j)
            if board[i][j] is not None and empty_tiles != 0:
                moves.append(Tile_Movement(board[i][j],(i,j+empty_tiles)))
                found_space = False
    return moves
###
# Applies the moves from the list of Tile_Movement(see compute_downward_movements)
# return a bool indicating if the tiles are in their respective place
###
def move_tiles(moves, direction):
    tiles_in_place = True
    for m in moves:
        t = m.tile
        (dest_i, dest_j) = m.to_dest
        finished = False

        if direction == Direction.DOWN:
            finished = t.fall_to(dest_i,dest_j)
        if direction == Direction.LEFT:
            finished = t.slide_left_to(dest_i,dest_j)

        if finished:
            board[t.i][t.j] = None
            board[dest_i][dest_j] = t
            t.move(dest_i, dest_j)
        else:
            tiles_in_place = False
                
    return tiles_in_place
###
# Return a list of tuple representing a move like so : [(TILE, (MOVE_I, MOVE_J)), (TILE2, (MOVE2_I, MOVE2_J)), ...] or [] if no empty columns are found
###
def compute_side_movements():
    moves = []
    found_space = False
    dest_i = 0
    nb_empty_col = 0
    for i in range(len(board)):
        max_j = len(board[i]) - 1
        if board[i][max_j] is None and not found_space:
            dest_i = i
            found_space = True
        if board[i][max_j] is not None and found_space:
            nb_empty_col = nb_empty_col + (i - dest_i)
        if board[i][max_j] is not None and nb_empty_col != 0:
            for j in range(len(board[i])):
                if board[i][j] is not None:
                    moves.append(Tile_Movement(board[i][j], (i - nb_empty_col ,j)))
            found_space = False
    return moves

###
# Undo the last step of the history
###
def undo_step(history):
    if history == [] or history.steps == []:
        return
    last_step = history.undo_last_step()
    for m in last_step.neighbors_moves:
        t = m.tile
        (from_i, from_j) = m.from_source
        t.move(from_i, from_j)
        board[from_i][from_j] = t
    for t in last_step.cluster:
        board[t.i][t.j] = t

###
# Checks the whole board is the game is over (won or lost)
###
def check_game_over():
    tiles_checked = []
    nb_clusters = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            curr_tile = board[i][j]
            if curr_tile is not None and not curr_tile in tiles_checked:
                (cluster, _) = get_connected_tiles(curr_tile)
                if len(cluster) > 1:
                    nb_clusters = nb_clusters + 1
                for t in cluster:
                    tiles_checked.append(t)

    if nb_clusters == 0:
        if len(tiles_checked) == 0:
            return GameOver.WIN
        else:
            return GameOver.LOSE
    else:
        return GameOver.PLAYING

def display_end_panel(msg, color, font):
    text = font.render(msg, True, color, color_white)

    x = display_width / 2 -  (text.get_rect().width / 2)
    y = display_height / 2 - (text.get_rect().height / 2) - (restart_button.rect.height) - 10
    gameDisplay.blit(text,(x,y))

    restart_button.draw()

def display_win_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    display_end_panel("YOU WIN !! :)", color_red, font)

def display_lose_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    display_end_panel("(you lose) :(", color_black, font)

def display_end_screen(game_over):
    if game_over == GameOver.WIN:
        display_win_screen()
    if game_over == GameOver.LOSE:
        display_lose_screen()
    

def game_loop():
    game_over = GameOver.PLAYING 
    app_running = True
    tile_on_mouse_down = Tile(-1,-1,color_white)
    button_on_mouse_down = None
    processing_movements = False
    processing_falling_movements = False
    processing_sliding_movements = False
    downward_moves = {}
    sideway_moves = []
    history = History()
    while app_running:
        gameDisplay.fill(background) #In lieu of picture
        draw_board()
        undo_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

        if game_over == game_over.PLAYING:
            if not processing_movements:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_tile = get_tile_from_coord(pos)
                    if clicked_tile is not None:
                        tile_on_mouse_down = clicked_tile
                    
                    if undo_button.collides_with(pos):
                        button_on_mouse_down = undo_button

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_tile = get_tile_from_coord(pos)
                    if clicked_tile is not None and clicked_tile == tile_on_mouse_down:
                        tile_on_mouse_down = Tile(-1,-1,color_white)
                        (connected, aff_columns) = get_connected_tiles(clicked_tile)
                        if len(connected) > 1:
                            for c in connected:
                                board[c.i][c.j] = None
                            history.add_new_step(connected)
                            processing_movements = True
                            processing_falling_movements = True
                            downward_moves = compute_downward_movements(aff_columns)

                    if undo_button.collides_with(pos) and button_on_mouse_down == undo_button:
                        button_on_mouse_down = None
                        undo_step(history)
            else:
                if processing_falling_movements and not processing_sliding_movements:
                    processing_falling_movements = not move_tiles(downward_moves, Direction.DOWN)
                if not processing_falling_movements:
                    if not processing_sliding_movements:
                        sideway_moves = compute_side_movements()
                        if sideway_moves != []:
                            processing_sliding_movements = True
                    else:
                        processing_sliding_movements = not move_tiles(sideway_moves, Direction.LEFT)
                processing_movements = processing_falling_movements or processing_sliding_movements

                if not processing_movements:
                    # Finished moving tiles
                    game_over = check_game_over()
                    history.add_tile_movements_to_current_step(sideway_moves)
                    history.add_tile_movements_to_current_step(downward_moves)

        else:
            display_end_screen(game_over)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.collides_with(pos):
                    # Restarts the game
                    initialize_board()
                    history = History()
                    game_over = GameOver.PLAYING
                    print("RESTART")

        pygame.display.update()
        clock.tick(60)

    

    pygame.quit()
    quit()

#
initialize_board()
game_loop()