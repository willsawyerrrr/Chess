import PySimpleGUI as sg
from pieces import *
import other


sg.theme("DarkGrey11")
other.welcome()

chessboard = [
    [sg.Button("New Game", key="new_game", size=(15, 1)),
     sg.Text(key="turn", size=(15, 1), justification="center"),
     sg.Text(key="out", size=(50, 1), justification="center")]]\
        + [
    [other.LightCell((row, column)) if (row + column) % 2 == 0
    else other.DarkCell((row, column)) for column in range(8)]
    for row in range(8)]

game_window = sg.Window("Chess", chessboard, finalize=True, size=(716, 700),
                        location=(0, 0), icon=r".\icons\chess_board.ico")
black, white, initial, destination, winner, count, turns = other.new_game(
    game_window)

# Game loop.
while True:
    winner = other.check_endgame(black, white)
    if winner is not None:
        game_window["turn"].update("")
        game_window["out"].update(f"{winner} wins!")

    event, values = game_window.read()

    if event == sg.WIN_CLOSED:
        game_window.close()
        break
    elif event == "new_game":
        black, white, initial, destination, winner, count, turns = \
            other.new_game(game_window)
    else:  # A cell is clicked.
        if initial is None:  # The piece to move hasn't been chosen.
            piece = moves.get_piece(black, white, event)
            if piece is not None and piece.get_team() == turns[count % 2]:
                initial = event
        else:
            destination = event
            dest_piece = moves.get_piece(black, white, destination)
            if dest_piece is None:
                if piece.move(destination, black, white, game_window):
                    count, black, white = other.end_turn(count, game_window,
                                                         piece, black, white)
            else:
                if piece.attack(destination, black, white, game_window):
                    count, black, white = other.end_turn(count, game_window,
                                                         piece, black, white)
            initial, destination = None, None

game_window.close()
