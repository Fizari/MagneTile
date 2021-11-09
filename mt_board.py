from mt_enums import Color, Image_Section, Direction, Game_State
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
    board_save = []

    col_nb = 0
    row_nb = 0
    color_nb = 0

    board_coord = (0, 0)
    board_width = 0
    board_height = 0

    tile_on_mouse_down = None

    downward_moves = []  # used for the downward animation
    sideway_moves = []  # used for the sliding left animation

    score_count = 0

    # State of the game
    tile_count = 0
    clusters = []

    # Represents the board of the game (2D array of tiles) #
    def __init__(self, color_nb, col_nb, row_nb):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.color_nb = color_nb
        self.board = []
        self.board_coord = (Tile.X_OFFSET, Tile.Y_OFFSET)
        self.board_width = col_nb * Tile.TILE_WIDTH
        self.board_height = row_nb * Tile.TILE_HEIGHT
        self.score_count = 0
        self.history = History()
        # self.initialize_custom(4, 9, 7)
        self.initialize_random(color_nb, col_nb, row_nb)
        # seed random number generator
        seed(time.time())

    def get_random_color(self):
        r = randint(0, self.color_nb - 1)
        return self.colors_rand_arr[r]

    ###
    # TEMPORARY for testing
    ###
    def initialize_custom(self, color_nb, col_nb, row_nb):
        self.row_nb = row_nb
        self.col_nb = col_nb
        self.color_nb = color_nb
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
                    self.board[i].append(Tile(i, j, template[i][j]))
        self.row_nb = len(template[0])
        self.col_nb = len(template)

    def initialize_random(self, color_nb, col_nb, row_nb):
        # Populates the board with a controlled randomized generation of tiles #
        self.board = []
        self.board_save = []
        self.row_nb = row_nb
        self.col_nb = col_nb

        color_count = {}
        for c in self.colors_rand_arr[:color_nb]:
            color_count[c] = 0
        color_count_total = 0
        chance_cluster = 0.25  # chance of to be of the same color of either the left neighbor or the last tile

        last_color = self.get_random_color()

        for i in range(col_nb):
            self.board.append([])
            self.board_save.append([])
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
                                chance_color[k] = ((1 - ratio) / (color_nb - 2)) + cumul  # invert he ratio of tiles on the board to get corresponding chances
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

                new_tile = Tile(i, j, color)
                last_color = color

                self.board[i].append(new_tile)
                self.board_save[i].append(Tile(i, j, color))

        self.update_game_state()

    def reset(self):
        self.initialize_random(self.color_nb, self.col_nb, self.row_nb)
        self.history = History()
        self.score_count = 0
        self.update_game_state()

    def revert_to_start(self):
        self.board = self.copy_board_saved()
        self.history = History()
        self.score_count = 0
        self.update_game_state()

    def copy_board_saved(self):
        new_board = []
        for i in range(len(self.board)):
            new_board.append([])
            for j in range(len(self.board[i])):
                new_board[i].append(Tile(i, j, self.board_save[i][j].color))
        return new_board

    ###
    # Checks the whole board is the game is over (won or lost)
    ###
    def check_game_over(self):
        if len(self.clusters) == 0:
            if self.tile_count == 0:
                return Game_State.WIN
            else:
                return Game_State.LOSE
        else:
            return Game_State.PLAYING

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
                        coord_to_check.append((i, j - 1))
                        coord_to_check.append((i, j + 1))
                        coord_to_check.append((i - 1, j))
                        coord_to_check.append((i + 1, j))
                    else:
                        coord_to_check.append((i, j - 1))
                        coord_to_check.append((i - 1, j))
                        coord_to_check.append((i + 1, j))
                else:
                    coord_to_check.append((i, j + 1))
                    coord_to_check.append((i - 1, j))
                    coord_to_check.append((i + 1, j))
            else:
                if j > 0:
                    if j < len(self.board[0]) - 1:
                        coord_to_check.append((i, j - 1))
                        coord_to_check.append((i, j + 1))
                        coord_to_check.append((i - 1, j))
                    else:
                        coord_to_check.append((i, j - 1))
                        coord_to_check.append((i - 1, j))
                else:
                    coord_to_check.append((i, j + 1))
                    coord_to_check.append((i - 1, j))
        else:
            if j > 0:
                if j < len(self.board[0]) - 1:
                    coord_to_check.append((i, j - 1))
                    coord_to_check.append((i, j + 1))
                    coord_to_check.append((i + 1, j))
                else:
                    coord_to_check.append((i, j - 1))
                    coord_to_check.append((i + 1, j))
            else:
                coord_to_check.append((i, j + 1))
                coord_to_check.append((i + 1, j))

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
        self.dfs(set(), tile)
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
                    moves.append(Tile_Movement(self.board[i][j], (i, j + empty_tiles)))
                    found_space = False
        return moves

    ###
    # instantly resolves the next state of the board after a cluster has been removed
    # cluster is a list of tiles
    ###
    def resolve_new_state(self, cluster):

        for tile in cluster:
            self.board[tile.i][tile.j] = None

        downward_moves = self.compute_downward_movements(cluster)
        for m in downward_moves:
            t = m.tile
            (dest_i, dest_j) = m.to_dest
            self.board[t.i][t.j] = None
            self.board[dest_i][dest_j] = t
            t.move(dest_i, dest_j)

        sideway_moves = self.compute_side_movements()
        for m in sideway_moves:
            t = m.tile
            (dest_i, dest_j) = m.to_dest
            self.board[t.i][t.j] = None
            self.board[dest_i][dest_j] = t
            t.move(dest_i, dest_j)

    def pick_random_cluster(self):
        r = randint(0, len(self.clusters) - 1)
        return self.clusters[r]

    def update_game_state(self):
        tiles_checked = []
        clusters = []  # List of clusters
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                curr_tile = self.board[i][j]
                if curr_tile and curr_tile not in tiles_checked:
                    cluster = self.get_connected_tiles(curr_tile)
                    if len(cluster) > 1:
                        clusters += [cluster]
                    for t in cluster:
                        tiles_checked.append(t)

        self.clusters = clusters
        self.tile_count = len(tiles_checked)
        # print("nb of clusters : " + str(len(self.clusters)))

    def post_processing_movement(self):
        self.history.add_tile_movements_to_current_step(self.sideway_moves)
        self.history.add_tile_movements_to_current_step(self.downward_moves)

    ###
    # Get a list of background (Tile_Image_Element) to draw from a list of moves for the falling of the tiles
    ###
    def compute_background_to_draw(self, moves):
        res = []
        for m in moves:
            t = m.tile
            res.append(self.create_background_tie(Image_Section.CENTER, t.coord))
        return res

    def convert_tile_position_for_comparison(self, tile):
        return tile.i + len(self.board) * tile.j

    ###
    # Sorts a list of tiles regarding their position in the grid : left to right first, then top to bottom
    ###
    def sort_tiles(self, list_tiles, rev=False):
        return sorted(list_tiles, key=(self.convert_tile_position_for_comparison), reverse=rev)

    ###
    # Prepare data for the falling of the tiles
    ###
    def compute_falling_tiles_data(self, tiles):
        bot_dict = {}
        falling_indexes = set()
        for t in tiles:
            if self.board[t.i][t.j]:
                falling_indexes.add(t.i)
            if t.i not in bot_dict.keys():
                bot_dict[t.i] = t.j
            else:
                if t.j > bot_dict[t.i]:
                    bot_dict[t.i] = t.j

        return (bot_dict, list(falling_indexes))

    def create_background_tie(self, section, coord):
        tmpTile = Tile(0, 0, None)
        tmpTile.coord = coord
        return Tile_Image_Element(tmpTile, section)

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
                                        tiles_to_draw_first_pass.append(tl.get_tie_corner())  # Add corner to top left neighbor

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

                                # Add background to remove corner of previous tile border
                                background_to_draw.append(self.create_background_tie(Image_Section.CORNER, (n.get_pos_left(), n.get_pos_bottom())))
                            else:
                                tiles_to_draw_third_pass.append(n.get_tie_center())  # Add only center of right neighbor
                            background_to_draw.append(self.create_background_tie(Image_Section.CORNER, (n.get_pos_left(), n.get_pos_top())))  # Add background to remove corner of previous tile on static right neighbor
                        else:
                            background_to_draw.append(self.create_background_tie(Image_Section.SIDE, (check_right.get_pos_right(), check_right.get_pos_top())))  # Add background of side of current tile
                    else:
                        background_to_draw.append(self.create_background_tie(Image_Section.SIDE, (check_right.get_pos_right(), check_right.get_pos_top())))  # Add background of side of current tile when on edge
                        background_to_draw.append(self.create_background_tie(Image_Section.CORNER, (check_right.get_pos_right(), check_right.get_pos_bottom())))  # Add background of corner of current tile when on edge

                    if check_right.j == bot_edge[check_right.i]:  # check corner
                        if check_right.i + 1 < len(self.board) and check_right.j + 1 < len(self.board[check_right.i]):
                            n_corner = self.board[check_right.i + 1][check_right.j + 1]
                            if n_corner:
                                tiles_to_draw_third_pass.append(n_corner.get_tie_center())  # Add center of corner neighbor when tiles are falling
                            else:
                                tiles_to_draw_third_pass.append(self.board[check_right.i][check_right.j + 1].get_tie_side())  # ??? (lost in translation)
                        if check_right.i < len(self.board) and check_right.j < len(self.board[check_right.i]):
                                background_to_draw.append(self.create_background_tie(Image_Section.CORNER, (check_right.get_pos_right(), check_right.get_pos_bottom())))  # Add background of old corner of static tile
            # BOTTOM EDGE
            if t.j == bot_edge[t.i]:
                if t.j != len(self.board[t.i]) - 1:  # not bottom edge of board
                    n = self.board[t.i][t.j + 1]
                    tiles_to_draw_third_pass.append(n.get_tie_center())  # Add center of bottom neighbor
                    if n.i == len(self.board) - 1:
                        tiles_to_draw_third_pass.append(n.get_tie_side())  # Add side if tile is on edge of board
                else:  # bottom edge of board
                    background_to_draw.append(self.create_background_tie(Image_Section.BOTTOM, (t.get_pos_left(), t.get_pos_bottom())))  # Add background of bottom side of removed tiles when on edge

            last_tile = t

        tiles_to_draw_all_passes = tiles_to_draw_first_pass + tiles_to_draw_second_pass + tiles_to_draw_third_pass
        return (tiles_to_draw_all_passes, background_to_draw)

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
                finished = t.fall_to(dest_i, dest_j)
            if direction == Direction.LEFT:
                finished = t.slide_left_to(dest_i, dest_j)

            if finished:
                self.board[t.i][t.j] = None
                self.board[dest_i][dest_j] = t
                t.move(dest_i, dest_j)
            else:
                tiles_in_place = False

        return tiles_in_place

    def moves_tiles_downward(self):
        return self.move_tiles(self.downward_moves, Direction.DOWN)

    def moves_tiles_left(self):
        return self.move_tiles(self.sideway_moves, Direction.LEFT)

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
                        moves.append(Tile_Movement(self.board[i][j], (i - nb_empty_col, j)))
                found_space = False
        self.sideway_moves = moves
        return moves

    def get_xy_from_ij(self, coord):
        (i, j) = coord
        t = Tile(i, j, Color.RED)
        return t.coord

    ###
    # Get a list of background rectangles to draw from a list of moves for the sliding of the tiles
    ###
    def compute_background_to_draw_for_sliding(self, moves, side_width, bottom_height):
        min_x = 999999999999999999  # AKA infinity
        max_x = 0
        min_y = 999999999999999999
        max_y = 0

        for m in moves:
            t = m.tile
            if t.get_x() > max_x:
                max_x = t.get_x()
            (dest_x, dest_y) = self.get_xy_from_ij(m.to_dest)
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
        tmpTile = Tile(0, 0, None)
        tmpTile.coord = (min_x, min_y)
        tmpTile.TILE_WIDTH = width
        tmpTile.TILE_HEIGHT = height
        return Tile_Image_Element(tmpTile, None)

    ###
    # Undo the last step of the history
    ###
    def undo_step(self):
        if self.history == [] or self.history.steps == []:
            return None
        last_step = self.history.undo_last_step()

        from_list = []  # the tiles we are moving from
        dest_list = []  # the destination of the tiles

        for m in last_step.neighbors_moves:
            t = m.tile
            (from_i, from_j) = m.from_source

            from_list.append(m.to_dest)
            dest_list.append(m.from_source)

            t.move(from_i, from_j)
            self.board[from_i][from_j] = t
        for t in last_step.cluster:
            self.board[t.i][t.j] = t
            dest_list.append((t.i, t.j))

        for coord in from_list:
            if coord not in dest_list:
                (i, j) = coord
                self.board[i][j] = None

        self.update_game_state()
        self.score_count -= self.calculate_score(len(last_step.cluster))
        return last_step

    def calculate_score(self, nb_of_tiles):
        return nb_of_tiles * 100 + (nb_of_tiles - 2) * 50

    def calculate_end_score(self, game_won):
        score = self.score_count
        if game_won:
            score += self.col_nb * 50 * ((self.col_nb * self.row_nb) % 10)
        return score

    def process_click(self, mouse_coord_down, mouse_coord_up):
        clicked_tile_down = self.get_tile_from_coord(mouse_coord_down)
        clicked_tile_up = self.get_tile_from_coord(mouse_coord_up)

        if not clicked_tile_down or not clicked_tile_up:
            return None

        connected_tiles_mouse_down = self.get_connected_tiles(clicked_tile_down)
        same_cluster = next((t for t in connected_tiles_mouse_down if t.i == clicked_tile_up.i and t.j == clicked_tile_up.j), None)
        if same_cluster:

            bg_to_draw = []  # list of Tile_Image_Element that represents the background to draw
            sides_to_draw = []  # list of Tile_Image_Element

            connected_tiles = connected_tiles_mouse_down
            if len(connected_tiles) > 1:
                for c in connected_tiles:
                    bg_to_draw.append(self.board[c.i][c.j].get_tie_center())
                    self.board[c.i][c.j] = None
                self.history.add_new_step(connected_tiles)
                self.tile_count -= len(connected_tiles)
                self.score_count += self.calculate_score(len(connected_tiles))
                # Compute first time falling tiles
                self.downward_moves = self.compute_downward_movements(connected_tiles)
                bg_to_draw = bg_to_draw + self.compute_background_to_draw(self.downward_moves)
                (sides_to_draw, side_bg_to_draw) = self.compute_sides_to_draw(connected_tiles, self.downward_moves)
                bg_to_draw += side_bg_to_draw

                return (sides_to_draw, bg_to_draw)
        return None

