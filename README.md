# MagneTile
Simple tile game in python

## Game rules
You need to get rid of all the tiles on the board. Tiles of the same color that are grouped by 2 or more can be removed by clicking on them. Tiles above the ones disapearing will drop to fill the gaps and therefore create new groups of tile. If there is an empty column on the board, it will also get rid of it by sliding columns to the left to fill the gap. 

## Installation
You will need Python 3 and [Pygame](https://www.pygame.org/) 

Simply run it with the command : 
```bash
python magnetile.py [-l language] [-c number_of_colors]
```

The language can be either "english" or "french". Default language is English.

The number of color is between 3 and 5. Default number is 5.
