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

    tile_width = 45
    tile_height = int(1.6*tile_width)
    side_width = 10
    bottom_height = 10
    tile_image_center_size = (tile_width, tile_height)
    tile_image_side_size = (side_width, tile_height)
    tile_image_bottome_size = (tile_width, bottom_height)
    tile_image_corner_size = (side_width, bottom_height)
    images_folder = "images"
    root_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.tiles_images = {
            Color.RED : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "flower_tile.png")), self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
                },
            Color.GREEN : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "bike_tile.png")),self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
                },
            Color.BLUE : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "cat_tile.png")),self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
                },
            Color.YELLOW : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "sun_tile.png")),self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
                },
            Color.BROWN : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "choco_tile.png")),self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir,self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
                },
            Color.PURPLE : {
                Image_Section.CENTER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "spaceship_tile.png")),self.tile_image_center_size),
                Image_Section.SIDE : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir,self.images_folder, "tile_side.png")), self.tile_image_side_size),
                Image_Section.BOTTOM : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_bottom.png")), self.tile_image_bottome_size),
                Image_Section.CORNER : pygame.transform.scale(pygame.image.load(os.path.join(self.root_dir, self.images_folder, "tile_corner.png")),self.tile_image_corner_size),
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
    tile_width = 45
    tile_height = int(1.6*tile_width)
    fps = 60
    background_color = Color.BACKGROUND

    score = 0

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('MagneTile2')
        self.gameDisplay.fill((119, 237, 131))
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
        self.offset_board_x = (self.display_width - (col_nb*self.tile_width)) / 2
        self.board = Board(color_nb, col_nb, row_nb, self.tile_width, self.tile_height, self.offset_board_x, self.tool_bar_height)

    def draw_tie(self, tie):
        ### draws a tie on the screen (tie is Tile Image Element) ###
        pyimage_to_draw = self.game_images.tiles_images[tie.color][tie.section]
        #print("drawing tile" + str(tie.coord))
        self.gameDisplay.blit(pyimage_to_draw, tie.coord)
        
    ###
    # Draws the whole board on the surface
    ###
    def draw_board(self):
        self.board.reset_tile_count()
        self.gameDisplay.fill(self.background_color.value)
        ties_to_draw = self.board.get_all_tie()
        for tie in ties_to_draw:
            self.draw_tie(tie)
        
    def draw_tile_count_text(self):
        tile_count_text.draw(self.gameDisplay)
        tile_count_number.update_and_draw(str(tile_count),self.gameDisplay,self.background_color.value)

    def draw_undo_button(self):
        undo_button.draw(self.gameDisplay)

    def run(self): 
        ### GAME LOOP ###
        self.draw_board()
        pygame.display.update()

        app_running = True
        while app_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_running = False

            if (self.game_state == Game_State.PLAYING):

                if not self.board.is_processing_movements():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.board.is_clicked(mouse_pos): # board click
                            self.board.process_click_mouse_down(mouse_pos)

                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.board.is_clicked(mouse_pos): # board click
                            self.board.process_click_mouse_up(mouse_pos)

                else:
                    print("Processing movements")


            else: # GAME OVER
                print("game over")
            self.clock.tick(self.fps)

