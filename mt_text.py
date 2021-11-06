from mt_enums import Color


class Label:
    """ Represents a non clickable text without background """
    x = 0
    y = 0
    text_color = Color.BLACK.value
    background_color = Color.WHITE.value
    text = ""
    font_name = "Comic Sans MS"
    font_size = 30

    width = 0
    height = 0

    def __init__(self, x, y, text, text_color=Color.BLACK.value, font_name='Comic Sans MS', font_size=30, background_color=None):
        """ (x,y) are the coordinates of the text on the screen """
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size
        self.background_color = background_color

    def get_coord(self):
        return (self.x, self.y)

    def update(self, text):
        self.text = text

    def update_size(self, width, height):
        self.width = width
        self.height = height

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def is_clicked(self, mouse_coord):
        (mouse_x, mouse_y) = mouse_coord
        return mouse_x >= self.x and mouse_y >= self.y and mouse_x <= (self.x + self.width) and mouse_y <= (self.y + self.height)


class Panel:
    x = 0
    y = 0
    width = 0
    height = 0
    background_color = Color.WHITE.value
    border_thickness = 0
    border_color = Color.BLACK.value

    def __init__(self, x, y, width, height, background_color=Color.WHITE.value, border_thickness=0, border_color=Color.BLACK.value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_thickness = border_thickness
        self.border_color = border_color

    def get_rect_border_left(self):
        return (self.x - self.border_thickness, self.y, self.border_thickness, self.height)

    def get_rect_border_right(self):
        return (self.x + self.width, self.y, self.border_thickness, self.height)

    def get_rect_border_top(self):
        return (self.x, self.y - self.border_thickness, self.width, self.border_thickness)

    def get_rect_border_bottom(self):
        return (self.x, self.y + self.height, self.width, self.border_thickness)
