from mt_enums import Color, Image_Section

class Tile_Image_Element:
    """ Represents the part of the tile that needs to be drawn on the screen """
    section = None # mt_enums.Image_Section
    tile = None # Tile

    def __init__(self, tile, section):
        self.tile = tile
        self.section = section

class Tile:
    """ Represents a Tile in space """

    # STATIC VARIABLES
    TILE_WIDTH = 0 
    TILE_HEIGHT = 0 
    X_OFFSET = 0
    Y_OFFSET = 0

    i = 0
    j = 0
    coord = (0,0) # coordinates on the screen 
    color = None # /!\ Color enum (not Tuple)
    speed = 6 # speed when drawing
    k = 1.05 # acceleration factor

    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        x = i*self.TILE_WIDTH + self.X_OFFSET
        y = j*self.TILE_HEIGHT + self.Y_OFFSET
        self.coord = (x,y)
        self.color = color

    def get_x(self):
        (curr_x, curr_y) = self.coord
        return curr_x

    def get_y(self):
        (curr_x, curr_y) = self.coord
        return curr_y

    def get_pos_left(self):
        return self.get_x()

    def get_pos_right(self):
        return self.get_x() + self.TILE_WIDTH

    def get_pos_top(self):
        return self.get_y()

    def get_pos_bottom(self):
        return self.get_y() + self.TILE_HEIGHT

    def get_supposed_coord(self):
        return (self.i*self.TILE_WIDTH + self.X_OFFSET, self.j*self.TILE_HEIGHT + self.Y_OFFSET)

    def get_coord_from_grid_pos(self, i, j):
        return (i*self.TILE_WIDTH + self.X_OFFSET, j*self.TILE_HEIGHT + self.Y_OFFSET)

    def move(self, i, j):
        self.i = i
        self.j = j
        x = i*self.TILE_WIDTH + self.X_OFFSET
        y = j*self.TILE_HEIGHT + self.Y_OFFSET
        self.coord = (x,y)

    def is_in_place(self):
        (curr_x,curr_y) = self.coord
        (supposed_x, supposed_y) = self.get_coord_from_grid_pos()
        return curr_x == supposed_x and curr_y == supposed_y

    def __accelerate(self):
        self.speed *= self.k

    def __stop_speed(self):
        self.speed = 6

    def fall_to(self, i, j):
        """Draws the tile falling toward (i,j), only the coordinates of the tile are moving, not the (i,j) coordinates"""
        (curr_x, curr_y) = self.coord
        (dest_x, dest_y) = self.get_coord_from_grid_pos(i,j)
        if curr_y + self.speed >= dest_y:
            self.__stop_speed()
            return True
        else:
            self.__accelerate()
            self.coord = (curr_x,curr_y + self.speed)
            return False 

    def slide_left_to(self, i, j):
        """Draws the tile sliding left toward (i,j), same as fall_to(self, i, j)"""
        (curr_x, curr_y) = self.coord
        (dest_x, dest_y) = self.get_coord_from_grid_pos(i,j)
        if curr_x - self.speed <= dest_x:
            return True
        else:
            self.coord = (curr_x - self.speed,curr_y)
            return False

    def get_tie_center(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self, Image_Section.CENTER)

    def get_tie_side(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self, Image_Section.SIDE) 

    def get_tie_bottom(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self, Image_Section.BOTTOM) 

    def get_tie_corner(self):
        ### tie = tile_image_element ###
        return Tile_Image_Element(self, Image_Section.CORNER) 

    def get_tie_all_sides(self):
        tie_list = []
        tie_list.append(self.get_tie_center())
        tie_list.append(self.get_tie_side())
        tie_list.append(self.get_tie_bottom())
        tie_list.append(self.get_tie_corner())
        return tie_list

    def is_clicked(self, mouse_coord):
        (mouse_x, mouse_y) = mouse_coord
        (x, y) = self.coord
        return mouse_x >= x and mouse_y >= y and mouse_x <= (x + self.TILE_WIDTH) and mouse_y <= (y + self.TILE_HEIGHT)

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