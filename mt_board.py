from mt_enums import Color, Image_Section, Direction
from mt_tile import Tile, Tile_Movement, Tile_Image_Element
from mt_history import History
from random import seed
from random import randint
from random import random
import time

class Board:

    board = []

    colors_rand_arr = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.PURPLE]
    history = None

    col_nb = 0
    row_nb = 0
    tile_count = 0
    color_nb = 0

    board_coord = (0,0)
    board_width = 0 
    board_height = 0

    tile_on_mouse_down = None

    downward_moves = [] # used for the downward animation

    """ Represents the board of the game (2D array of tiles) """
    def __init__(self, color_nb, col_nb, row_nb):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.color_nb = color_nb
        self.board = []
        self.board_coord = (Tile.X_OFFSET, Tile.Y_OFFSET)
        self.board_width = col_nb * Tile.TILE_WIDTH
        self.board_height = row_nb * Tile.TILE_HEIGHT
        self.history = History()
        #self.initialize_custom()
        self.initialize_random(color_nb, col_nb, row_nb)
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
    def initialize_custom(self):
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
                    self.board[i].append(Tile(i,j, template[i][j]))
        self.row_nb = len(template[0])
        self.col_nb = len(template)

    def initialize_random(self, color_nb, col_nb, row_nb):
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

                new_tile = Tile(i,j,color)
                last_color = color

                self.board[i].append(new_tile)

    def get_all_tie(self):
        tie_list = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    tie_list += self.board[i][j].get_tie_all_sides()
        return tie_list

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
    def dfs(self, visited, tile):
        if tile not in visited:
            visited.add(tile)
            self.connected_neighbors.add(tile)
            for neighbour in self.get_tile_same_color_neighbors(tile):
                self.dfs(visited, neighbour)

    def get_connected_tiles(self, tile):
        self.connected_neighbors = set()
        self.dfs(set(),tile)
        return self.connected_neighbors

    ###
    # Get the tile that matches the coordinates, or None if no tiles are found 
    ###
    def get_tile_from_coord(self, coord):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] and self.board[i][j].is_clicked(coord):
                    return self.board[i][j]
        return None

    ###
    # Creates list of Tile_movement representing a move the tiles need to make
    ###

    def compute_downward_movements(self, connected_tiles):

        columns = {t.i for t in connected_tiles}
        moves = []
        for i in columns:
            dest_j = 0
            found_space = False
            empty_tiles = 0
            for j in range(len(self.board[i]) - 1, -1, -1): 
                if not self.board[i][j] and not found_space:
                    dest_j = j
                    found_space = True
                if self.board[i][j] and found_space:
                    empty_tiles = empty_tiles + (dest_j - j)
                if self.board[i][j] and empty_tiles != 0:
                    moves.append(Tile_Movement(self.board[i][j],(i,j+empty_tiles)))
                    found_space = False
        return moves

    ###
    # Get a list of background (Tile_Image_Element) to draw from a list of moves for the falling of the tiles
    ###
    def compute_background_to_draw(self, moves):
        res = []
        for m in moves:
            t = m.tile
            res.append(t.get_tie_center())
        return res

    def convert_tile_position_for_comparison(self, tile):
        return tile.i + len(self.board) * tile.j
    ###
    # Sorts a list of tiles regarding their position in the grid : left to right first, then top to bottom
    ###
    def sort_tiles(self, list_tiles, rev=False):
        return sorted(list_tiles,key=(self.convert_tile_position_for_comparison), reverse=rev)

    ###
    # Prepare data for the falling of the tiles 
    ###
    def compute_falling_tiles_data(self, tiles):
        bot_dict = {}
        falling_indexes = set()
        for t in tiles :
            if self.board[t.i][t.j]:
                falling_indexes.add(t.i)
            if t.i not in bot_dict.keys():
                bot_dict[t.i] = t.j
            else:
                if t.j > bot_dict[t.i]:
                    bot_dict[t.i] = t.j

        return (bot_dict, list(falling_indexes))

    ###
    # Get the background of all the 'reacting' tiles around the disapearing tiles to draw
    ###
    def compute_sides_to_draw(self, removed_tiles, moves):
        all_tiles = [m.tile for m in moves]
        all_tiles = all_tiles + list(removed_tiles)
        all_tiles = self.sort_tiles(all_tiles)

        tiles_to_draw_first_pass = []
        tiles_to_draw_second_pass = []
        tiles_to_draw_third_pass = []

        background_to_draw = []

        (bot_edge, falling_indexes) = self.compute_falling_tiles_data(all_tiles)

        last_tile = None
        top_left_tile_found = False
        for t in all_tiles:

            check_left_List = []
            check_right_list = []

            # FIRST TILE
            if not last_tile:
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
                        n = self.board[check_left.i - 1][check_left.j]
                        if n:

                            if not top_left_tile_found:
                                top_left_tile_found = True
                                if check_left.i > 0 and check_left.j > 0:
                                    tl = self.board[check_left.i - 1][check_left.j - 1]
                                    if tl:
                                        tiles_to_draw_first_pass.append(tl.get_tie_corner()) # Add corner to top left neighbor

                            # Add side and corner to left neighbor
                            tiles_to_draw_first_pass.append(n.get_tie_side())
                            tiles_to_draw_first_pass.append(n.get_tie_corner())

            if self.board[t.i][t.j]:
                # Add all sides of falling tile
                tiles_to_draw_first_pass.append(t.get_tie_side())
                tiles_to_draw_first_pass.append(t.get_tie_corner())
                tiles_to_draw_second_pass.append(t.get_tie_bottom())
                tiles_to_draw_third_pass.append(t.get_tie_center())

            if check_right_list != []:
                for check_right in check_right_list:
                    if check_right.i + 1 < len(self.board):
                        n = self.board[check_right.i + 1][check_right.j]
                        if n:
                            if n.j == len(self.board[n.i]) - 1:
                                # Add center and bottom of right neighbor
                                tiles_to_draw_third_pass.append(n.get_tie_center())
                                tiles_to_draw_third_pass.append(n.get_tie_bottom())

                                background_to_draw.append(Tile_Image_Element(n.color, Image_Section.CORNER, n.get_pos_left(), n.get_pos_bottom())) # Add background to remove corner of previous tile border
                            else:
                                tiles_to_draw_third_pass.append(n.get_tie_center()) # Add only center of right neighbor
                            background_to_draw.append(Tile_Image_Element(n.color, Image_Section.CORNER, n.get_pos_left(), n.get_pos_top())) # Add background to remove corner of previous tile on static right neighbor
                        else:
                            background_to_draw.append(Tile_Image_Element(check_right.color, Image_Section.SIDE, check_right.get_pos_right(), check_right.get_pos_top())) # Add background of side of current tile
                    else:
                        background_to_draw.append(Tile_Image_Element(check_right.color, Image_Section.SIDE, check_right.get_pos_right(), check_right.get_pos_top())) # Add background of side of current tile when on edge
                        background_to_draw.append(Tile_Image_Element(check_right.color, Image_Section.CORNER, check_right.get_pos_right(), check_right.get_pos_bottom())) # Add background of corner of current tile when on edge

                    if check_right.j == bot_edge[check_right.i]:# check corner
                        if check_right.i + 1 < len(self.board) and check_right.j + 1 < len(self.board[check_right.i]):
                            n_corner = self.board[check_right.i + 1][check_right.j + 1]
                            if n_corner:
                                tiles_to_draw_third_pass.append(n_corner.get_tie_center()) # Add center of corner neighbor when tiles are falling
                            else:
                                tiles_to_draw_third_pass.append(self.board[check_right.i][check_right.j + 1].get_tie_side()) # ??? (lost in translation)
                        if check_right.i < len(self.board) and check_right.j < len(self.board[check_right.i]):
                                background_to_draw.append(Tile_Image_Element(check_right.color, Image_Section.CORNER, check_right.get_pos_right(), check_right.get_pos_bottom())) # Add background of old corner of static tile
            # BOTTOM EDGE
            if t.j == bot_edge[t.i]:
                if t.j != len(self.board[t.i]) - 1: # not bottom edge of board
                    n = self.board[t.i][t.j + 1]
                    tiles_to_draw_third_pass.append(n.get_tie_center()) # Add center of bottom neighbor
                    if n.i == len(self.board) - 1:
                        tiles_to_draw_third_pass.append(n.get_tie_side()) # Add side if tile is on edge of board
                else: # bottom edge of board
                    background_to_draw.append(Tile_Image_Element(t.color, Image_Section.BOTTOM, t.get_pos_left(), t.get_pos_bottom())) # Add background of bottom side of removed tiles when on edge

            last_tile = t

        tiles_to_draw_all_passes = tiles_to_draw_first_pass + tiles_to_draw_second_pass + tiles_to_draw_third_pass
        return (tiles_to_draw_all_passes,background_to_draw)

    ###
    # Applies the moves from the list of Tile_Movement(see compute_downward_movements)
    # return a bool indicating if the tiles are in their respective place
    ###
    def move_tiles(self, moves, direction):
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
                self.board[t.i][t.j] = None
                self.board[dest_i][dest_j] = t
                t.move(dest_i, dest_j)
            else:
                tiles_in_place = False
                    
        return tiles_in_place

    ###
    # Return a list of Tile_Movement representing the moves the tiles need to do
    ###
    def compute_side_movements(self):
        moves = []
        found_space = False
        dest_i = 0
        nb_empty_col = 0
        for i in range(len(self.board)):
            max_j = len(self.board[i]) - 1
            if not self.board[i][max_j] and not found_space:
                dest_i = i
                found_space = True
            if self.board[i][max_j] and found_space:
                nb_empty_col = nb_empty_col + (i - dest_i)
            if self.board[i][max_j] and nb_empty_col != 0:
                for j in range(len(self.board[i])):
                    if self.board[i][j]:
                        moves.append(Tile_Movement(self.board[i][j], (i - nb_empty_col ,j)))
                found_space = False
        return moves

    def get_xy_from_ij(self, coord):
        (i,j) = coord
        t = Tile(i,j,Color.RED)
        return (t.rect.x, t.rect.y)

    ###
    # Get a list of background rectangles to draw from a list of moves for the sliding of the tiles
    ###
    def compute_background_to_draw_for_sliding(self, moves):
        min_x = display_width
        max_x = 0
        min_y = display_height
        max_y = 0

        for m in moves:
            t = m.tile
            if t.get_x() > max_x:
                max_x = t.get_x()
            (dest_x,dest_y) = self.get_xy_from_ij(m.to_dest)
            if dest_x < min_x:
                min_x = dest_x
            if t.get_y() < min_y:
                min_y = t.get_y()
            if t.get_y() > max_y:
                max_y = t.get_y()

        min_x = min_x + side_width
        max_x = max_x + Tile.TILE_WIDTH 
        max_y = max_y + Tile.TILE_HEIGHT 
        width = (max_x - min_x) + side_width
        height = max_y - min_y + bottom_height
        r = pygame.Rect((min_x, min_y), (width, height))
        return r

    def process_click_mouse_down(self, mouse_coord):
        clicked_tile = self.get_tile_from_coord(mouse_coord)
        if clicked_tile is not None:
            self.tile_on_mouse_down = clicked_tile
            #print(str(self.tile_on_mouse_down))

    def process_click_mouse_up(self, mouse_coord):
        clicked_tile = self.get_tile_from_coord(mouse_coord)
        #print("DEBUG tile_mouse_down : " + str(tile_on_mouse_down.i) + "," + str(tile_on_mouse_down.j) ) if tile_on_mouse_down else print("DEBUG tile_on_mouse_down is None")
        #print("DEBUG clicked tile : " + str(clicked_tile.i) + "," + str(clicked_tile.j) ) if clicked_tile else print("DEBUG clicked_tile is None")
        connected_tiles_mouse_down = self.get_connected_tiles(self.tile_on_mouse_down) if self.tile_on_mouse_down and clicked_tile else []
        same_cluster = next((t for t in connected_tiles_mouse_down if t.i == clicked_tile.i and t.j == clicked_tile.j), None)
        if clicked_tile and same_cluster:
            self.tile_on_mouse_down = None
            print("clicked : " + str(clicked_tile))

            bg_to_draw = [] # list of Tile_Image_Element that represents the background to draw
            sides_to_draw = [] # list of Tile_Image_Element

            connected_tiles = connected_tiles_mouse_down
            if len(connected_tiles) > 1:
                for c in connected_tiles:
                    bg_to_draw.append(self.board[c.i][c.j].get_tie_center())
                    self.board[c.i][c.j] = None
                self.history.add_new_step(connected_tiles)
                self.tile_count -= len(connected_tiles)
                # Compute first time falling tiles
                self.downward_moves = self.compute_downward_movements(connected_tiles)
                bg_to_draw = bg_to_draw + self.compute_background_to_draw(self.downward_moves)
                (sides_to_draw, side_bg_to_draw) = self.compute_sides_to_draw(connected_tiles, self.downward_moves)
                bg_to_draw += side_bg_to_draw
                return (sides_to_draw, bg_to_draw)
        return None
