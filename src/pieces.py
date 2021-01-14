from consts import WHITE, BLACK, RESET, RANKS, FILES


class Pawn:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1  # -1 -> 0 when pieces are initialized on the board by Board._put()
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'P' + RESET
        elif self.side == 'w':
            return WHITE + 'P' + RESET

    def __repr__(self):
        return "{} Pawn {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        pass

    def can_mate_king(self, king_pos, future_board_state):
        # TODO
        return False


class Rook:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'R' + RESET
        elif self.side == 'w':
            return WHITE + 'R' + RESET

    def __repr__(self):
        return "{} Rook {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        """
        Rook can move across file or rank. Can't jump over other pieces.
        Move is not legal if it leads to check.

        Returns
        -------
        list: str
            chess squares where piece can be legally moved
        """
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)
        moves = []

        # Increasing the rank
        for r in RANKS[rank_index + 1:]:
            chess_square = self.file + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)
                    # Can only move till capturing the opponent's piece.
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                # Can't jump over same side's piece.
                break
            else:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the rank. Order is crucial, so reversing.
        for r in RANKS[:rank_index][::-1]:
            chess_square = self.file + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)

        # Increasing the file
        for f in FILES[file_index + 1:]:
            chess_square = f + self.rank
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the file
        for f in FILES[:file_index][::-1]:
            chess_square = f + self.rank
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)

        return moves

    def can_mate_king(self, king_pos, future_board_state):
        """
        Checks whether any possible moves by the piece results in king's capture.
        Used to simulate future board states and helpful in determining the legal moves.
        """
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)

        for r in RANKS[rank_index + 1:]:
            chess_square = self.file + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                # Can't jump over pieces on the same side
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    # Can capture an enemy piece but it is not the king.
                    break
            else:
                # Continue loop till a piece is encountered
                continue

        for r in RANKS[:rank_index][::-1]:
            chess_square = self.file + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        for f in FILES[file_index + 1:]:
            chess_square = f + self.rank
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        for f in FILES[:file_index][::-1]:
            chess_square = f + self.rank
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        return False


class Bishop:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'B' + RESET
        elif self.side == 'w':
            return WHITE + 'B' + RESET

    def __repr__(self):
        return "{} Bishop {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        """
        Bishop can move diagonally in four directions. Can't jump over other pieces.
        Move is not legal if it leads to check.

        Returns
        -------
        list: str
            chess squares where piece can be legally moved
        """
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)
        moves = []

        # Increasing the rank and file
        for r, f in zip(RANKS[rank_index + 1:], FILES[file_index + 1:]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    # Can only move till capturing the opponent's piece.
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                # Can't jump over same side's piece.
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the rank and file. Order is crucial, so reversing.
        for r, f in zip(RANKS[:rank_index][::-1], FILES[:file_index][::-1]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Increasing the file and decreasing the rank
        for r, f in zip(RANKS[:rank_index][::-1], FILES[file_index + 1:]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the file and increasing the rank
        for r, f in zip(RANKS[rank_index + 1:], FILES[:file_index][::-1]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        return moves

    def can_mate_king(self, king_pos, future_board_state):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)

        # Increasing the rank and file
        for r, f in zip(RANKS[rank_index + 1:], FILES[file_index + 1:]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Decrease the rank and file
        for r, f in zip(RANKS[:rank_index][::-1], FILES[:file_index][::-1]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Increase the rank and decrease the file
        for r, f in zip(RANKS[rank_index + 1:], FILES[:file_index][::-1]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Increasing the file and decreasing the rank
        for r, f in zip(RANKS[:rank_index][::-1], FILES[file_index + 1:]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        return False


class Knight:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'N' + RESET
        elif self.side == 'w':
            return WHITE + 'N' + RESET

    def __repr__(self):
        return "{} Knight {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)
        moves = []

        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]

        for d in directions:
            if 0 <= file_index + d[0] < len(FILES) and 0 <= rank_index + d[1] < len(RANKS):
                chess_square = FILES[file_index + d[0]] + RANKS[rank_index + d[1]]
                if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                    if self.board.leads_to_check(self, chess_square[0], chess_square[1]):
                        continue
                    else:
                        moves.append(chess_square)
                elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                    continue
                else:
                    if self.board.leads_to_check(self, chess_square[0], chess_square[1]):
                        continue
                    else:
                        moves.append(chess_square)

        return moves

    def can_mate_king(self, king_pos, future_board_state):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)

        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]

        for d in directions:
            if 0 <= file_index + d[0] < len(FILES) and 0 <= rank_index + d[1] < len(RANKS):
                chess_square = FILES[file_index + d[0]] + RANKS[rank_index + d[1]]
                if future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side and chess_square == king_pos:
                    return True
        return False


class Queen:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'Q' + RESET
        elif self.side == 'w':
            return WHITE + 'Q' + RESET

    def __repr__(self):
        return "{} Queen {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)
        moves = []

        # Increasing the rank
        for r in RANKS[rank_index + 1:]:
            chess_square = self.file + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)
                    # Can only move till capturing the opponent's piece.
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                # Can't jump over same side's piece.
                break
            else:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the rank. Order is crucial, so reversing.
        for r in RANKS[:rank_index][::-1]:
            chess_square = self.file + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, self.file, r):
                    continue
                else:
                    moves.append(chess_square)

        # Increasing the file
        for f in FILES[file_index + 1:]:
            chess_square = f + self.rank
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the file
        for f in FILES[:file_index][::-1]:
            chess_square = f + self.rank
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, self.rank):
                    continue
                else:
                    moves.append(chess_square)

        # Increasing the rank and file
        for r, f in zip(RANKS[rank_index + 1:], FILES[file_index + 1:]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    # Can only move till capturing the opponent's piece.
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                # Can't jump over same side's piece.
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the rank and file. Order is crucial, so reversing.
        for r, f in zip(RANKS[:rank_index][::-1], FILES[:file_index][::-1]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Increasing the file and decreasing the rank
        for r, f in zip(RANKS[:rank_index][::-1], FILES[file_index + 1:]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        # Decreasing the file and increasing the rank
        for r, f in zip(RANKS[rank_index + 1:], FILES[:file_index][::-1]):
            chess_square = f + r
            if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)
                    break
            elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                break
            else:
                if self.board.leads_to_check(self, f, r):
                    continue
                else:
                    moves.append(chess_square)

        return moves

    def can_mate_king(self, king_pos, future_board_state):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)

        for r in RANKS[rank_index + 1:]:
            chess_square = self.file + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                # Can't jump over pieces on the same side
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    # Can capture an enemy piece but it is not the king.
                    break
            else:
                # Continue loop till a piece is encountered
                continue

        for r in RANKS[:rank_index][::-1]:
            chess_square = self.file + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        for f in FILES[file_index + 1:]:
            chess_square = f + self.rank
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        for f in FILES[:file_index][::-1]:
            chess_square = f + self.rank
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Increasing the rank and file
        for r, f in zip(RANKS[rank_index + 1:], FILES[file_index + 1:]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Decrease the rank and file
        for r, f in zip(RANKS[:rank_index][::-1], FILES[:file_index][::-1]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Increase the rank and decrease the file
        for r, f in zip(RANKS[rank_index + 1:], FILES[:file_index][::-1]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        # Increasing the file and decreasing the rank
        for r, f in zip(RANKS[:rank_index][::-1], FILES[file_index + 1:]):
            chess_square = f + r
            if future_board_state[chess_square] is not None and future_board_state[chess_square].side == self.side:
                break
            elif future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side:
                if chess_square == king_pos:
                    return True
                else:
                    break
            else:
                continue

        return False


class King:
    def __init__(self, board, side, file, rank):
        self.board = board
        self.side = side
        self.file = file
        self.rank = rank
        self.num_moves = -1
        self.move_history = []

    def __str__(self):
        if self.side == 'b':
            return BLACK + 'K' + RESET
        elif self.side == 'w':
            return WHITE + 'K' + RESET

    def __repr__(self):
        return "{} King {}{}".format(self.side, self.file, self.rank)

    def all_legal_moves(self):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)
        moves = []

        for r in [-1, 0, 1]:
            for f in [-1, 0, 1]:
                if r == f == 0:
                    continue
                elif 0 <= rank_index + r < len(RANKS) and 0 <= file_index + f < len(FILES):
                    chess_square = FILES[file_index + f] + RANKS[rank_index + r]
                    if self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side != self.side:
                        if self.board.leads_to_check(self, chess_square[0], chess_square[1]):
                            continue
                        else:
                            moves.append(chess_square)
                    elif self.board.current_state['state'][chess_square] is not None and self.board.current_state['state'][chess_square].side == self.side:
                        continue
                    else:
                        if self.board.leads_to_check(self, chess_square[0], chess_square[1]):
                            continue
                        else:
                            moves.append(chess_square)
                else:
                    continue

        if self.num_moves == 0 and not self.board.leads_to_check(self, self.file, self.rank):
            # Queenside Castling
            queenside_rook = self.board.current_state['state']['a' + self.rank]
            if queenside_rook is not None and queenside_rook.__class__ == Rook and queenside_rook.num_moves == 0 and not any(self.board.current_state['state'][f + self.rank] for f in 'bcd'):
                # Square king move through are not under attack
                if not self.board.leads_to_check(self, 'd', self.rank) and not self.board.leads_to_check(self, 'c', self.rank):
                    print('queenside', self.side)
                    moves.append('c' + self.rank)

            # Kingside Castling
            kingside_rook = self.board.current_state['state']['h' + self.rank]
            if kingside_rook is not None and kingside_rook.__class__ == Rook and kingside_rook.num_moves == 0 and not any(self.board.current_state['state'][f + self.rank] for f in 'fg'):
                if not self.board.leads_to_check(self, 'f', self.rank) and not self.board.leads_to_check(self, 'g', self.rank):
                    print('kingside', self.side)
                    moves.append('g' + self.rank)

        return moves

    def can_mate_king(self, king_pos, future_board_state):
        rank_index = RANKS.index(self.rank)
        file_index = FILES.index(self.file)

        for r in [-1, 0, 1]:
            for f in [-1, 0, 1]:
                if r == f == 0:
                    continue
                elif 0 <= rank_index + r < len(RANKS) and 0 <= file_index + f < len(FILES):
                    chess_square = FILES[file_index + f] + RANKS[rank_index + r]
                    if future_board_state[chess_square] is not None and future_board_state[chess_square].side != self.side and chess_square == king_pos:
                        return True
        return False
