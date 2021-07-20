import moves


class Piece(object):
    def __init__(self, position, team):
        """ A Chess piece, defined by its type, position and team. """
        _paths = {
            "Black Pawn": r".\icons\bp.png",
            "Black Rook": r".\icons\br.png",
            "Black Knight": r".\icons\bn.png",
            "Black Bishop": r".\icons\bb.png",
            "Black King": r".\icons\bk.png",
            "Black Queen": r".\icons\bq.png",
            "White Pawn": r".\icons\wp.png",
            "White Rook": r".\icons\wr.png",
            "White Knight": r".\icons\wn.png",
            "White Bishop": r".\icons\wb.png",
            "White King": r".\icons\wk.png",
            "White Queen": r".\icons\wq.png"
        }
        self._pos = position
        self._team = team
        self._icon_path = _paths[repr(self)]
        self._initial = True

    def __repr__(self):
        return f"{self._team} {self._type}"

    def move(self, destination, black, white, window):
        """ Controls the piece's move.

        Parameters
        ----------
        destination : tuple[int, int]
            The cell to which the piece is attempting to move.
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.
        window : sg.Window
            The Chess game Window.

        Returns
        -------
        bool
            True if the piece's move is valid. False otherwise.
        """
        position = self.get_position()
        direction = moves.get_direction(position, destination)
        if not direction:
            return False
        if not moves.validate_move(self, direction, window):
            return False
        if not moves.validate_path(self, black, white, position, destination,
                             direction, window):
            return False
        self.update_position(window, destination)
        self._pos = destination
        self._initial = False
        return True

    def attack(self, destination, black, white, window):
        """ Controls the piece's attack.

        Parameters
        ----------
        destination : tuple[int, int]
            The cell at which the piece is attempting to attack another piece.
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.
        window : sg.Window
            The Chess game Window.

        Returns
        -------
        bool
            True if the piece's attack is valid. False otherwise.
        """
        position = self.get_position()
        direction = moves.get_direction(position, destination)
        if not direction:
            return False
        if not moves.validate_attack(self, direction, window):
            return False
        if not moves.validate_position(self, black, white, destination, window):
            return False
        if not moves.validate_path(self, black, white, position, destination,
                             direction, window):
            return False
        self.update_position(window, destination)
        self._pos = destination
        self._initial = False
        return True

    def kill(self, black, white):
        """ Removes the piece from the list of its team's current pieces.

        Parameters
        ----------
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.

        Returns
        -------
        tuple[list[Piece], list[Piece]]
            list[Piece] : The list of current Black pieces.
            list[Piece] : The list of current White pieces.
        """
        if self.get_team() == "Black":
            black.remove(self)
        elif self.get_team() == "White":
            white.remove(self)
        return black, white

    def update_position(self, window, destination):
        """ Updates position of a piece's icon.

        Parameters
        ----------
        window : sg.Window
            The Chess game window.
        destination : tuple[int, int]
            The cell to which the piece is moving.
        """
        window[self.get_position()].update(image_filename="",
                                           image_size=(75, 75))
        window[destination].update(image_filename=self.get_icon_path(),
                                   image_size=(75, 75))

    def promote(self, piece_type, black, white, window):
        return

    def get_position(self):
        """ Returns the piece's position as a tuple[row, column]. """
        return self._pos

    def get_type(self):
        """ Returns the piece's type as a string. """
        return self._type

    def get_team(self):
        """ Returns the piece's team as a string. """
        return self._team

    def get_move(self):
        """ Returns the list of directions in which the piece can move. """
        return self._move_directions

    def get_attack(self):
        """ Returns the list of directions in which the piece can attack. """
        return self._attack_directions

    def get_icon_path(self):
        """ Returns the piece's icon path as a string."""
        return self._icon_path

    def get_initial(self):
        """ Returns whether or not the piece is at its initial position. """
        return self._initial

    def get_far(self):
        """ Returns the row which is the far side of the Chessboard. """
        _far_rows = {"Black": 7, "White": 0}
        return _far_rows[self.get_team()]


class Pawn(Piece):
    _type = "Pawn"

    def promote(self, piece_type, black, white, window):
        """ Promotes a Pawn to another piece when it reaches the far side of
        the Chessboard.

        Parameters
        ----------
        piece_type : str
            The type of piece which the Pawn is being promoted to.
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.
        window : sg.Window
            The Chess game window.

        Returns
        -------
        tuple[Piece, list[Piece], list[Piece]]
            Piece : The promoted piece.
            list[Piece] : The list of current Black pieces.
            list[Piece] : The list of current White pieces.
        """
        team = self.get_team()
        position = self.get_position()
        pieces = {
            "Rook": Rook(position, team),
            "Knight": Knight(position, team),
            "Bishop": Bishop(position, team),
            "Queen": Queen(position, team)
        }
        if team == "Black":
            black.remove(self)
            black.append(pieces[piece_type])
            black[-1].update_position(window, position)
        else:
            white.remove(self)
            white.append(pieces[piece_type])
            white[-1].update_position(window, position)
        return black, white

    def get_move(self):
        """ Returns the list of directions in which the piece can move. """
        _move_directions = {"Black": ["down"], "White": ["up"]}
        return _move_directions[self.get_team()]

    def get_attack(self):
        """ Returns the list of directions in which the piece can attack. """
        _attack_directions = {"Black": ["bottom-left", "bottom-right"],
                              "White": ["top-left", "top-right"]}
        return _attack_directions[self.get_team()]


class Rook(Piece):
    _type = "Rook"
    _move_directions = [
        "left",
        "right",
        "up",
        "down"
    ]
    _attack_directions = [
        "left",
        "right",
        "up",
        "down"
    ]


class Knight(Piece):
    _type = "Knight"

    def move(self, destination, black, white, window):
        """ Controls the piece's move.

        Parameters
        ----------
        destination : tuple[int, int]
            The cell to which the piece is attempting to move.
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.
        window : sg.Window
            The Chess game Window.

        Returns
        -------
        bool
            True if the piece's move is valid. False otherwise.
        """
        position = self.get_position()
        if moves.knight(position, destination, window):
            self.update_position(window, destination)
            self._pos = destination
            return True
        return False

    def attack(self, destination, black, white, window):
        """ Controls the piece's attack.

        Parameters
        ----------
        destination : tuple[int, int]
            The cell at which a piece is attempting to attack another piece.
        black : list[Piece]
            The list of current Black pieces.
        white : list[Piece]
            The list of current White pieces.
        window : sg.Window
            The Chess game Window.

        Returns
        -------
        bool
            True if the piece's attack is valid. False otherwise.
        """
        position = self.get_position()
        dest_piece = moves.get_piece(black, white, destination)
        if dest_piece.get_team() != self.get_team():
            if moves.knight(position, destination, window):
                self.update_position(window, destination)
                self._pos = destination
                return True
        return False


class Bishop(Piece):
    _type = "Bishop"
    _move_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right"
    ]
    _attack_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right"
    ]


class Queen(Piece):
    _type = "Queen"
    _move_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "left",
        "right",
        "up",
        "down"
    ]
    _attack_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "left",
        "right",
        "up",
        "down"
    ]


class King(Piece):
    _type = "King"
    _move_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "left",
        "right",
        "up",
        "down"
    ]
    _attack_directions = [
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "left",
        "right",
        "up",
        "down"
    ]
