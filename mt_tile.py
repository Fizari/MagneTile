try:
    import pygame
except ModuleNotFoundError:
    print("### Please install pygame : pip install pygame ###")
    raise
from mt_enums import Color, Image_Section

class Tile_Image_Element:
    """ Represents the part of the tile that needs to be drawn on the screen """
    color = None # mt_enums.Color
    section = None # mt_enums.Image_Section
    coord = (0,0) # position of the element on screen

    def __init__(self, color, section, x, y):
        self.color = color
        self.section = section
        self.coord = (x, y)

class Tile:
    """ Represents a Tile in space """
    x_offset = 0
    y_offset = 0
    i = 0
    j = 0
    tile_width = 0
    tile_height = 0
    rect = pygame.Rect(0,0,0,0)
    color = None # /!\ Color enum (not Tuple)
    speed = 6 # speed when drawing
    k = 1.05 # acceleration factor

    def __init__(self, i, j, color, tile_width, tile_height, x_offset, y_offset):
        self.i = i
        self.j = j
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.tile_width = tile_width
        self.tile_height= tile_height
        x = i*tile_width + self.x_offset
        y = j*tile_height + self.y_offset
        self.rect = pygame.Rect((x,y),(tile_width, tile_height))
        self.color = color

    def get_supposed_coord(self):
        return (self.i*self.tile_width + self.x_offset, self.j*self.tile_height + self.y_offset)

    def get_coord_from_grid_pos(self, i, j):
        return (i*self.tile_width + self.x_offset, j*self.tile_height + self.y_offset)

    def move(self, i, j):
        self.i = i
        self.j = j
        x = i*self.tile_width + self.x_offset
        y = j*self.tile_height + self.y_offset
        self.rect = pygame.Rect((x,y),(self.tile_width, self.tile_height))

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
            self.rect = pygame.Rect((curr_x,curr_y + self.speed),(self.tile_width, self.tile_height))
            return False

    def slide_left_to(self, i, j):
        """Draws the tile sliding left toward (i,j), same as fall_to(self, i, j)"""
        (x,y) = self.get_coord_from_grid_pos(i,j)
        if self.rect.x - self.speed <= x:
            return True
        else:
            curr_x = self.rect.x
            curr_y = self.rect.y
            self.rect = pygame.Rect((curr_x - self.speed,curr_y),(self.tile_width, self.tile_height))
            return False

    def get_tie_center(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self.color, Image_Section.CENTER, self.rect.x, self.rect.y)

    def get_tie_side(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self.color, Image_Section.SIDE, self.rect.right, self.rect.y) 

    def get_tie_bottom(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self.color, Image_Section.BOTTOM, self.rect.x, self.rect.bottom) 

    def get_tie_corner(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self.color, Image_Section.CORNER, self.rect.right, self.rect.bottom) 

    def get_tie_all_sides(self):
        tie_list = []
        tie_list.append(self.get_tie_center())
        tie_list.append(self.get_tie_side())
        tie_list.append(self.get_tie_bottom())
        tie_list.append(self.get_tie_corner())
        return tie_list

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