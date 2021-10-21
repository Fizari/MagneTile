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

    """ Represents the board of the game (2D array of tiles) """
    def __init__(self, color_nb, col_nb, row_nb, tile_width, tile_height, offset_x, offset_y):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.color_nb = color_nb
        self.board = []
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

