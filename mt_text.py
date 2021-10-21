try:
    import pygame
except ModuleNotFoundError:
    print("### Please install pygame : pip install pygame ###")
    raise
from mt_enums import Color

class Text_Display:
    """ Represents a non clickable text without background """
    x = 0
    y = 0
    rect = pygame.Rect(0,0,0,0)
    text_render = None

    text_color = Color.BLACK.value
    font_name = 'Comic Sans MS'
    font_size = 30

    def __init__(self, x, y, text, text_color=Color.BLACK.value, font_name='Comic Sans MS', font_size=30):
        """ (x,y) are the coordinates of the text's center"""
        text_font = pygame.font.SysFont(font_name, font_size)
        self.text_render = text_font.render(text, True, text_color)
        width = self.text_render.get_rect().width
        height = self.text_render.get_rect().height
        self.text_color = text_color
        self.font_name = font_name
        self.font_size = font_size
        self.x = x - width / 2
        self.y = y - height / 2
        self.rect = pygame.Rect(self.x,self.y,width,height)

    def draw(self, gameDisplay):
        gameDisplay.blit(self.text_render,(self.x,self.y))

    def update(self, text):
        text_font = pygame.font.SysFont(self.font_name, self.font_size)
        self.text_render = text_font.render(text, True, self.text_color)

    def update_and_draw(self, text, gameDisplay, background_color=None):
        if (background_color):
            pygame.draw.rect(gameDisplay, background_color, self.rect)
        self.update(text)
        self.draw(gameDisplay)

class Text_Button:
    x = 0
    y = 0
    text_color = Color.BLACK.value
    background_color = Color.WHITE.value
    rect = pygame.Rect(0,0,0,0)
    btn_render = None

    border_thickness = 2
    border_color = Color.BLACK.value
    border_padding = 5

    def __init__(self, x, y, text):
        """ (x,y) are the coordinates of the button's center"""
        font_btn = pygame.font.SysFont('Comic Sans MS', 30)
        self.btn_render = font_btn.render(text, True, self.text_color, self.background_color)
        width = self.btn_render.get_rect().width
        height = self.btn_render.get_rect().height
        self.x = x - width / 2
        self.y = y - height / 2
        self.rect = pygame.Rect(self.x,self.y,width,height)

    def __draw_border(self, gameDisplay):
        border_width = self.rect.width + self.border_thickness * 8 + self.border_padding * 2
        border_height = self.rect.height +  self.border_thickness * 2

        border_rect = pygame.Rect((self.x - self.border_thickness *4 - self.border_padding, self.y - self.border_thickness),(border_width, border_height))
        mask_rect = pygame.Rect((border_rect.x + self.border_thickness *4, border_rect.y + self.border_thickness),(border_rect.width - self.border_thickness * 8, border_rect.height - self.border_thickness * 2))
        pygame.draw.rect(gameDisplay, self.border_color, pygame.Rect(border_rect))
        pygame.draw.rect(gameDisplay, self.background_color, pygame.Rect(mask_rect))


    def draw(self, gameDisplay):
        self.__draw_border(gameDisplay)
        gameDisplay.blit(self.btn_render,(self.x,self.y))

    def collides_with(self, coord):
        return self.rect.collidepoint(coord)