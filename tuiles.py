import pygame
from random import seed
from random import randint
import time

# seed random number generator
seed(time.time())

display_width = 1280
display_height = 800

tile_width = 50
tile_height = 1.6*tile_width
board_col_nb = 25
board_row_nb = 10

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
pygame.display.set_caption('Tuiles')
clock = pygame.time.Clock()

class Tile:
    """ Represents a Tile in space """
    i = 0
    j = 0
    rect = pygame.Rect(0,0,0,0)
    color = color_red

    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.rect = pygame.Rect((i*tile_width,j*tile_height),(tile_width, tile_height))
        self.color = color

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, pygame.Rect(self.rect))

    def move(self, i, j):
        self.i = i
        self.j = j
        self.rect = pygame.Rect((i*tile_width,j*tile_height),(tile_width, tile_height))

    def is_in_place(self):
        return self.rect.x == self.i*tile_width and self.rect.y == self.j*tile_height

    def fall_to(self, i, j):
        """Draws the tile falling toward (i,j)"""
        if self.rect.y >= j*tile_height:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x,curr_y + 5),(tile_width, tile_height))
            return False

    def slide_left_to(self, i, j):
        """Draws the tile sliding left toward (i,j)"""
        if self.rect.x <= i*tile_width:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x - 5,curr_y),(tile_width, tile_height))
            return False

    def  __str__(self):
        return "("+str(self.i)+","+str(self.j)+") is_in_place : "+str(self.is_in_place())

board = []

###
# Populates the board with random color tiles
###
def initialize_board():
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
# Creates a dictionary with the column index as keys, and a list of the tiles and their destination as values
# Like so : {COLUMN_NUMBER: [(TILE, (DESTINATION_I, DESTINATION_J)), (TILE2, (DESTINATION2_I, DESTINATION2_J)), ...]}
###
def compute_downward_movements(affected_columns):
    moves = {}
    for i in affected_columns:
        moves[i] = []
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
                moves[i].append((board[i][j], (i,j+empty_tiles)))
                found_space = False
    return moves

###
# Applies the moves from the moves_dict (see compute_downward_movements)
# return a bool indicating if the tiles are in their respective place
###
def move_tiles_downward(moves_dict):
    tiles_in_place = True
    for k in moves_dict.keys():
        for (t, (dest_i, dest_j)) in moves_dict[k]:
            if t.fall_to(dest_i,dest_j):
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
                    moves.append((board[i][j], (i -nb_empty_col ,j)))
            found_space = False
    return moves

###
# Applies the moves from the moves list (see compute_side_movements)
###
def move_tiles_sideway(moves):
    tiles_in_place = True
    for (t, (dest_i, dest_j)) in moves:
        if t.slide_left_to(dest_i,dest_j):
            board[t.i][t.j] = None
            board[dest_i][dest_j] = t
            t.move(dest_i, dest_j)
        else:
            tiles_in_place = False

    return tiles_in_place

def game_loop():
    game_over = False #TODO define function to calculate winning state
    tile_on_mouse_down = Tile(-1,-1,color_white)
    processing_movements = False
    processing_falling_movements = False
    processing_sliding_movements = False
    downward_moves = {}
    sideway_moves = []
    while not game_over:
        gameDisplay.fill(background) #In lieu of picture
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if not processing_movements:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_tile = get_tile_from_coord(pos)
                if clicked_tile is not None:
                    tile_on_mouse_down = clicked_tile
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_tile = get_tile_from_coord(pos)
                if clicked_tile is not None and clicked_tile == tile_on_mouse_down:
                    tile_on_mouse_down = Tile(-1,-1,color_white)
                    (connected, aff_columns) = get_connected_tiles(clicked_tile)
                    for c in connected:
                        board[c.i][c.j] = None
                    processing_movements = True
                    processing_falling_movements = True
                    downward_moves = compute_downward_movements(aff_columns)
        else:
            if processing_falling_movements and not processing_sliding_movements:
                processing_falling_movements = not move_tiles_downward(downward_moves)
            if not processing_falling_movements:
                if not processing_sliding_movements:
                    sideway_moves = compute_side_movements()
                    if sideway_moves != []:
                        processing_sliding_movements = True
                else:
                    processing_sliding_movements = not move_tiles_sideway(sideway_moves)
            processing_movements = processing_falling_movements or processing_sliding_movements

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

#
initialize_board()
game_loop()