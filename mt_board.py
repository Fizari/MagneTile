from mt_enums import Color
from mt_tile import Tile

class Board:

    board = []

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
        self.initialize_custom(tile_width, tile_height, offset_x, offset_y)

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
        

    def get_all_tie(self):
        tie_list = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    tie_list += self.board[i][j].get_tie_all_sides()
        return tie_list

