from mt_enums import Color
from mt_tile import Tile
from random import seed
from random import randint
from random import random
import time

class Board:

    board = []

    colors_rand_arr = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.PURPLE]

    col_nb = 0
    row_nb = 0
    tile_count = 0
    color_nb = 0

    processing_falling_movements = False
    processing_sliding_movements = False

    board_coord = (0,0)
    board_width = 0 
    board_height = 0

    tile_on_mouse_down = None

    """ Represents the board of the game (2D array of tiles) """
    def __init__(self, color_nb, col_nb, row_nb, tile_width, tile_height, offset_x, offset_y):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.color_nb = color_nb
        self.board = []
        self.board_coord = (offset_x, offset_y)
        self.board_width = col_nb * tile_width
        self.board_height = row_nb * tile_height
        #self.initialize_custom(tile_width, tile_height, offset_x, offset_y)
        self.initialize_random(color_nb, col_nb, row_nb, tile_width, tile_height, offset_x, offset_y)
        # seed random number generator
        seed(time.time())

    def set_tile_count(self, tile_count):
        self.tile_count = tile_count

    def get_tile_count(self):
        return self.tile_count

    def reset_tile_count(self):
        self.tile_count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    self.tile_count += 1

    def get_random_color(self):
        r = randint(0, self.color_nb - 1)
        return self.colors_rand_arr[r]

    ###
    # TEMPORARY for testing
    ###
    def initialize_custom(self, tile_width, tile_height, offset_x, offset_y):
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
            self.board.append([])
            for j in range(len(template[i])):
                if template[i][j] is None:
                    self.board[i].append(None) 
                else:
                    self.board[i].append(Tile(i,j, template[i][j], tile_width, tile_height, offset_x, offset_y))
        self.row_nb = len(template[0])
        self.col_nb = len(template)

    def initialize_random(self, color_nb, col_nb, row_nb, tile_width, tile_height, offset_x, offset_y):
        ### Populates the board with a controlled randomized generation of tiles ###
        self.board = []
        self.row_nb = row_nb
        self.col_nb = col_nb

        color_count = {}
        for c in self.colors_rand_arr[:color_nb]:
            color_count[c] = 0
        color_count_total = 0
        chance_cluster = 0.25 # chance of to be of the same color of either the left neighbor or the last tile

        last_color = self.get_random_color()

        for i in range(col_nb):
            self.board.append([])
            for j in range(row_nb):
                left_neighbor = None
                if i > 0:
                    left_neighbor = self.board[i - 1][j]

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
                                chance_color[k] = ((1 - ratio) / (color_nb - 2)) + cumul # invert he ratio of tiles on the board to get corresponding chances
                                cumul = chance_color[k]

                        r2 = random()
                        last_threshold = 0
                        for k in chance_color.keys():
                            if r2 >= last_threshold and r2 < chance_color[k]:
                                color = k
                                break

                    else:
                        color = self.get_random_color()
                    
                color_count[color] += 1
                color_count_total += 1

                new_tile = Tile(i,j,color, tile_width, tile_height, offset_x, offset_y)
                last_color = color

                self.board[i].append(new_tile)

    def get_all_tie(self):
        tie_list = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    tie_list += self.board[i][j].get_tie_all_sides()
        return tie_list

    def is_processing_movements(self):
        return self.processing_falling_movements or self.processing_sliding_movements

    def is_clicked(self, mouse_coord):
        (mouse_x, mouse_y) = mouse_coord
        (board_x, board_y) = self.board_coord
        return mouse_x >= board_x and mouse_y >= board_y and mouse_x <= (board_x + self.board_width) and mouse_y <= (board_y + self.board_height)
    
    ###
    # Get the neighbors of a tile that are of the same color
    ###
    def get_tile_same_color_neighbors(self, tile):
        i = tile.i
        j = tile.j

        n = []
        coord_to_check = []

        if i > 0:
            if i < len(self.board) - 1:
                if j > 0:
                    if j < len(self.board[0]) - 1:
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
                    if j < len(self.board[0]) - 1:
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
                    if j < len(self.board[0]) - 1:
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
            tile_to_check = self.board[c[0]][c[1]]
            if tile_to_check and tile_to_check.color == tile.color:
                n.append(tile_to_check)

        return n

    ###
    # Depth first search algoritm to get the tiles of the same color
    ###
    connected_neighbors = set()
    def dfs(visited, tile):
        if tile not in visited:
            visited.add(tile)
            self.connected_neighbors.add(tile)
            for neighbour in self.get_tile_same_color_neighbors(tile):
                dfs(visited, neighbour)

    def get_connected_tiles(self, tile):
        self.connected_neighbors = set()
        dfs(set(),tile)
        return self.connected_neighbors

    def process_click_mouse_down(self, mouse_coord):
        clicked_tile = get_tile_from_coord(mouse_coord)
        if clicked_tile is not None:
            self.tile_on_mouse_down = clicked_tile

    def process_click_mouse_up(self, mouse_coord):
        clicked_tile = get_tile_from_coord(mouse_coord)
        #print("DEBUG tile_mouse_down : " + str(tile_on_mouse_down.i) + "," + str(tile_on_mouse_down.j) ) if tile_on_mouse_down else print("DEBUG tile_on_mouse_down is None")
        #print("DEBUG clicked tile : " + str(clicked_tile.i) + "," + str(clicked_tile.j) ) if clicked_tile else print("DEBUG clicked_tile is None")
        connected_tiles_mouse_down = self.get_connected_tiles(self.tile_on_mouse_down) if self.tile_on_mouse_down and clicked_tile else []
        same_cluster = next((t for t in connected_tiles_mouse_down if t.i == clicked_tile.i and t.j == clicked_tile.j), None)
        if clicked_tile and same_cluster:
            self.tile_on_mouse_down = None
            connected_tiles = connected_tiles_mouse_down
            if len(connected_tiles) > 1:
                for c in connected_tiles:
                    bg_to_draw.append(self.board[c.i][c.j].rect)
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
