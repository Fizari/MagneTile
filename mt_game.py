from mt_board import Board
from mt_enums import Color, Game_State, Image_Section
from mt_tile import Tile
from mt_text import Label, Panel
from mt_save import Save
import os
try:
    import pygame
except ModuleNotFoundError:
    print("### Please install pygame : pip install pygame ###")
    raise


class Game_Language:
    french_text_map = None
    english_text_map = None

    text_map = None

    def __init__(self):
        self.french_text_map = {
            "undo": "Annuler",
            "restart": "Rejouer",
            "you_won": "Vous avez gagné !! :)",
            "you_lost": "Vous avez perdu",
            "tile_count": "Tuiles : ",
            "score": "Score : ",
            "highscore": "Meilleur score : ",
            "new_highscore": "Meilleur score !"
        }
        self.english_text_map = {
            "undo": "Undo",
            "restart": "Play again",
            "you_won": "You won !! :)",
            "you_lost": "You lost",
            "tile_count": "Tiles : ",
            "score": "Score : ",
            "highscore": "Highscore: ",
            "new_highscore": "New highscore !"
        }
        self.set_to_english()  # default value

    def set_to_french(self):
        self.text_map = self.french_text_map

    def set_to_english(self):
        self.text_map = self.english_text_map

    def get_text(self, key):
        return self.text_map[key]


class Game_Images:
    # Images that are gonna be drawn on the screen #
    tiles_images = None
    side_width = 10
    bottom_height = 10
    images_folder = "images"
    root_dir = os.path.dirname(os.path.realpath(__file__))

    # map to get the correct size of the background to draw
    bg_size_map = None

    def __init__(self):

        tile_image_center_size = (Tile.TILE_WIDTH, Tile.TILE_HEIGHT)
        tile_image_side_size = (self.side_width, Tile.TILE_HEIGHT)
        tile_image_bottom_size = (Tile.TILE_WIDTH, self.bottom_height)
        tile_image_corner_size = (self.side_width, self.bottom_height)

        self.bg_size_map = {
            Image_Section.CENTER: (Tile.TILE_WIDTH, Tile.TILE_HEIGHT),
            Image_Section.SIDE: (self.side_width, Tile.TILE_HEIGHT),
            Image_Section.BOTTOM: (Tile.TILE_WIDTH, self.bottom_height),
            Image_Section.CORNER: (self.side_width, self.bottom_height)
        }

        self.tiles_images = {
            Color.RED:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "flower_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            },
            Color.GREEN:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "bike_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            },
            Color.BLUE:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "cat_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            },
            Color.YELLOW:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "sun_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            },
            Color.BROWN:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "choco_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            },
            Color.PURPLE:
            {
                Image_Section.CENTER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "spaceship_tile.png")), tile_image_center_size),
                Image_Section.SIDE: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER: pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
            }
        }


class Game:
    # Main Class #
    board = None
    gameDisplay = None
    clock = None
    game_images = None
    language = None
    game_state = None

    display_width = 1280
    display_height = 720
    # to center the board in the window
    offset_board_x = 0
    tool_bar_height = 50
    fps = 120
    background_color = Color.BACKGROUND

    undo_button = None
    restart_button = None
    tile_count_label = None
    tile_counter_label = None
    score_counter_label = None
    new_highscore_label = None
    highscore_counter_label = None
    you_won_label = None
    you_lost_label = None

    end_panel = None

    score = 0
    save = None

    def __init__(self):
        # setting statics
        Tile.TILE_WIDTH = 45
        Tile.TILE_HEIGHT = int(1.6 * Tile.TILE_WIDTH)
        ratio_speed = self.fps / 60
        Tile.SPEED = Tile.SPEED / ratio_speed
        Tile.RESET_SPEED = Tile.SPEED
        Tile.ACCELERATION = 1 + ((Tile.ACCELERATION - 1) / ratio_speed)

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('MagneTile2')
        self.clock = pygame.time.Clock()
        self.game_images = Game_Images()
        self.language = Game_Language()
        self.game_state = Game_State.PLAYING
        self.save = Save()

        # undo button
        self.undo_button = Label(0, 0, "undo", Color.BLACK.value)
        self.undo_button.background_color = Color.WHITE
        (btn_width, btn_height) = self.get_size_of_label(self.undo_button)
        self.undo_button.update_size(btn_width, btn_height)
        self.undo_button.update_position(self.display_width / 2 - btn_width / 2, 5)

        # tile count label
        self.tile_count_label = Label(10, 5, "tile_count", Color.BLACK.value)
        (btn_width, btn_height) = self.get_size_of_label(self.tile_count_label)
        self.tile_count_label.update_size(btn_width, btn_height)

        # tile counter
        self.tile_counter_label = Label(self.tile_count_label.width + 7, 5, "0", Color.BLACK.value)
        self.tile_counter_label.background_color = self.background_color
        (btn_width, btn_height) = self.get_size_of_label(self.tile_counter_label, False)
        self.tile_counter_label.update_size(btn_width, btn_height)

        # score counter
        self.score_counter_label = Label(0, 5, "0", Color.RED.value)
        self.score_counter_label.background_color = self.background_color
        (btn_width, btn_height) = self.get_size_of_label(self.score_counter_label, False)
        self.score_counter_label.update_size(btn_width, btn_height)
        self.score_counter_label.update_position(self.display_width - btn_width - 10, 5)

        # end panel
        end_panel_width = 500
        end_panel_height = 400
        self.end_panel = Panel((self.display_width - end_panel_width) / 2, (self.display_height - end_panel_height) / 2, end_panel_width, end_panel_height, background_color=Color.WHITE, border_thickness=5, border_color=Color.BLACK)

        # winning label
        self.you_won_label = Label(0, 5, "you_won", Color.BLACK.value, 'Comic Sans MS', 50)
        (btn_width, btn_height) = self.get_size_of_label(self.you_won_label)
        self.you_won_label.update_size(btn_width, btn_height)
        self.you_won_label.update_position(self.display_width / 2 - btn_width / 2, self.end_panel.y + 40)

        # losing label
        self.you_lost_label = Label(0, 5, "you_lost", Color.BLACK.value, 'Comic Sans MS', 50)
        (btn_width, btn_height) = self.get_size_of_label(self.you_lost_label)
        self.you_lost_label.update_size(btn_width, btn_height)
        self.you_lost_label.update_position(self.display_width / 2 - btn_width / 2, self.you_won_label.y)

        # new highscore label
        self.new_highscore_label = Label(0, 5, "new_highscore", Color.RED.value, 'Comic Sans MS', 25)
        (btn_width, btn_height) = self.get_size_of_label(self.new_highscore_label)
        self.new_highscore_label.update_size(btn_width, btn_height)
        self.new_highscore_label.update_position(self.display_width / 2 - btn_width / 2, self.you_won_label.y + self.you_won_label.height + 75)

        # restart button
        self.restart_button = Label(0, 0, "restart", Color.BLACK.value)
        self.restart_button.background_color = Color.LIGHT_BLUE
        (btn_width, btn_height) = self.get_size_of_label(self.restart_button)
        self.restart_button.update_size(btn_width, btn_height)
        self.restart_button.update_position(self.display_width / 2 - btn_width / 2, self.end_panel.y + self.end_panel.height - btn_height - 50)

    def set_language_to_french(self):
        self.language.set_to_french()

    def set_language_to_english(self):
        self.language.set_to_english()

    def initialize_board(self, color_nb, col_nb, row_nb):
        print("Init board")
        self.offset_board_x = (self.display_width - (col_nb * Tile.TILE_WIDTH)) / 2
        Tile.X_OFFSET = self.offset_board_x
        Tile.Y_OFFSET = self.tool_bar_height
        self.board = Board(color_nb, col_nb, row_nb)

    def draw_label_raw(self, label):
        # Draws the label without translation #
        self.draw_label(label, False)

    def draw_label(self, label, with_translation=True):
        text_to_display = label.text
        if with_translation:
            text_to_display = self.language.get_text(label.text)

        text_font = pygame.font.SysFont(label.font_name, label.font_size)
        text_render = text_font.render(text_to_display, True, label.text_color)
        (width, height) = text_render.get_size()
        label.update_size(width, height)
        if label.background_color:
            pygame.draw.rect(self.gameDisplay, label.background_color.value, (label.x, label.y, width, height))
        self.gameDisplay.blit(text_render, label.get_coord())

    def draw_tile_count(self):
        (x, y) = self.tile_counter_label.get_coord()
        x = self.tile_count_label.width + 7
        self.tile_counter_label.update_position(x, y)
        pygame.draw.rect(self.gameDisplay, self.background_color.value, (x, y, self.tile_counter_label.width, self.tile_counter_label.height))
        self.tile_counter_label.text = str(self.board.tile_count)
        (new_width, new_height) = self.get_size_of_label(self.tile_counter_label, False)
        self.tile_counter_label.update_size(new_width, new_height)

        self.draw_label_raw(self.tile_counter_label)

    def hide_score_count(self):
        pygame.draw.rect(self.gameDisplay, self.background_color.value, (self.score_counter_label.x, self.score_counter_label.y, self.score_counter_label.width, self.score_counter_label.height))

    def draw_score_count(self):
        self.hide_score_count()
        (x, y) = self.score_counter_label.get_coord()
        self.score_counter_label.text = str(self.board.score_count)
        (new_width, new_height) = self.get_size_of_label(self.score_counter_label, False)
        self.score_counter_label.update_size(new_width, new_height)
        self.score_counter_label.update_position(self.display_width - new_width - 10, y)

        self.draw_label_raw(self.score_counter_label)

    def draw_end_score(self):
        end_score_text = self.language.get_text("score") + str(self.board.calculate_end_score(self.game_state == Game_State.WIN))
        self.end_score_label = Label(0, 0, end_score_text, Color.BLACK.value)
        (new_width, new_height) = self.get_size_of_label(self.end_score_label, False)
        self.end_score_label.update_size(new_width, new_height)
        self.end_score_label.update_position((self.display_width - new_width) / 2, self.you_won_label.y + self.you_won_label.height + 30)

        self.draw_label_raw(self.end_score_label)

    def draw_highscore(self):
        highscore = self.save.get_highscore()
        highscore_text = self.language.get_text("highscore") + str(highscore)
        self.highscore_label = Label(0, 0, highscore_text, Color.DARK_GRAY.value, 'Comic Sans MS', 25)
        (new_width, new_height) = self.get_size_of_label(self.highscore_label, False)
        self.highscore_label.update_size(new_width, new_height)
        self.highscore_label.update_position((self.display_width - new_width) / 2, self.end_score_label.y + self.end_score_label.height)

        self.draw_label_raw(self.highscore_label)

    def get_size_of_label(self, label, with_translation=True):
        text_to_display = label.text
        if with_translation:
            text_to_display = self.language.get_text(label.text)

        text_font = pygame.font.SysFont(label.font_name, label.font_size)
        text_render = text_font.render(text_to_display, True, label.text_color)
        return text_render.get_size()

    def draw_panel(self, panel):
        pygame.draw.rect(self.gameDisplay, panel.background_color.value, (panel.x, panel.y, panel.width, panel.height))
        if panel.border_thickness and panel.border_thickness > 0:
            (x, y, width, height) = panel.get_rect_border_left()
            pygame.draw.rect(self.gameDisplay, panel.border_color.value, (x, y, width, height))
            (x, y, width, height) = panel.get_rect_border_right()
            pygame.draw.rect(self.gameDisplay, panel.border_color.value, (x, y, width, height))
            (x, y, width, height) = panel.get_rect_border_top()
            pygame.draw.rect(self.gameDisplay, panel.border_color.value, (x, y, width, height))
            (x, y, width, height) = panel.get_rect_border_bottom()
            pygame.draw.rect(self.gameDisplay, panel.border_color.value, (x, y, width, height))

    ###
    # Draws a TIE (Tile_Image_Element)
    ###
    def draw_tie(self, tie):
        # draws a tie on the screen (tie is Tile Image Element) #
        pyimage_to_draw = self.game_images.tiles_images[tie.tile.color][tie.section]

        (x, y) = tie.tile.coord
        if tie.section == Image_Section.CENTER:
            coord = (x, y)
        elif tie.section == Image_Section.SIDE:
            coord = (x + Tile.TILE_WIDTH, y)
        elif tie.section == Image_Section.BOTTOM:
            coord = (x, y + Tile.TILE_HEIGHT)
        elif tie.section == Image_Section.CORNER:
            coord = (x + Tile.TILE_WIDTH, y + Tile.TILE_HEIGHT)

        self.gameDisplay.blit(pyimage_to_draw, coord)

    ###
    # Draws a list of TIEs (Tile_Image_Element)
    ###
    def draw_ties(self, list_of_ties):
        for tie in list_of_ties:
            self.draw_tie(tie)

    ###
    # Draws the whole board on the surface
    ###
    def draw_board(self):
        self.board.reset_tile_count()
        self.gameDisplay.fill(self.background_color.value)
        ties_to_draw = self.board.get_all_tie()
        for tie in ties_to_draw:
            self.draw_tie(tie)
        self.draw_label(self.undo_button)
        self.draw_label(self.tile_count_label)
        self.draw_tile_count()
        self.draw_score_count()

    ###
    # Draws the list of Tile_Image_Element bg_to_draw on the screen
    ###
    def draw_background_tiles(self, bg_to_draw):
        for tie in bg_to_draw:
            size = self.game_images.bg_size_map[tie.section] if tie.section else (tie.tile.TILE_WIDTH, tie.tile.TILE_HEIGHT)
            pygame.draw.rect(self.gameDisplay, self.background_color.value, pygame.Rect(tie.tile.coord, size))

    ###
    # Draws the moving tiles
    ###
    def draw_moving_tiles(self, moves):
        tie_list = []
        for m in moves:
            t = m.tile
            all_ties = t.get_tie_all_sides()
            tie_list += all_ties
        self.draw_ties(tie_list)

    def display_end_panel(self, label, new_highscore):
        self.hide_score_count()
        self.draw_panel(self.end_panel)
        self.draw_label(label)
        self.draw_end_score()
        if not new_highscore:
            self.draw_highscore()
        else:
            self.draw_label(self.new_highscore_label)

        self.draw_label(self.restart_button)

    def display_end_screen(self, game_state, new_highscore):
        if game_state == Game_State.WIN:
            self.display_end_panel(self.you_won_label, new_highscore)
        if game_state == Game_State.LOSE:
            self.display_end_panel(self.you_lost_label, new_highscore)

    def compute_highscore(self, game_won):
        highscore = self.save.get_highscore()
        new_highscore = self.board.calculate_end_score(game_won)
        if highscore < new_highscore:
            self.save.save_highscore(new_highscore)
            return True
        return False

    def run(self):
        # GAME LOOP #
        self.draw_board()
        pygame.display.update()

        processing_falling_movements = False
        processing_sliding_movements = False
        bg_to_draw = []  # list of Tile_Image_Element that represents the background to draw
        sides_to_draw = []  # list of Tile_Image_Element

        app_running = True

        coord_mouse_down = None
        coord_mouse_up = None
        board_clicked = False
        undo_clicked = False
        restart_clicked = False

        while app_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                coord_mouse_down = pygame.mouse.get_pos()
                board_clicked = False
                undo_clicked = False
                restart_clicked = False

            if event.type == pygame.MOUSEBUTTONUP:
                coord_mouse_up = pygame.mouse.get_pos()
                if coord_mouse_down:
                    if self.undo_button.is_clicked(coord_mouse_down) and self.undo_button.is_clicked(coord_mouse_up):
                        undo_clicked = True
                        print("Undo clicked")

                    if self.board.is_clicked(coord_mouse_down) and self.board.is_clicked(coord_mouse_up):
                        board_clicked = True
                        print("Board clicked")

                    if self.restart_button.is_clicked(coord_mouse_down) and self.restart_button.is_clicked(coord_mouse_up):
                        restart_clicked = True
                        print("Restart clicked")

            game_clicked = coord_mouse_down and coord_mouse_up
            if game_clicked:
                print("Game clicked")

            if (self.game_state == Game_State.PLAYING):

                if not (processing_falling_movements or processing_sliding_movements):

                    if game_clicked:

                        if board_clicked:
                            result_process_mouse_up = self.board.process_click(coord_mouse_down, coord_mouse_up)
                            if result_process_mouse_up:
                                (sides_to_draw, bg_to_draw) = result_process_mouse_up
                                processing_falling_movements = True
                                self.draw_tile_count()
                                self.draw_score_count()
                                pygame.display.update()

                        if undo_clicked:
                            last_hist_step = self.board.undo_step()
                            if (last_hist_step):
                                self.draw_board()
                                pygame.display.update()

                        coord_mouse_down = None
                        coord_mouse_up = None

                else:
                    self.draw_background_tiles(bg_to_draw)

                    if processing_falling_movements and not processing_sliding_movements:
                        # Falling tiles
                        processing_falling_movements = not self.board.moves_tiles_downward()

                        self.draw_ties(sides_to_draw)

                    if not processing_falling_movements:

                        if not processing_sliding_movements:
                            if self.board.compute_side_movements():
                                # Compute first time sliding tiles
                                bg_to_draw = [self.board.compute_background_to_draw_for_sliding(self.board.sideway_moves, self.game_images.side_width, self.game_images.bottom_height)]
                                processing_sliding_movements = True
                        else:
                            # Sliding tiles
                            processing_sliding_movements = not self.board.moves_tiles_left()
                            self.draw_moving_tiles(self.board.sideway_moves)

                    if not (processing_falling_movements or processing_sliding_movements):
                        # Finished moving tiles
                        bg_to_draw = []
                        sides_to_draw = []
                        self.game_state = self.board.check_game_over()
                        self.board.post_processing_movements()

                    pygame.display.update()

            else:  # GAME OVER
                if self.game_state != Game_State.FINISHED:
                    game_won = self.game_state == Game_State.WIN
                    new_highscore = self.compute_highscore(game_won)
                    self.display_end_screen(self.game_state, new_highscore)
                    self.game_state = Game_State.FINISHED
                    pygame.display.update()
                    coord_mouse_down = None
                    coord_mouse_up = None
                else:  # Game is idle
                    if game_clicked:
                        if undo_clicked:
                            last_hist_step = self.board.undo_step()
                            if (last_hist_step):
                                self.draw_board()
                                self.game_state = Game_State.PLAYING
                                pygame.display.update()

                        if restart_clicked:
                            # Restarts the game
                            self.board.reset()
                            self.draw_board()
                            self.game_state = Game_State.PLAYING
                            pygame.display.update()

                        coord_mouse_down = None
                        coord_mouse_up = None

            self.clock.tick(self.fps)
