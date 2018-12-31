class TicTacToeBoard:
    """General board class. Extended by GlobalBoard and LocalBoard"""

    def __init__(self):
        # 3x3 grid of zeros. Will be set to 1 or 2 when the square is claimed
        self.board = [[0, 0, 0] for _ in range(3)]

    # does this board have tic tac toe
    def has_tic_tac_toe(self, player):
        """Checks all possible tic tac toes for the given player"""

        # Check for horizontal and vertical tic tac toe
        for x in range(3):
            # Horizontal tic tac toe
            if self.board[x][0] == player and \
                    self.board[x][0] == self.board[x][1] and self.board[x][0] == self.board[x][2]:
                return True
            # Vertical tic tac toe
            if self.board[0][x] == player and \
                    self.board[0][x] == self.board[1][x] and self.board[0][x] == self.board[2][x]:
                return True

        # Check for negative diagonal tic tac toe
        if self.board[0][0] == player and self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            return True

        # Check for positive diagonal tic tac toe
        if self.board[2][0] == player and self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2]:
            return True

        # If there is no tic tac toe
        return False

    def is_full(self):
        """Checks if every space on the board has been played (i.e. there is a draw)"""
        return not any(0 in self.board[row] for row in range(3))


"""******************************************************************************************************************"""


class GlobalBoard(TicTacToeBoard):
    def __init__(self):
        TicTacToeBoard.__init__(self)
        self.local_boards = [LocalBoard(i) for i in range(9)]  # 3x3 grid of local boards

    def print_board(self):
        """Prints the board in the command line"""
        print()
        print('-' * 35)
        print()

        # each loop prints a row of the local boards
        for x in range(3):
            print(self.local_boards[0].board[x], '\t', self.local_boards[1].board[x], '\t',
                  self.local_boards[2].board[x])
        print()
        for x in range(3):
            print(self.local_boards[3].board[x], '\t', self.local_boards[4].board[x], '\t',
                  self.local_boards[5].board[x])
        print()
        for x in range(3):
            print(self.local_boards[6].board[x], '\t', self.local_boards[7].board[x], '\t',
                  self.local_boards[8].board[x])

    def mark_global_board(self, local_board, player):
        """Records when a local board has been won"""
        row = local_board.index // 3
        col = local_board.index % 3
        self.board[row][col] = player


"""******************************************************************************************************************"""


class LocalBoard(TicTacToeBoard):
    def __init__(self, index):
        TicTacToeBoard.__init__(self)
        self.focus = True
        self.playable = True
        self.index = index  # The board's index in the local_boards list (from the GlobalBoard class)
