""" Path taken by a piece from its original position to its destination. """


class Path(object):
    def __init__(self, initial, destination, direction):
        changes = {
            "down": (0, 1),
            "left": (-1, 0),
            "up": (0, -1),
            "right": (1, 0),
            "bottom-left": (-1, 1),
            "top-left": (-1, -1),
            "top-right": (1, -1),
            "bottom-right": (1, 1)
        }
        self._cells = []
        self._valid = True
        position = initial
        x, y = changes[direction]
        count = 0
        position = (position[0] + y, position[1] + x)
        while position != destination:
            self._cells.append(position)
            position = (position[0] + y, position[1] + x)
            count += 1
            if count > 8:
                self._valid = False
                break

    def get_cells(self):
        return self._cells

    def is_valid(self):
        return self._valid
