from mt_enums import Color


class Label:
    """ Represents a non clickable text without background """
    coord = (0, 0)
    text_color = Color.BLACK.value
    text = ""
    font_name = "Comic Sans MS"
    font_size = 30

    width = 0
    height = 0

    def __init__(self, x, y, text, text_color=Color.BLACK.value, font_name='Comic Sans MS', font_size=30):
        """ (x,y) are the coordinates of the text on the screen """
        self.coord = (x, y)
        self.text = text
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size

    def update(self, text):
        self.text = text

    def update_size(self, width, height):
        self.width = width
        self.height = height

    def update_position(self, new_coord):
        self.coord = new_coord

    def is_clicked(self, mouse_coord):
        (mouse_x, mouse_y) = mouse_coord
        (x, y) = self.coord
        return mouse_x >= x and mouse_y >= y and mouse_x <= (x + self.width) and mouse_y <= (y + self.height)
