from typing import List


class TicTacToeBoard:
    """General board class. Extended by GlobalBoard and LocalBoard"""

    def __init__(self) -> None:
        # 3x3 grid of zeros. Will be set to 1 or 2 when the square is claimed
        self.board: List[List[int]] = [[0, 0, 0] for _ in range(3)]

    # does this board have tic tac toe
    def has_tic_tac_toe(self, player: int) -> bool:
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

    def is_full(self) -> bool:
        """Checks if every space on the board has been played (i.e. there is a draw)"""
        return not any(0 in self.board[row] for row in range(3))


"""******************************************************************************************************************"""


class LocalBoard(TicTacToeBoard):
    def __init__(self, index: int) -> None:
        TicTacToeBoard.__init__(self)
        self.focus: bool = True
        self.playable: bool = True
        self.index: int = index  # The board's index in the local_board_list (from the GlobalBoard class)


"""******************************************************************************************************************"""


class GlobalBoard(TicTacToeBoard):
    def __init__(self) -> None:
        TicTacToeBoard.__init__(self)
        self.local_board_list: List[LocalBoard] = [LocalBoard(i) for i in range(9)]  # 3x3 grid of local boards

    def print_board(self) -> None:
        """Prints the board in the command line"""
        print()
        print('-' * 35)
        print()

        # each loop prints a row of the local boards
        for x in range(3):
            print(self.local_board_list[0].board[x], '\t', self.local_board_list[1].board[x], '\t',
                  self.local_board_list[2].board[x])
        print()
        for x in range(3):
            print(self.local_board_list[3].board[x], '\t', self.local_board_list[4].board[x], '\t',
                  self.local_board_list[5].board[x])
        print()
        for x in range(3):
            print(self.local_board_list[6].board[x], '\t', self.local_board_list[7].board[x], '\t',
                  self.local_board_list[8].board[x])

    def mark_global_board(self, local_board: LocalBoard, player: int) -> None:
        """Records when a local board has been won"""
        row = local_board.index // 3
        col = local_board.index % 3
        self.board[row][col] = player

    def update_focus(self, old_row: int, old_col: int) -> None:
        """Use the previous move to set the focus of the local boards for the next turn"""

        # Local board in the same position as the previous guess. May or may not be playable
        next_lb = self.local_board_list[old_row * 3 + old_col]

        # if the board is playable, set focus to True, and all others to False
        if next_lb.playable:
            for local_board in self.local_board_list:
                local_board.focus = False
            next_lb.focus = True
        # if the board is not playable, set all playable boards in focus, and all non-playable boards out of focus
        else:
            for local_board in self.local_board_list:
                local_board.focus = local_board.playable
