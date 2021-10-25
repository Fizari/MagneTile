from mt_board import Board
from mt_enums import Color, Game_State, Image_Section
from mt_tile import Tile_Image_Element, Tile
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
            "undo" : "Annuler",
            "restart" : "Rejouer",
            "you_won" : "Vous avez gagné !! :)",
            "you_lost" : "Vous avez perdu",
            "tile_count" : "Tuiles : "
        }
        self.english_text_map = {
            "undo" : "Undo",
            "restart" : "Play again",
            "you_won" : "You won !! :)",
            "you_lost" : "You lost",
            "tile_count" : "Tiles : "
        }
        self.set_to_english() # default value

    def set_to_french(self):
        self.text_map = self.french_text_map

    def set_to_english(self):
        self.text_map = self.english_text_map

class Game_Images:
    ### Images that are gonna be drawn on the screen ###
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
            Image_Section.CENTER : (Tile.TILE_WIDTH, Tile.TILE_HEIGHT),
            Image_Section.SIDE : (self.side_width, Tile.TILE_HEIGHT),
            Image_Section.BOTTOM : (Tile.TILE_WIDTH, self.bottom_height),
            Image_Section.CORNER : (self.side_width, self.bottom_height)
        }

        self.tiles_images = {
            Color.RED : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "flower_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),tile_image_corner_size),
                },
            Color.GREEN : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "bike_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
                },
            Color.BLUE : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "cat_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
                },
            Color.YELLOW : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "sun_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
                },
            Color.BROWN : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "choco_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir,self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
                },
            Color.PURPLE : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "spaceship_tile.png")), tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir,self.images_folder, "tile_side.png")), tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), tile_image_bottom_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")), tile_image_corner_size),
                }
        }

class Game:
    ### Main Class ###
    board = None
    gameDisplay = None
    clock = None
    game_images = None
    language = None
    game_state = None

    display_width = 1100
    display_height = 720
    #to center the board in the window
    offset_board_x = 0
    tool_bar_height = 50
    fps = 60
    background_color = Color.BACKGROUND

    score = 0

    def __init__(self):
        # setting statics
        Tile.TILE_WIDTH = 45
        Tile.TILE_HEIGHT = int(1.6*Tile.TILE_WIDTH)

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('MagneTile2')
        self.clock = pygame.time.Clock()
        self.game_images = Game_Images()
        self.language = Game_Language()
        self.game_state = Game_State.PLAYING

    def set_language_to_french(self):
        language.set_to_french()

    def set_language_to_english(self):
        language.set_to_english()
        
    def initialize_board(self, color_nb, col_nb, row_nb):
        print("Init board")
        self.offset_board_x = (self.display_width - (col_nb*Tile.TILE_WIDTH)) / 2
        Tile.X_OFFSET = self.offset_board_x
        Tile.Y_OFFSET = self.tool_bar_height
        self.board = Board(color_nb, col_nb, row_nb)

    ###
    # Draws a TIE (Tile_Image_Element)
    ###
    def draw_tie(self, tie):
        ### draws a tie on the screen (tie is Tile Image Element) ###
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
    ###
    # Draws the list of Tile_Image_Element bg_to_draw on the screen
    ###
    def draw_background_tiles(self, bg_to_draw):
        for tie in bg_to_draw:
            size = self.game_images.bg_size_map[tie.section] if tie.section else (tie.tile.TILE_WIDTH, tie.tile.TILE_HEIGHT)
            pygame.draw.rect(self.gameDisplay, self.background_color.value, pygame.Rect(tie.tile.coord,size))

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

    def run(self): 
        ### GAME LOOP ###
        self.draw_board()
        pygame.display.update()

        processing_falling_movements = False
        processing_sliding_movements = False
        bg_to_draw = [] # list of Tile_Image_Element that represents the background to draw
        sides_to_draw = [] # list of Tile_Image_Element

        app_running = True
        while app_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_running = False

            if (self.game_state == Game_State.PLAYING):

                if not (processing_falling_movements or processing_sliding_movements):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.board.is_clicked(mouse_pos): # board click
                            self.board.process_click_mouse_down(mouse_pos)

                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.board.is_clicked(mouse_pos): # board click
                            result_process_mouse_up = self.board.process_click_mouse_up(mouse_pos)
                            if result_process_mouse_up:
                                (sides_to_draw, bg_to_draw) = result_process_mouse_up
                                processing_falling_movements = True
                                pygame.display.update()

                else:
                    self.draw_background_tiles(bg_to_draw)

                    ############### WIP 
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
                            #Sliding tiles
                            processing_sliding_movements = not self.board.moves_tiles_left()
                            self.draw_moving_tiles(self.board.sideway_moves)

                    if not (processing_falling_movements or processing_sliding_movements):
                        # Finished moving tiles
                        bg_to_draw = []
                        sides_to_draw = []
                        #game_over = check_game_over()
                        #history.add_tile_movements_to_current_step(self.board.sideway_moves)
                        #history.add_tile_movements_to_current_step(self.board.downward_moves)
                    pygame.display.update()


            else: # GAME OVER
                print("game over")
            self.clock.tick(self.fps)

