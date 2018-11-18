class TicTacToeBoard:
    def __init__(self):
        self.board = [[0, 0, 0] for _ in range(3)]

    def has_tic_tac_toe(self):
        # Check for horizontal and vertical tic tac toe
        for x in range(3):
            # Horizontal tic tac toe
            if self.board[x][0] > 0 and self.board[x][0] == self.board[x][1] and self.board[x][0] == self.board[x][2]:
                return True
            # Vertical tic tac toe
            if self.board[0][x] > 0 and self.board[0][x] == self.board[1][x] and self.board[0][x] == self.board[2][x]:
                return True

        # Check for negative diagonal tic tac toe
        if self.board[0][0] > 0 and self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            return True

        # Check for positive diagonal tic tac toe
        if self.board[2][0] > 0 and self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2]:
            return True

        # If there is no tic tac toe
        return False

    def is_full(self):
        for row in range(3):
            if 0 in self.board[row]:
                return False
        return True


class GlobalBoard(TicTacToeBoard):
    def __init__(self):
        TicTacToeBoard.__init__(self)
        self.local_boards = [LocalBoard() for _ in range(9)]

    def print_board(self):
        print()
        print('-' * 35)
        print()
        for x in range(3):
            print(self.local_boards[0].board[x], '\t', self.local_boards[1].board[x], '\t', self.local_boards[2].board[x])
        print()
        for x in range(3):
            print(self.local_boards[3].board[x], '\t', self.local_boards[4].board[x], '\t', self.local_boards[5].board[x])
        print()
        for x in range(3):
            print(self.local_boards[6].board[x], '\t', self.local_boards[7].board[x], '\t', self.local_boards[8].board[x])

    def mark_board(self, lb_index, player: int):
        if lb_index < 3:
            row = 0
        elif lb_index < 6:
            row = 1
        else:
            row = 2
        col = lb_index % 3
        self.board[row][col] = player


class LocalBoard(TicTacToeBoard):
    def __init__(self):
        TicTacToeBoard.__init__(self)
        self.focus = True
        self.playable = True
