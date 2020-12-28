from consts import (
    SPACE_AND_UNDERSCORE, PIPE_AND_SPACE, PIPE_AND_UNDERSCORE,
    SIDES, FILES, RANKS, SQUARE_TO_CORD_MAPPING, FILES_DRAW, PIPE_AND_SPACE_8,
    PIPE_AND_SPACE_7, PIPE_AND_SPACE_6, PIPE_AND_SPACE_5, PIPE_AND_SPACE_4,
    PIPE_AND_SPACE_3, PIPE_AND_SPACE_2, PIPE_AND_SPACE_1
)
from pieces import Rook, Queen, King, Knight, Pawn, Bishop
from exceptions import PieceAlreadyPresent
from copy import deepcopy


class Board:
    def __init__(self):
        self._grid = [SPACE_AND_UNDERSCORE[:], PIPE_AND_SPACE[:], PIPE_AND_SPACE_8[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_7[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_6[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_5[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_4[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_3[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_2[:], PIPE_AND_UNDERSCORE[:],
                      PIPE_AND_SPACE[:], PIPE_AND_SPACE_1[:], PIPE_AND_UNDERSCORE[:], FILES_DRAW[:]]
        self.current_state = {'player': SIDES[0], 'move': None, 'state': {f + r: None for f in FILES for r in RANKS}}
        self.history = []
        self.num_moves = 0

        self._put(Rook(self, SIDES[0], 'a', '1'), 'a', '1')
        self._put(Rook(self, SIDES[0], 'h', '1'), 'h', '1')
        self._put(Knight(self, SIDES[0], 'b', '1'), 'b', '1')
        self._put(Knight(self, SIDES[0], 'g', '1'), 'g', '1')
        self._put(Bishop(self, SIDES[0], 'c', '1'), 'c', '1')
        self._put(Bishop(self, SIDES[0], 'f', '1'), 'f', '1')
        self._put(Queen(self, SIDES[0], 'd', '1'), 'd', '1')
        self._put(King(self, SIDES[0], 'e', '1'), 'e', '1')

        for f in FILES:
            self._put(Pawn(self, SIDES[0], f, '2'), f, '2')

        self._put(Rook(self, SIDES[1], 'a', '8'), 'a', '8')
        self._put(Rook(self, SIDES[1], 'h', '8'), 'h', '8')
        self._put(Knight(self, SIDES[1], 'b', '8'), 'b', '8')
        self._put(Knight(self, SIDES[1], 'g', '8'), 'g', '8')
        self._put(Bishop(self, SIDES[1], 'c', '8'), 'c', '8')
        self._put(Bishop(self, SIDES[1], 'f', '8'), 'f', '8')
        self._put(Queen(self, SIDES[1], 'd', '8'), 'd', '8')
        self._put(King(self, SIDES[1], 'e', '8'), 'e', '8')

        for f in FILES:
            self._put(Pawn(self, SIDES[1], f, '7'), f, '7')

    def draw(self):
        for g in self._grid:
            print("".join(g))

    def undo_last_move(self):
        pass

    def input(self, move_string):
        """
        Parses move_string according to Standard Algebraic Notation.
        """
        pass

    def _put(self, piece, file, rank):
        """
        Underlying API for moving pieces on the board. Hides the hardcoded mapping
        between chess squares and actual grid coordinates.

        Parameters
        ----------
        piece: object
            Knight, Bishop, King, Pawn, Queen, Rook.
        file: str
            file at which piece is to be placed.
        rank: str
            rank at which piece is to be placed.

        Raises
        ------
        PieceAlreadyPresent
            If two pieces collide at the same position. Captured piece has to be
            deleted before new piece is moved in its place.
        """
        chess_square = str(file) + str(rank)
        self._grid[SQUARE_TO_CORD_MAPPING[chess_square][0]][SQUARE_TO_CORD_MAPPING[chess_square][1]] = str(piece)

        if self.current_state['state'][chess_square] is None:
            self.current_state['state'][chess_square] = piece
            piece.file = file
            piece.rank = rank
            piece.num_moves += 1
        else:
            raise PieceAlreadyPresent(self.current_state['state'][chess_square])
        return

    def _delete(self, file, rank):
        """
        When a piece is captured, this function is called to remove it.
        Called before _put().
        """
        chess_square = str(file) + str(rank)
        self._grid[SQUARE_TO_CORD_MAPPING[chess_square][0]][SQUARE_TO_CORD_MAPPING[chess_square][1]] = ' '
        self.current_state['state'][chess_square] = None

    def leads_to_check(self, piece, file, rank):
        """
        Checks whether putting the piece at <file><rank> will
        lead to check of their own king.
        Used by a piece to determine the legality of a move.

        Returns
        --------
        bool
            True if current side's king is in check, False otherwise.
        """
        state = deepcopy(self.current_state)

        # Puttin piece(its copy) at the proposed position
        temp = state['state'][piece.file + piece.rank]
        state['state'][piece.file + piece.rank] = None
        state['state'][file + rank] = temp

        # Updating the piece copy as well
        state['state'][file + rank].file = file
        state['state'][file + rank].rank = rank

        # Search the state dictionary for king
        king = next(k for k in state['state'].values() if k.__class__ == King and k.side == piece.side)

        # Checking if an enemy piece can directly capture the king
        for p in state['state'].values():
            if p is not None and p.side != piece.side and p.can_mate_king(king.file + king.rank, state['state']):
                return True

        return False

    def is_square_under_attack(self, file, rank):
        """
        Checks whether the specified square(<file><rank>) is under attack by any
        of enemy pieces.

        Returns
        --------
        bool
            True if square is under attack, False otherwise
        """
        if file + rank in self.all_legal_moves().values():
            return True

        return False

    def all_legal_moves(self):
        """
        Find all legal moves for the given state. Game ends when there are no
        legal moves available for the player.

        Parameters
        ----------
        state: dict
            Pass a future board state to see if a move is viable or not. Default
            is to check the current state.

        Returns
        -------
        dict
            Piece: [List of Moves]
        """
        moves = {}

        for m in self.current_state['state'].values():
            if m is not None and m.side == self.current_state['player']:
                moves[repr(m)[2:]] = m.all_legal_moves()

        return moves
