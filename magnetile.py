import sys
import os
import getopt
import time
import enum
import pygame
from random import seed
from random import randint

french_text_map = {
    "undo" : "Annuler",
    "restart" : "Rejouer",
    "you_won" : "Vous avez gagné !! :)",
    "you_lost" : "Vous avez perdu"
}

english_text_map = {
    "undo" : "Undo",
    "restart" : "Play again",
    "you_won" : "You won !! :)",
    "you_lost" : "You lost"
}

text_map = english_text_map

def print_help():
    print ("usage : magnetile.py [-l language]")
    print ("        Languages are : french or english (default)")

try:
    options, remainder = getopt.getopt(sys.argv[1:],"hl:",["language=","--help"])
except getopt.GetoptError:
    print_help()
    sys.exit(2)

for opt, arg in options: 
    if opt in ("-l","--language"):
        if arg == "french":
            text_map = french_text_map
        else:
            print ("Languages are : french or english (default)")
            sys.exit(2)
    if opt in ("-h", "--help"):
        print_help()

# seed random number generator
seed(time.time())
fps = 60

display_width = 850
display_height = 750

tile_width = 45
tile_height = int(1.6*tile_width)
board_col_nb = 18
board_row_nb = 9
#board_col_nb = 6 #FOR TESTING
#board_row_nb = 2 #FOR TESTING

tool_bar_height = 50

#to center the grid in the window
offset_x_grid = (display_width - (board_col_nb*tile_width)) / 2

class Color(enum.Enum):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GRAY = (175, 185, 204)
    RED = (237, 125, 119)
    GREEN = (119, 237, 131)
    BLUE = (119, 160, 237)
    YELLOW = (237, 215, 119)
    PURPLE = (182, 3, 252)

side_width = 10
bottom_height = 10
tile_image_center_size = (tile_width, tile_height)
tile_image_side_size = (side_width, tile_height)
tile_image_side_bottom = (tile_width, bottom_height)
tile_image_side_corner = (side_width, bottom_height)
tiles_images = {
    Color.RED : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "red_tile_center.png")), tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "red_tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "red_tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "red_tile_corner.png")),tile_image_side_corner),
        },
    Color.GREEN : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "green_tile_center.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "green_tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "green_tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "green_tile_corner.png")),tile_image_side_corner),
        },
    Color.BLUE : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "blue_tile_center.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "blue_tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "blue_tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "blue_tile_corner.png")),tile_image_side_corner),
        },
    Color.YELLOW : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "yellow_tile_center.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "yellow_tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "yellow_tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "yellow_tile_corner.png")),tile_image_side_corner),
        },
    Color.PURPLE : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "purple_tile_center.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "purple_tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "purple_tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join("images", "tmp", "purple_tile_corner.png")),tile_image_side_corner),
        }
}

background_color = Color.WHITE

###
# Picks a random color
###
colors_rand_arr = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
def get_random_color():
    r = randint(0, 3)
    return colors_rand_arr[r]

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('MagneTile')
clock = pygame.time.Clock()

class Custom_Range:
    start = 0
    end = 0
    length = 0

    def __init__(self, start, end):
        self.start = start if start <= end else end 
        self.end = end if start <= end else start 
        self.length = self.end - self.start

    def is_overlaping(self, o_range):
        res = False
        if self.start < o_range.start:
            if o_range.start <= self.end:
                res = True
        else:
            if self.start <= o_range.end:
                res = True
        return res

    def union(self, o_range):
        if self.is_overlaping(o_range):
            return Custom_Range(min(self.start, o_range.start), max(self.end, o_range.end))
        else:
            return None

    def get_range(self):
        return range(self.start, self.end + 1)

    def __str__(self):
        return "("+str(self.start)+","+str(self.end)+")"

class Tile_Image(pygame.sprite.Sprite):
    """ Represents a tile image to be displayed on screen"""

    side_image = None
    bottom_image = None
    corner_image = None

    def __init__(self, color, coord):
        super().__init__()
        self.image = tiles_images[color]["center"]
        self.side_image = tiles_images[color]["side"]
        self.bottom_image = tiles_images[color]["bottom"]
        self.corner_image = tiles_images[color]["corner"]
        self.rect = self.image.get_rect()
        (x,y) = coord
        self.rect.x = x
        self.rect.y = y

    def move (self, coord):
        (x, y) = coord
        self.rect.x = x
        self.rect.y = y

    def draw(self, coord):
        gameDisplay.blit(self.image, coord)

    def draw_side(self):
        coord = (self.rect.right, self.rect.y)
        gameDisplay.blit(self.side_image, coord)

    def draw_bottom(self):
        coord = (self.rect.x, self.rect.bottom)
        gameDisplay.blit(self.bottom_image, coord)

    def draw_corner(self):
        coord = (self.rect.right, self.rect.bottom)
        gameDisplay.blit(self.corner_image, coord)

class Tile:
    """ Represents a Tile in space """
    x_offset = offset_x_grid
    y_offset = tool_bar_height
    i = 0
    j = 0
    tile_image = None
    rect = pygame.Rect(0,0,0,0)
    color = None # /!\ Color enum (not Tuple)
    speed = 6 # speed when drawing
    k = 1.05 # acceleration factor

    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        x = i*tile_width + self.x_offset
        y = j*tile_height + self.y_offset
        self.rect = pygame.Rect((x,y),(tile_width, tile_height))
        self.color = color
        self.tile_image = Tile_Image(color, (x,y))

    def get_supposed_coord(self):
        return (self.i*tile_width + self.x_offset, self.j*tile_height + self.y_offset)

    def get_coord_from_grid_pos(self, i, j):
        return (i*tile_width + self.x_offset, j*tile_height + self.y_offset)

    def draw(self):
        self.tile_image.draw((self.rect.x, self.rect.y))
        #pygame.draw.rect(gameDisplay, self.color.value, pygame.Rect(self.rect))

    def move(self, i, j):
        self.i = i
        self.j = j
        x = i*tile_width + self.x_offset
        y = j*tile_height + self.y_offset
        self.rect = pygame.Rect((x,y),(tile_width, tile_height))
        self.tile_image.move((x, y)) 

    def is_in_place(self):
        (x,y) = self.get_coord_from_grid_pos()
        return self.rect.x == x and self.rect.y == y

    def __accelerate(self):
        self.speed *= self.k

    def __stop_speed(self):
        self.speed = 6

    def fall_to(self, i, j):
        (x,y) = self.get_coord_from_grid_pos(i,j)
        """Draws the tile falling toward (i,j), only the rectangle that represent the tile is moving, not the (i,j) coordinates"""
        if self.rect.y + self.speed >= y:
            self.__stop_speed()
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.__accelerate()
            self.rect = pygame.Rect((curr_x,curr_y + self.speed),(tile_width, tile_height))
            self.tile_image.move((curr_x,curr_y + self.speed))
            return False

    def slide_left_to(self, i, j):
        """Draws the tile sliding left toward (i,j), same as fall_to(self, i, j)"""
        (x,y) = self.get_coord_from_grid_pos(i,j)
        if self.rect.x - self.speed <= x:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x - self.speed,curr_y),(tile_width, tile_height))
            self.tile_image.move((curr_x - self.speed,curr_y))
            return False

    def  __str__(self):
        return "TILE("+str(self.i)+","+str(self.j)+")"

class Tile_Movement():
    tile = None
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
    text_color = Color.BLACK.value
    background_color = Color.WHITE.value
    rect = pygame.Rect(0,0,0,0)
    btn_render = None

    border_thickness = 2
    border_color = Color.BLACK.value
    border_padding = 5

    def __init__(self, x, y, text):
        """ (x,y) are the coordinates of the button's center"""
        font_btn = pygame.font.SysFont('Comic Sans MS', 30)
        self.btn_render = font_btn.render(text, True, self.text_color, self.background_color)
        width = self.btn_render.get_rect().width
        height = self.btn_render.get_rect().height
        self.x = x - width / 2
        self.y = y - height / 2
        self.rect = pygame.Rect(self.x,self.y,width,height)

    def __draw_border(self):
        border_with = self.rect.width + self.border_thickness * 8 + self.border_padding * 2
        border_height = self.rect.height +  self.border_thickness * 2

        border_rect = pygame.Rect((self.x - self.border_thickness *4 - self.border_padding, self.y - self.border_thickness),(border_with, border_height))
        mask_rect = pygame.Rect((border_rect.x + self.border_thickness *4, border_rect.y + self.border_thickness),(border_rect.width - self.border_thickness * 8, border_rect.height - self.border_thickness * 2))
        pygame.draw.rect(gameDisplay, self.border_color, pygame.Rect(border_rect))
        pygame.draw.rect(gameDisplay, self.background_color, pygame.Rect(mask_rect))


    def draw(self):
        self.__draw_border()
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

class Game_Over(enum.Enum):
   WIN = 1
   LOSE = 2
   PLAYING = 3

class Direction(enum.Enum):
   LEFT = 1
   UP = 2
   RIGHT = 3
   DOWN = 4

class Perspective(enum.Enum):
   SIDE = 1
   BOTTOM = 2
   CORNER = 3

board = []
restart_button = Text_Button(display_width / 2, display_height / 2 , text_map["restart"])
undo_button = Text_Button(display_width / 2, 25 , text_map["undo"])


###
# Get the tile that matches the coordinates, or None if no tiles are found 
###
def get_tile_from_coord(coord):
    for i in range(len(board)):
        for j in range(len(board[i])):
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
###
# Depth first search algoritm to get the tiles of the sale color
###
def dfs(visited, tile):
    if tile not in visited:
        visited.add(tile)
        connected_neighbors.add(tile)
        for neighbour in get_tile_same_color_neighbors(tile):
            dfs(visited, neighbour)

def get_connected_tiles(tile):
    global connected_neighbors
    connected_neighbors = set()
    dfs(set(),tile)
    return connected_neighbors

###
# Sorts a list of tiles regarding their position in the grid : left to right first, then top to bottom
###
def convert_tile_position_for_comparison(tile):
    return tile.i + len(board) * tile.j

def sort_tiles(list_tiles, rev=False):
    return sorted(list_tiles,key=convert_tile_position_for_comparison, reverse=rev)

def convert_side_to_draw_for_comparison(std):
    (sides_bool_arr, tile) = std
    return tile.i + len(board) * tile.j

def sort_sides_to_draw(list_sides_to_draw): # [ ([], TILE), ([], TILE), ([], TILE), ... ]
    return sorted(list_sides_to_draw,key=convert_side_to_draw_for_comparison)

###
# Creates list of Tile_movement representing a move the tiles need to make
###

def compute_downward_movements(connected_tiles):

    columns = {t.i for t in connected_tiles}
    moves = []
    for i in columns:
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
# Draws the list of rectangle bg_to_draw on the screen
###
def draw_background_tiles(bg_to_draw):
    for r in bg_to_draw:
        pygame.draw.rect(gameDisplay, background_color.value, r)

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
        t.draw()
    for t in last_step.cluster:
        board[t.i][t.j] = t
        t.draw()

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
                cluster = get_connected_tiles(curr_tile)
                if len(cluster) > 1:
                    nb_clusters = nb_clusters + 1
                for t in cluster:
                    tiles_checked.append(t)

    if nb_clusters == 0:
        if len(tiles_checked) == 0:
            return Game_Over.WIN
        else:
            return Game_Over.LOSE
    else:
        return Game_Over.PLAYING

###
# Get a list of background rectangles to draw from a list of moves for the falling of the tiles
###
def compute_background_to_draw(moves):
    res = []
    for m in moves:
        t = m.tile
        res.append(t.rect)
    return res

###
# Get a list of background rectangles to draw from a list of moves for the sliding of the tiles
###
def compute_background_to_draw_for_sliding(moves):
    rect_to_draw = []
    range_dict = {} # keys : line number | values : list of range of movements
    for m in moves:
        t = m.tile
        (i,j) = (t.i, t.j)
        from_i = m.from_source[0]
        to_i = m.to_dest[0]
        mov_range = Custom_Range(to_i, from_i)
        if not j in range_dict.keys():
            range_dict[j] = [mov_range]
        else:
            add_range = True
            for r in range_dict[j]:
                union = r.union(mov_range)
                if union is not None:
                    r.start = union.start
                    r.end = union.end
                    add_range = False
            if add_range:
                range_dict[j].append(mov_range)

    for j in range_dict.keys():
        for r in range_dict[j]:
            for i in r.get_range():
                tile = board[i][j]
                if tile is not None:
                    rect_to_draw.append(tile.rect)

    return rect_to_draw

###
# Returns a list of tiles that represent the 'edge' of the (removed + moving) tiles
###
def compute_edge(tile_list, comparator):
    edge = {} # dictionary : {ROW_NUMBER : TILE_WITH_MINIMUM_OR_MAXIMUM_COLUMN_NUMBER}

    for t in tile_list:
        if t.j not in edge.keys():
            edge[t.j] = t
        else:
            curr_min_tile = edge[t.j]
            if comparator(t.i, curr_min_tile.i):
                edge[t.j] = t

    sorted_edge = sort_tiles(edge.values(), True)
    i_threshold = sorted_edge[0].i
    curated_edge = []
    for t in sorted_edge:
        if comparator(t.i, i_threshold):
            i_threshold = t.i
            curated_edge.append(t)

    return curated_edge

def compute_edge_side_background(sorted_tile_list):
    edge = [] 
    last_tile = sorted_tile_list[0]
    max_j = last_tile.j
    for t in sorted_tile_list:
        if t.j != last_tile.j: # new line
            if last_tile.j > max_j:
                max_j = last_tile.j
            # add last tile to edge
            edge.append(last_tile)
        if t.i != last_tile.i or t.i != last_tile.i + 1: # gap in line
            # add to edge
            edge.append(last_tile)
        last_tile = t

    curated_edge = []
    for t in reversed(edge):
        if t.j <= max_j:
            curated_edge.append(t)

    return curated_edge

def compute_left_edge(tile_list):
    return compute_edge(tile_list, lambda i1,i2 : i1 <= i2)

def compute_right_edge(tile_list):
    return compute_edge(tile_list, lambda i1,i2 : i1 >= i2)

###
# return a dictionary of the corners of an edge (see above)
###
def compute_corners_of_edge(sorted_edge_list):
    corners = {}
    for t in sorted_edge_list:
        if not t.i in corners.keys():
            corners[t.i] = t
        else:
            if t.j > corners[t.i].j:
                corners[t.i] = t

    return corners 

def compute_side_background_to_draw(sorted_edge_list):
    bg_to_draw = [] # list of rect
    for t in sorted_edge_list:
        if (t.i == len(board) - 1) or (board[t.i + 1][t.j] is None):
            bg_to_draw.append(pygame.Rect((t.rect.right, t.rect.top),(side_width,t.rect.height)))
            print("BACKGROUNg TILE TO DRAW : "+str(t.rect.right) + ","+ str(t.rect.top) + "," + str(side_width) + "," + str(t.rect.height))
    return bg_to_draw

###
# Return a list of sides to draw from the removed tiles and the affected tiles that will fall
# 
###
def compute_sides_to_draw(removed_tiles, moves):

    tiles_side_to_draw_first_pass = {} # TODO REWORK WITH dict {TILE : {Perspective, ...}, ...}
    tiles_side_to_draw_seconde_pass = {} # TODO REWORK WITH dict {TILE : {Perspective, ...}, ...}

    all_tiles = [m.tile for m in moves]
    all_tiles = all_tiles + list(removed_tiles)
    all_tiles = sort_tiles(all_tiles)

    tiles_to_draw_first_pass = []
    tiles_to_draw_second_pass = []
    tiles_to_draw_third_pass = []

    background_to_draw = []

    # LEFT EDGE
    curated_left_edge = compute_left_edge(all_tiles)
    for t in curated_left_edge:
        if t.i > 0:
            neighbor = board[t.i - 1][t.j]
            if neighbor is not None:
                tiles_to_draw_first_pass.append(([False,True,False, True],neighbor)) # Add Side and Corner to left egdge of all tiles

    corners = compute_corners_of_edge(curated_left_edge) # To fix the corner problem on the left side

    # To fix the corner problem
    for t in corners.values():
        print (t)
        if t.j + 1 < len(board[t.i]):
            neighbor = board[t.i][t.j + 1]
            if neighbor is not None: # useless ?
                print ("Should draw center of "+str(neighbor))
                tiles_to_draw_second_pass.append(([True,False,False,False], neighbor)) # Add center bottom left corner tile
            else:
                print("neighbor is none")
                print (neighbor)

    top_left_corner_tile = curated_left_edge[len(curated_left_edge) - 1] # to fix the other corner problem
    print ("Corner top left "+str(top_left_corner_tile))
    if top_left_corner_tile.i > 0 and top_left_corner_tile.j > 0:
        neighbor = board[top_left_corner_tile.i - 1][top_left_corner_tile.j - 1]
        if neighbor is not None:
            tiles_to_draw_first_pass.append(([False,False,False,True], neighbor)) # Add corner to top left neighbor

    # RIGHT EDGE
    curated_right_edge = compute_right_edge(all_tiles)
    corners = compute_corners_of_edge(curated_right_edge)
    for t in curated_right_edge:
        if t.i + 1 < len(board):
            neighbor = board[t.i + 1][t.j]
            if neighbor is not None:
                tiles_to_draw_third_pass.append(([True,False,False,False],neighbor)) # Add center to right egdge neighbors

    for t in corners.values():
        if t.i + 1 < len(board) and t.j + 1 < len(board[t.i]):
            neighbor = board[t.i + 1][t.j + 1]
            if neighbor is not None:
                tiles_to_draw_third_pass.append(([True,False,False,False], neighbor)) # Add center to bottom right neighbor
                if (neighbor.i == len(board) - 1) or (neighbor.i < len(board) and board[neighbor.i + 1][neighbor.j] is None):
                    tiles_to_draw_third_pass.append(([False,True,False,False], neighbor)) # Add side of corner's neighbor if it doesn't have anything to its right

    # background to draw when falling tiles
    top_right_corner_tile = curated_right_edge[len(curated_right_edge) - 1]
    right_edge_for_background = compute_edge_side_background(all_tiles) 
    background_to_draw = compute_side_background_to_draw(right_edge_for_background)

    # draw center of bottom edge neighbors (falling tiles)
    # draw bottom side of bottom edge (falling tiles) 
    # draw all sides for falling tiles
    bottom_edges = {} #dictionary : {COL_NUMBER : MOVE_WITH_TILE_OF_MAXIMUM_ROW_NUMBER}
    for m in moves:
        t = m.tile
        tiles_to_draw_second_pass.append(([False,True,False,True], t)) # Add Side and Corner of falling tiles
        if t.i not in bottom_edges:
            bottom_edges[t.i] = m
        else:
            curr_max_tile = bottom_edges[t.i].tile
            if t.j > curr_max_tile.j:
                bottom_edges[t.i] = m

    for move in bottom_edges.values():
        tile = move.tile
        tiles_to_draw_second_pass.append(([False, False, True, False], tile)) #draw bottom of falling tiles
        (dest_i,dest_j) = move.to_dest
        if dest_j + 1 < len(board[tile.i]):
            neighbor = board[tile.i][dest_j + 1]
            if neighbor is not None: # useless ?
                tiles_to_draw_third_pass.append(([True,False,False,False], neighbor)) # Add center to bottom edge neighbors
                if (neighbor.i == len(board) - 1) or (board[neighbor.i + 1][neighbor.j] is None):
                    tiles_to_draw_third_pass.append(([False,True,False,False], neighbor)) # Add side of bottom's neighbor if it doesn't have anything to its right


    # Sort drawing order
    tiles_to_draw_first_pass = sort_sides_to_draw(tiles_to_draw_first_pass)
    tiles_to_draw_second_pass = sort_sides_to_draw(tiles_to_draw_second_pass)
    tiles_to_draw_third_pass = sort_sides_to_draw(tiles_to_draw_third_pass)

    return (tiles_to_draw_first_pass + tiles_to_draw_second_pass + tiles_to_draw_third_pass, background_to_draw)

###
# Populates the board with random color tiles
###
def initialize_board():
    global board
    board = []
    for i in range(board_col_nb):
        board.append([])
        for j in range(board_row_nb):
            new_tile = Tile(i,j,get_random_color())
            board[i].append(new_tile)
    if check_game_over() == Game_Over.LOSE: # prevents generation with no clusters
        initialize_board()

###
# Draws the moving tiles
###
def draw_moving_tiles(moves):
    for m in moves:
        t = m.tile
        t.draw()

###
# Draws a tile with its perspective according to a list of sides to draw
# list_pers_tile_to_draw : Tuple of list of perspective sides to draw [([center, side, bottom, corner], tile), ...]
###
def draw_tile_with_perspective(list_pers_tile_to_draw):
    for (sides, tile) in list_pers_tile_to_draw:
        if sides[0]:
            tile.draw()
        if sides[1]:
            tile.tile_image.draw_side()
        if sides[2]:
            tile.tile_image.draw_bottom()
        if sides[3]:
            tile.tile_image.draw_corner()

def display_end_panel(msg, color, font):
    text = font.render(msg, True, color, Color.WHITE.value)

    x = display_width / 2 -  (text.get_rect().width / 2)
    y = display_height / 2 - (text.get_rect().height / 2) - (restart_button.rect.height) - 10
    gameDisplay.blit(text,(x,y))

    restart_button.draw()

def display_win_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    display_end_panel(text_map["you_won"], Color.RED.value, font)

def display_lose_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    display_end_panel(text_map["you_lost"], Color.BLACK.value, font)

def display_end_screen(game_over):
    if game_over == Game_Over.WIN:
        display_win_screen()
    if game_over == Game_Over.LOSE:
        display_lose_screen()

###
# Draws the board on the surface
###
def draw_board():
    gameDisplay.fill(background_color.value) #In lieu of picture
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                board[i][j].draw()

def game_loop():
    game_over = Game_Over.PLAYING 
    app_running = True
    tile_on_mouse_down = None
    button_on_mouse_down = None
    processing_falling_movements = False
    processing_sliding_movements = False
    bg_to_draw = []
    sides_to_draw = []
    downward_moves = {}
    sideway_moves = []
    history = History()
    draw_board()
    while app_running:
        undo_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

        if game_over == game_over.PLAYING:
            if not (processing_falling_movements or processing_sliding_movements) :
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
                        tile_on_mouse_down = None
                        connected_tiles = get_connected_tiles(clicked_tile)
                        if len(connected_tiles) > 1:
                            for c in connected_tiles:
                                bg_to_draw.append(board[c.i][c.j].rect)
                                board[c.i][c.j] = None
                            history.add_new_step(connected_tiles)
                            processing_falling_movements = True
                            # Compute first time falling tiles
                            downward_moves = compute_downward_movements(connected_tiles)
                            bg_to_draw = bg_to_draw + compute_background_to_draw(downward_moves)
                            (sides_to_draw, side_bg_to_draw) = compute_sides_to_draw(connected_tiles, downward_moves)
                            bg_to_draw += side_bg_to_draw

                    if undo_button.collides_with(pos) and button_on_mouse_down == undo_button:
                        button_on_mouse_down = None
                        undo_step(history)
            else:
                draw_background_tiles(bg_to_draw)
                if processing_falling_movements and not processing_sliding_movements:
                    # Falling tiles
                    processing_falling_movements = not move_tiles(downward_moves, Direction.DOWN)
                    draw_tile_with_perspective(sides_to_draw)
                    draw_moving_tiles(downward_moves)
                if not processing_falling_movements:
                    if not processing_sliding_movements:
                        sideway_moves = compute_side_movements()
                        if sideway_moves != []:
                            # Compute first time sliding tiles
                            bg_to_draw = compute_background_to_draw_for_sliding(sideway_moves)
                            processing_sliding_movements = True
                    else:
                        #Sliding tiles
                        processing_sliding_movements = not move_tiles(sideway_moves, Direction.LEFT)
                        draw_moving_tiles(sideway_moves)

                if not (processing_falling_movements or processing_sliding_movements):
                    # Finished moving tiles
                    bg_to_draw = []
                    sides_to_draw = []
                    game_over = check_game_over()
                    history.add_tile_movements_to_current_step(sideway_moves)
                    history.add_tile_movements_to_current_step(downward_moves)

        else:
            display_end_screen(game_over)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.collides_with(pos):
                    button_on_mouse_down = restart_button
                if undo_button.collides_with(pos):
                    button_on_mouse_down = undo_button

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if restart_button.collides_with(pos) and button_on_mouse_down == restart_button:
                    # Restarts the game
                    initialize_board()
                    draw_board()
                    history = History()
                    game_over = Game_Over.PLAYING
                if undo_button.collides_with(pos) and button_on_mouse_down == undo_button:
                    # Undo last step
                    undo_step(history)
                    game_over = Game_Over.PLAYING

                button_on_mouse_down = None

        pygame.display.update()
        clock.tick(fps)

    

    pygame.quit()
    quit()

initialize_board()
game_loop()