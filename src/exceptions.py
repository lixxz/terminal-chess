class PieceAlreadyPresent(Exception):
    """
    When two pieces collide at the same position and the captured
    piece is not removed first.
    """
    def __init__(self, piece):
        self.piece = piece
        self.message = "Delete this piece before moving new one."

    def __str__(self):
        return "{piece} already present at {file}{rank}. {message}".format(piece=repr(self.piece), file=self.piece.file, rank=self.piece.rank, message=self.message)


class InvalidMove(Exception):
    pass
