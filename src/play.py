import argparse
from board import Board
from consts import WHITE, BLACK, RESET
from ai import AI


def ask_player_side():
    while True:
        side = str(input("Please select your side. " + WHITE + "w" + RESET + " for white and " + BLACK + 'b' + RESET + " for black: "))
        if side == 'w' or side == 'b':
            break
        else:
            print("\nPlease enter valid input\n")
    return side


def greeting():
    print("Welcome to Terminal Chess!\n\n")


def ask_difficulty():
    while True:
        difficulty = input("\nComputer AI level. 'r' for regular, 'm' for medium and 'h' for hard: ")
        if difficulty == 'r' or difficulty == 'm' or difficulty == 'h':
            break
        else:
            print("\nPlease enter valid input\n")
            continue
    return difficulty


def show_help():
    print("q - quit")
    print("r - play random move")
    print("u - undo your last move")
    print("s - show all legal moves")


def main():
    greeting()
    side = ask_player_side()
    difficulty = ask_difficulty()

    b = Board()
    ai = AI(b, difficulty)

    while True:
        b.draw()

        if b.current_state['player'] == str(side):
            # Player's turn
            move = input("\nYour Move(? for help): ")
            if move == '?':
                show_help()
            else:
                b.input(move)
            pass
        else:
            # AI's turn
            b.input(ai.get_random_move())
            pass
        break


if __name__ == "__main__":
    main()
