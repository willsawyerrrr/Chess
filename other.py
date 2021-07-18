""" Other functions used to operate the Chess game. """

from pieces import *
import PySimpleGUI as sg


def DarkCell(position):
    """ Returns a PySimpleGUI image element with a black background. """
    return sg.Button(button_color="black", key=position)


def LightCell(position):
    """ Returns a PySimpleGUI image element with a white background. """
    return sg.Button(button_color="white", key=position)


def new_game(window):
    """ Initialises pieces and resets count and winner for a new game. """
    black = [
        Rook((0, 0), "Black"),
        Knight((0, 1), "Black"),
        Bishop((0, 2), "Black"),
        Queen((0, 3), "Black"),
        King((0, 4), "Black"),
        Bishop((0, 5), "Black"),
        Knight((0, 6), "Black"),
        Rook((0, 7), "Black"),
        Pawn((1, 0), "Black"),
        Pawn((1, 1), "Black"),
        Pawn((1, 2), "Black"),
        Pawn((1, 3), "Black"),
        Pawn((1, 4), "Black"),
        Pawn((1, 5), "Black"),
        Pawn((1, 6), "Black"),
        Pawn((1, 7), "Black")
    ]

    white = [
        Pawn((6, 0), "White"),
        Pawn((6, 1), "White"),
        Pawn((6, 2), "White"),
        Pawn((6, 3), "White"),
        Pawn((6, 4), "White"),
        Pawn((6, 5), "White"),
        Pawn((6, 6), "White"),
        Pawn((6, 7), "White"),
        Rook((7, 0), "White"),
        Knight((7, 1), "White"),
        Bishop((7, 2), "White"),
        King((7, 3), "White"),
        Queen((7, 4), "White"),
        Bishop((7, 5), "White"),
        Knight((7, 6), "White"),
        Rook((7, 7), "White")
    ]

    for i in range(8):
        for j in range(8):
            window[(i, j)].update(image_filename="", image_size=(75, 75))

    for piece in black:
        piece.update_position(window, piece.get_position())
    for piece in white:
        piece.update_position(window, piece.get_position())
    window["turn"].update("It's White's turn.")

    initial = None
    destination = None
    count = 0
    turns = {0: "White", 1: "Black"}

    return black, white, initial, destination, count, turns


def check_endgame(black, white):
    """ Determines whether each team still has a King.

    Parameters
    ----------
    black : list[Piece]
        The list of current Black 
    white : list[Piece]
        The list of current White 

    Returns
    -------
    Union[str, NoneType]
        The winner as a string, if appropriate. None otherwise.
    """
    b_king = False
    for piece in black:
        if piece.get_type() == "King":
            b_king = True
    if not b_king:
        return "White"
    w_king = False
    for piece in white:
        if piece.get_type() == "King":
            w_king = True
    if not w_king:
        return "Black"
    return None
