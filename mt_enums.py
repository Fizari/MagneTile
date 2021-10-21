import enum
class Color(enum.Enum):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GRAY = (175, 185, 204)
    RED = (237, 125, 119)
    GREEN = (119, 237, 131)
    BLUE = (119, 160, 237)
    YELLOW = (237, 215, 119)
    BROWN = (156, 107, 78)
    PURPLE = (166, 59, 211)
    ORANGE = (250, 183, 0)
    DARK_BLUE = (46, 50, 128)

class Game_Over(enum.Enum):
   WIN = 1
   LOSE = 2
   PLAYING = 3

class Direction(enum.Enum):
   LEFT = 1
   UP = 2
   RIGHT = 3
   DOWN = 4

#class Perspective(enum.Enum):
#   SIDE = 1
#   BOTTOM = 2
#   CORNER = 3

class Image_Section(enum.Enum):
  CENTER = 0
  SIDE = 1
  BOTTOM = 2
  CORNER = 3