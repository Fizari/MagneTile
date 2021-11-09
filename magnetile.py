from mt_game import Game
import getopt
import sys


def print_help(number_of_color_min, number_of_color):
    print("usage : magnetile.py [-l language] [-c number_of_colors]")
    print("        Languages are : french or english (default)")
    print("        The number of colors can be between " + str(number_of_color_min) + " and " + str(number_of_color) + " included. Default is " + str(number_of_color))


def main():
    try:
        options, remainder = getopt.getopt(sys.argv[1:], "hl:c:", ["language=", "--help", "colors="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    number_of_color = 6
    number_of_color_min = 3
    game = Game()

    for opt, arg in options:
        if opt in ("-l", "--language"):
            if arg == "french":
                game.set_language_to_french()
            elif arg == "english":
                game.set_language_to_english()
            else:
                print("Languages are : french or english (default)")
                sys.exit(2)
        if opt in ("-c", "--colors"):
            nb = 0
            try:
                nb = int(arg)
            except():
                print_help()
                sys.exit(2)
            if nb <= number_of_color and nb >= number_of_color_min:
                number_of_color = nb
            else:
                print("Please choose a number of colors between " + str(number_of_color_min) + " and " + str(number_of_color))
                sys.exit(2)
        if opt in ("-h", "--help"):
            print_help(number_of_color_min, number_of_color)
            sys.exit(2)

    col_nb = 22
    row_nb = 9
    # game.initialize_board(3, col_nb, row_nb)
    game.initialize_board(number_of_color, col_nb, row_nb)
    game.run()
    # game.run_stats(10000)
    # game.run_auto_play()


main()
