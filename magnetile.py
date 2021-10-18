import sys
import os
import getopt
import time
import enum
from random import seed
from random import randint
from random import random

try:
    import pygame
except ModuleNotFoundError:
    print("### Please install pygame : pip install pygame ###")
    raise

french_text_map = {
    "undo" : "Annuler",
    "restart" : "Rejouer",
    "you_won" : "Vous avez gagné !! :)",
    "you_lost" : "Vous avez perdu",
    "tile_count" : "Tuiles : "
}

english_text_map = {
    "undo" : "Undo",
    "restart" : "Play again",
    "you_won" : "You won !! :)",
    "you_lost" : "You lost",
    "tile_count" : "Tiles : "
}

text_map = english_text_map

number_of_color = 5
number_of_color_min = 3

def print_help():
    print ("usage : magnetile.py [-l language] [-c number_of_colors]")
    print ("        Languages are : french or english (default)")
    print ("        The number of colors can be between "+str(number_of_color_min)+" and "+str(number_of_color)+" included. Default is "+str(number_of_color))

try:
    options, remainder = getopt.getopt(sys.argv[1:],"hl:c:",["language=","--help","colors="])
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
    if opt in ("-c","--colors"):
        nb = 0
        try:
            nb = int(arg)
        except:
            print_help()
            sys.exit(2)
        if nb <= number_of_color and nb >=3:
            number_of_color = nb
        else:
            print ("Please choose a number of colors between "+str(number_of_color_min)+" and "+str(number_of_color))
            sys.exit(2)
    if opt in ("-h", "--help"):
        print_help()
        sys.exit(2)

# seed random number generator
seed(time.time())
fps = 60

root_dir = os.path.dirname(os.path.realpath(__file__))

display_width = 850
display_height = 720

tile_width = 45
tile_height = int(1.6*tile_width)
board_col_nb = 18
board_row_nb = 9

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
    ORANGE = (250, 183, 0)
    DARK_BLUE = (46, 50, 128)
    
side_width = 10
bottom_height = 10
tile_image_center_size = (tile_width, tile_height)
tile_image_side_size = (side_width, tile_height)
tile_image_side_bottom = (tile_width, bottom_height)
tile_image_side_corner = (side_width, bottom_height)
images_folder = "images"
tiles_images = {
    Color.RED : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "flower_tile.png")), tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_corner.png")),tile_image_side_corner),
        },
    Color.GREEN : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "bike_tile.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_corner.png")),tile_image_side_corner),
        },
    Color.BLUE : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "cat_tile.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_corner.png")),tile_image_side_corner),
        },
    Color.YELLOW : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "sun_tile.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_corner.png")),tile_image_side_corner),
        },
    Color.PURPLE : {
        "center" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "choco_tile.png")),tile_image_center_size),
        "side" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir,images_folder, "tile_side.png")), tile_image_side_size),
        "bottom" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_bottom.png")), tile_image_side_bottom),
        "corner" : pygame.transform.scale(pygame.image.load(os.path.join(root_dir, images_folder, "tile_corner.png")),tile_image_side_corner),
        }
}

background_color = Color.DARK_BLUE

###
# Picks a random color
###
colors_rand_arr = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.PURPLE]
def get_random_color():
    r = randint(0, number_of_color - 1)
    return colors_rand_arr[r]

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('MagneTile')
clock = pygame.time.Clock()

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

    def draw_all_sides(self):
        self.draw()
        self.tile_image.draw_side()
        self.tile_image.draw_bottom()
        self.tile_image.draw_corner()

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
        return "Movement from "+str(self.from_source)+" to "+str(self.to_dest)

class Text_Display:
    """ Represents a non clickable text without background """
    x = 0
    y = 0
    rect = pygame.Rect(0,0,0,0)
    text_render = None

    text_color = Color.BLACK.value
    font_name = 'Comic Sans MS'
    font_size = 30

    def __init__(self, x, y, text, text_color=Color.BLACK.value, font_name='Comic Sans MS', font_size=30):
        """ (x,y) are the coordinates of the text's center"""
        text_font = pygame.font.SysFont(font_name, font_size)
        self.text_render = text_font.render(text, True, text_color)
        width = self.text_render.get_rect().width
        height = self.text_render.get_rect().height
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size
        self.x = x - width / 2
        self.y = y - height / 2
        self.rect = pygame.Rect(self.x,self.y,width,height)

    def draw(self):
        gameDisplay.blit(self.text_render,(self.x,self.y))

    def update(self, text):
        text_font = pygame.font.SysFont(self.font_name, self.font_size)
        self.text_render = text_font.render(text, True, self.text_color)

    def update_and_draw(self, text, background_color=None):
        if (background_color):
            pygame.draw.rect(gameDisplay, background_color, self.rect)
        self.update(text)
        self.draw()

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
        border_width = self.rect.width + self.border_thickness * 8 + self.border_padding * 2
        border_height = self.rect.height +  self.border_thickness * 2

        border_rect = pygame.Rect((self.x - self.border_thickness *4 - self.border_padding, self.y - self.border_thickness),(border_width, border_height))
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
tile_count_text = Text_Display(60, 25, text_map["tile_count"], Color.WHITE.value)
tile_count_number = Text_Display(tile_count_text.rect.width + tile_count_text.x + 45, 25, text_map["tile_count"], Color.WHITE.value)

###
# TEMPORARY for testing
###
def initialize_custom_board():
    template = [
        [Color.BLUE,   Color.BLUE,   Color.BLUE,   Color.BLUE,   Color.BLUE,    Color.BLUE,   Color.GREEN],
        [None,         Color.GREEN,  Color.RED,    Color.RED,    Color.RED,     Color.RED,    Color.GREEN],
        [None,         Color.GREEN,  Color.GREEN,  Color.GREEN,  Color.RED,     Color.YELLOW, Color.GREEN],
        [Color.GREEN,  Color.RED,    Color.RED,    Color.RED,    Color.RED,     Color.RED,    Color.GREEN],
        [Color.GREEN,  Color.RED,    Color.RED,    Color.RED,    Color.RED,     Color.RED,    Color.GREEN],
        [None,         None,         Color.GREEN,  Color.RED,    Color.YELLOW,  Color.YELLOW, Color.GREEN],
        [None,         Color.GREEN,  Color.RED,    Color.RED,    Color.RED,     Color.RED,    Color.GREEN],
        [Color.BLUE,   Color.BLUE,   Color.BLUE,   Color.RED,    Color.BLUE,    Color.BLUE,   Color.GREEN],
        [None,         None,         None,         None,         None,          None,         Color.BLUE]
    ]
    for i in range(len(template)):
        board.append([])
        for j in range(len(template[i])):
            if template[i][j] is None:
                board[i].append(None) 
            else:
                board[i].append(Tile(i,j, template[i][j])) 

###
# Draws the whole board on the surface
###
def draw_board():
    tile_count = 0
    gameDisplay.fill(background_color.value) 
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                board[i][j].draw_all_sides()
                tile_count += 1
    tile_count_text.draw()
    undo_button.draw()
    tile_count_number.update_and_draw(str(tile_count),background_color.value)

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
# Depth first search algoritm to get the tiles of the same color
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
# Return a list of Tile_Movement representing the moves the tiles need to do
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
        return None
    last_step = history.undo_last_step()

    from_list = [] # the tiles we are moving from
    dest_list = [] # the destination of the tiles

    for m in last_step.neighbors_moves:
        t = m.tile
        (from_i, from_j) = m.from_source

        from_list.append(m.to_dest)
        dest_list.append(m.from_source)

        t.move(from_i, from_j)
        board[from_i][from_j] = t
    for t in last_step.cluster:
        board[t.i][t.j] = t
        dest_list.append((t.i, t.j))

    for coord in from_list:
        if coord not in dest_list:
            (i,j) = coord
            board[i][j] = None

    draw_board()
    return last_step

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
    min_x = display_width
    max_x = 0
    min_y = display_height
    max_y = 0

    for m in moves:
        t = m.tile
        if t.rect.x > max_x:
            max_x = t.rect.x
        (dest_x,dest_y) = get_xy_from_ij(m.to_dest)
        if dest_x < min_x:
            min_x = dest_x
        if t.rect.y < min_y:
            min_y = t.rect.y
        if t.rect.y > max_y:
            max_y = t.rect.y

    min_x = min_x + side_width
    max_x = max_x + tile_width 
    max_y = max_y + tile_height 
    width = (max_x - min_x) + side_width
    height = max_y - min_y + bottom_height
    r = pygame.Rect((min_x, min_y), (width, height))
    return r

def get_xy_from_ij(coord):
    (i,j) = coord
    t = Tile(i,j,Color.RED)
    return (t.rect.x, t.rect.y)

def compute_falling_tiles_data(tiles):
    bot_dict = {}
    falling_indexes = set()
    for t in tiles :
        if board[t.i][t.j] != None:
            falling_indexes.add(t.i)
        if t.i not in bot_dict.keys():
            bot_dict[t.i] = t.j
        else:
            if t.j > bot_dict[t.i]:
                bot_dict[t.i] = t.j

    return (bot_dict, list(falling_indexes))

def compute_sides_to_draw(removed_tiles, moves):
    all_tiles = [m.tile for m in moves]
    all_tiles = all_tiles + list(removed_tiles)
    all_tiles = sort_tiles(all_tiles)

    tiles_to_draw_first_pass = []
    tiles_to_draw_second_pass = []
    tiles_to_draw_third_pass = []

    background_to_draw = []

    (bot_edge, falling_indexes) = compute_falling_tiles_data(all_tiles)

    last_tile = None
    top_left_tile_found = False
    for t in all_tiles:

        check_left_List = []
        check_right_list = []

        # FIRST TILE
        if last_tile is None:
            check_left_List = [t]
        else:
            # NEW LINE
            if t.j != last_tile.j:
                check_right_list.append(last_tile)
                check_left_List.append(t)
            else:
                # GAP IN LINE
                if t.i != last_tile.i + 1:
                    check_right_list.append(last_tile)
                    check_left_List.append(t)

            # LAST TILE
            if t == all_tiles[-1]:
                check_right_list.append(t)

        if check_left_List != []:
            for check_left in check_left_List:
                if check_left.i > 0:
                    n = board[check_left.i - 1][check_left.j]
                    if n is not None:

                        if not top_left_tile_found:
                            top_left_tile_found = True
                            if check_left.i > 0 and check_left.j > 0:
                                tl = board[check_left.i - 1][check_left.j - 1]
                                if tl is not None:
                                    tiles_to_draw_first_pass.append(([False,False,False,True], tl)) # Add corner to top left neighbor

                        tiles_to_draw_first_pass.append(([False,True,False,True], n)) # Add side and corner to left neighbor

        if board[t.i][t.j] is not None:
            tiles_to_draw_first_pass.append(([False,True,False,True], t)) # Add all sides of falling tile
            tiles_to_draw_second_pass.append(([False,False,True,False], t)) # "
            tiles_to_draw_third_pass.append(([True,False,False,False], t)) # "

        if check_right_list != []:
            for check_right in check_right_list:
                if check_right.i + 1 < len(board):
                    n = board[check_right.i + 1][check_right.j]
                    if n is not None:
                        if n.j == len(board[n.i]) - 1:
                            tiles_to_draw_third_pass.append(([True,False,True,False], n)) # Add center and bottom of right neighbor
                            background_to_draw.append(pygame.Rect((n.rect.left,n.rect.bottom),tile_image_side_corner)) # Add background to remove corner of previous tile border
                        else:
                            tiles_to_draw_third_pass.append(([True,False,False,False], n)) # Add only center of right neighbor
                        background_to_draw.append(pygame.Rect((n.rect.left,n.rect.top),tile_image_side_corner)) # Add background to remove corner of previous tile on static right neighbor
                    else:
                        background_to_draw.append(pygame.Rect((check_right.rect.right, check_right.rect.top), tile_image_side_size)) # Add background of side of current tile
                else:
                    background_to_draw.append(pygame.Rect((check_right.rect.right, check_right.rect.top), tile_image_side_size)) # Add background of side of current tile when on edge
                    background_to_draw.append(pygame.Rect((check_right.rect.right, check_right.rect.bottom), tile_image_side_corner)) # Add background of corner of current tile when on edge

                if check_right.j == bot_edge[check_right.i]:# check corner
                    if check_right.i + 1 < len(board) and check_right.j + 1 < len(board[check_right.i]):
                        n_corner = board[check_right.i + 1][check_right.j + 1]
                        if n_corner is not None:
                            tiles_to_draw_third_pass.append(([True,False,False,False], n_corner)) # Add center of corner neighbor when tiles are falling
                        else:
                            tiles_to_draw_third_pass.append(([False,True,False,False], board[check_right.i][check_right.j + 1])) # Add center of corner neighbor when tiles are falling
                    if check_right.i < len(board) and check_right.j < len(board[check_right.i]):
                            background_to_draw.append(pygame.Rect((check_right.rect.right, check_right.rect.bottom), tile_image_side_corner)) # Add background of old corner of static tile
        # BOTTOM EDGE
        if t.j == bot_edge[t.i]:
            if t.j != len(board[t.i]) - 1: # not bottom edge of board
                n = board[t.i][t.j + 1]
                tiles_to_draw_third_pass.append(([True,False,False,False], n)) # Add center of bottom neighbor
                if n.i == len(board) - 1:
                    tiles_to_draw_third_pass.append(([False,True,False,False], n)) # Add side if tile is on edge of board
            else: # bottom edge of board
                background_to_draw.append(pygame.Rect((t.rect.left, t.rect.bottom), tile_image_side_bottom)) # Add background of bottom side of removed tiles when on edge

        last_tile = t

    tiles_to_draw_all_passes = tiles_to_draw_first_pass + tiles_to_draw_second_pass + tiles_to_draw_third_pass
    return (tiles_to_draw_all_passes,background_to_draw)

###
# Populates the board with a controlled randomized generation of tiles
###
def initialize_board():
    global board
    board = []

    color_count = {}
    for c in colors_rand_arr[:number_of_color]:
        color_count[c] = 0
    color_count_total = 0
    chance_cluster = 0.25 # chance of to be of the same color of either the left neighbor or the last tile

    last_color = get_random_color()

    for i in range(board_col_nb):
        board.append([])
        for j in range(board_row_nb):
            left_neighbor = None
            if i > 0:
                left_neighbor = board[i - 1][j]

            r = random()
            color = None
            if r < chance_cluster:

                if left_neighbor is not None:
                    r_cluster = random()
                    if r_cluster <= 0.5:
                        color = last_color
                    else:
                        color = left_neighbor.color
                else:
                    color = last_color
            else:
                enough_colors = True

                for k in color_count.keys():
                    if color_count[k] == 0:
                        enough_colors = False
                        break

                if enough_colors:
                    chance_color = {}
                    cumul = 0
                    count_last_color = color_count[last_color]

                    for k in color_count.keys():
                        if k != last_color:
                            total = (color_count_total - count_last_color)
                            ratio = color_count[k] / total
                            chance_color[k] = ((1 - ratio) / (number_of_color - 2)) + cumul # invert he ratio of tiles on the board to get corresponding chances
                            cumul = chance_color[k]

                    r2 = random()
                    last_threshold = 0
                    for k in chance_color.keys():
                        if r2 >= last_threshold and r2 < chance_color[k]:
                            color = k
                            break

                else:
                    color = get_random_color()
                
            color_count[color] += 1
            color_count_total += 1

            new_tile = Tile(i,j,color)
            last_color = color

            board[i].append(new_tile)

    if check_game_over() == Game_Over.LOSE: # prevents generation with no clusters
        initialize_board()

###
# Draws the moving tiles
###
def draw_sliding_tiles(moves):
    for m in moves:
        t = m.tile
        t.draw_all_sides()

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
    tile_count = board_col_nb * board_row_nb
    history = History()
    draw_board()
    while app_running:

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
                            tile_count -= len(connected_tiles)
                            processing_falling_movements = True
                            # Compute first time falling tiles
                            downward_moves = compute_downward_movements(connected_tiles)
                            bg_to_draw = bg_to_draw + compute_background_to_draw(downward_moves)
                            (sides_to_draw, side_bg_to_draw) = compute_sides_to_draw(connected_tiles, downward_moves)
                            bg_to_draw += side_bg_to_draw
                            # Update tile count
                            tile_count_number.update_and_draw(str(tile_count),background_color.value)

                    if undo_button.collides_with(pos) and button_on_mouse_down == undo_button:
                        button_on_mouse_down = None
                        last_hist_step = undo_step(history)
                        if (last_hist_step):
                            tile_count += len(last_hist_step.cluster)
            else:
                draw_background_tiles(bg_to_draw)
                if processing_falling_movements and not processing_sliding_movements:
                    # Falling tiles
                    processing_falling_movements = not move_tiles(downward_moves, Direction.DOWN)
                    draw_tile_with_perspective(sides_to_draw)   
                if not processing_falling_movements:

                    if not processing_sliding_movements:
                        sideway_moves = compute_side_movements()
                        if sideway_moves != []:
                            # Compute first time sliding tiles
                            bg_to_draw = [compute_background_to_draw_for_sliding(sideway_moves)]
                            processing_sliding_movements = True
                    else:
                        #Sliding tiles
                        processing_sliding_movements = not move_tiles(sideway_moves, Direction.LEFT)
                        draw_sliding_tiles(sideway_moves)

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
                    tile_count = board_col_nb * board_row_nb
                    history = History()
                    game_over = Game_Over.PLAYING
                if undo_button.collides_with(pos) and button_on_mouse_down == undo_button:
                    # Undo last step
                    last_hist_step = undo_step(history)
                    if (last_hist_step):
                        tile_count += len(last_hist_step.cluster)
                    game_over = Game_Over.PLAYING

                button_on_mouse_down = None

        pygame.display.update()
        clock.tick(fps)

    

    pygame.quit()
    quit()

initialize_board()
#initialize_custom_board()
game_loop()