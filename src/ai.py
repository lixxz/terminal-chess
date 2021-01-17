import random


class AI:
    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty
        pass

    def get_best_move(self):
        pass

    def get_random_move(self):
        avail_moves = self.board.all_legal_moves()
        source = random.choice(list(avail_moves.keys()))
        dest = random.choice(avail_moves[source])
        return "{} {}".format(source.split(' ')[-1], dest)
