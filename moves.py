""" Functions used to validate movements and attacks of chess pieces. """

import PySimpleGUI as sg
from paths import Path


def get_direction(initial, destination):
    """ Returns the direction in which the piece has attempted to move or
    attack.

    Parameters
    ----------
    initial : tuple[int, int]
        The position from which the piece has attempted to move or attack.
    destination : tuple[int, int]
        The position to which the piece has attempted to move or attack.

    Returns
    -------
    str
        The direction in which the piece has moved.
    """
    y = destination[0] - initial[0]
    x = destination[1] - initial[1]
    if x < 0:
        x = -1
    elif x > 0:
        x = 1
    if y < 0:
        y = -1
    elif y > 0:
        y = 1
    directions = {
        (0, 0): None,
        (0, -1): "up",
        (0, 1): "down",
        (-1, 0): "left",
        (1, 0): "right",
        (-1, -1): "top-left",
        (1, -1): "top-right",
        (-1, 1): "bottom-left",
        (1, 1): "bottom-right"
    }
    return directions[(x, y)]


def validate_move(piece, direction, window):
    """ Determines whether the piece can move in a given direction.

    Parameters
    ----------
    piece : Piece
        The piece which has attempted to move.
    direction : str
        The direction in which the piece has attempted to moved.
    window : sg.Window
        The Chess game window.

    Returns
    -------
    bool
        True if the move is valid. False otherwise.
    """
    if direction in piece.get_move():
        return True
    error_msg = f"Your {piece.get_type()} can't move in that direction."
    window["out"].update(error_msg)
    return False


def validate_attack(piece, direction, window):
    """ Determines whether the piece can attack in a given direction.

    Parameters
    ----------
    piece : Piece
        The piece which has attempted to attack.
    direction : str
        The direction in which the piece has attempted to attack.
    window : sg.Window
        The Chess game window.

    Returns
    -------
    bool
        True if the attack is valid. False otherwise.
    """
    if direction in piece.get_attack():
        return True
    error_msg = f"Your {piece.get_type()} can't attack in that direction."
    window["out"].update(error_msg)
    return False


def validate_position(piece, black, white, position, window):
    """ Determines whether a piece can move to or attack at a given position.

    Parameters
    ----------
    piece : Piece
        The piece which has attempted to move or attack.
    black : list[Piece]
        The list of current Black pieces.
    white : list[Piece]
        The list of current White pieces.
    position : tuple[int, int]
        The position to which the piece has attempted to move or attack.
    window : sg.Window
        The Chess game window.

    Returns
    -------
    bool
        True if the position is valid. False otherwise.
    """
    pos_piece = get_piece(black, white, position)
    if piece.get_team() == pos_piece.get_team():
        if piece.get_type() == pos_piece.get_type():
            error_msg = f"Your {piece.get_type()} can't move there. " \
                        f"Your other {pos_piece.get_type()} is already there."
        else:
            error_msg = f"Your {piece.get_type()} can't move there. " \
                        f"Your {pos_piece.get_type()} is already there."
        window["out"].update(error_msg)
        return False
    return True


def validate_path(piece, black, white, initial, destination, direction, window):
    """ Determines whether a piece can follow a path between two cells.

    Parameters
    ----------
    piece : Piece
        The piece which has attempted to move or attack.
    black : list[Piece]
        The list of current Black pieces.
    white : list[Piece]
        The list of current White pieces.
    initial : tuple[int, int]
        The position from which the piece has attempted to move or attack.
    destination : tuple[int, int]
        The position to which the piece has attempted to move or attack.
    direction : str
        The direction in which the piece has attempted to move or attack.
    window : sg.Window
        The Chess game window.

    Returns
    -------
    bool
        True if the path is valid. False otherwise.
    """
    y = destination[0] - initial[0]
    x = destination[1] - initial[1]
    piece_type = piece.get_type()
    team = piece.get_team()
    error_msg = f"Your {piece_type} can't move that far."
    if piece_type == "Pawn" and abs(y) > 2:
        # If a Pawn moves more than two cells.
        window["out"].update(error_msg)
        return False
    elif piece_type == "Pawn" and not piece.get_initial and abs(y) == 2:
        # If a Pawn which hasn't moved yet moves more than two cells.
        window["out"].update(error_msg)
        return False
    elif piece_type == "King" and (abs(x) > 1 or abs(y) > 1):
        # If a Pawn or King moves more than one cell.
        window["out"].update(error_msg)
        return False

    path = Path(initial, destination, direction)
    if not path.is_valid():
        window["out"].update(f"Your {piece_type} can't move in that direction.")
        return False
    for cell in path.get_cells():
        blockage = get_piece(black, white, cell)
        if blockage is not None:
            if blockage.get_team() == team:
                error_msg = f"Your {piece_type} can't move here. It's path " \
                            f"is blocked by your {blockage.get_type()}."
            else:
                error_msg = f"Your {piece_type} can't move here. It's path " \
                            f"is blocked by your {blockage.get_type()}."
            window["out"].update(error_msg)
            return False
    return True


def knight(initial, destination, window):
    """ Determines whether a Knight can move or attack to a given position.

    Parameters
    ----------
    initial : tuple[int, int]
        The position from which the piece has attempted to move or attack.
    destination : tuple[int, int]
        The position to which the piece has attempted to move or attack.
    window : sg.Window
        The Chess game window.

    Returns
    -------
    bool
        True if the move or attack is valid. False otherwise.
    """
    y = abs(destination[0] - initial[0])
    x = abs(destination[1] - initial[1])
    if x in (1, 2) and y in (1, 2) and x != y:
        return True
    window["out"].update("Your Knight can't move in that direction.")
    return False


def get_piece(black, white, position):
    """ Returns the piece which is at the given position.

    Parameters
    ----------
    black : list[pieces.Piece]
        The list of current Black pieces.
    white : list[pieces.Piece]
        The list of current White pieces.
    position : tuple[int, int]
        The position which is being checked for a piece.

    Returns
    -------
    pieces.Piece
        The piece which is at the given position. None if there is no piece.
    """
    for piece in black:
        if piece.get_position() == position:
            return piece
    for piece in white:
        if piece.get_position() == position:
            return piece
    return None
