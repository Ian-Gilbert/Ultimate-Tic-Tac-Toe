from copy import deepcopy
import math
from threading import Thread
from time import time
from random import choice


class Tree:
    def __init__(self, root):
        self.current_root = root

    def get_next_root(self, global_board):
        for child in self.current_root.children:
            if child.is_equal(global_board):
                self.current_root = child
                return


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.plays = 0
        self.reward = 0

        self.action = action
        self.parent = parent
        self.children = []

    def birth_children(self):
        for action in self.state.get_possible_moves():
            new_state = self.state.get_next_state(action)
            # new_state.global_board.print_board()
            self.children.append(Node(new_state, self, action))

    def get_favorite_child(self):  # lol
        ucb1_list = []
        for child in self.children:
            avg_reward = child.reward / child.plays
            ucb1 = avg_reward + math.sqrt((2 * math.log(self.plays)) / child.plays)
            ucb1_list.append(ucb1)
        return self.children[ucb1_list.index(max(ucb1_list))]


class UTTTState:
    def __init__(self, global_board, player):
        self.global_board = global_board
        self.player = player

    def is_equal(self, gb):
        if self.global_board.board == gb.board:
            if all(self.global_board.local_board_list[i].board == gb.local_board_list[i].board for i in range(9)):
                return True
        return False

    def get_possible_moves(self):
        moves = []
        for local_board in self.global_board.local_board_list:
            if local_board.focus:
                for row_index, row in enumerate(local_board.board):
                    for col_index, cell in enumerate(row):
                        if cell == 0:
                            move = (local_board, row_index, col_index)
                            moves.append(move)
        return moves

    def get_next_state(self, move):
        state = deepcopy(self)
        local_board = state.global_board.local_board_list[move[0].index]
        local_board.board[move[1]][move[2]] = state.player

        if local_board.has_tic_tac_toe(state.player):
            local_board.playable = False
            state.global_board.mark_global_board(local_board, state.player)
        elif local_board.is_full():
            local_board.playable = False
            state.global_board.mark_global_board(local_board, -1)

        state.global_board.update_focus(move[1], move[2])
        state.player = (state.player % 2) + 1
        return state

    def is_terminal(self):
        if self.global_board.has_tic_tac_toe(self.player) or self.global_board.has_tic_tac_toe(
                (self.player % 2) + 1) or self.global_board.is_full():
            return True
        return False

    def get_reward(self):
        if self.global_board.has_tic_tac_toe(self.player):
            return 1
        elif self.global_board.has_tic_tac_toe((self.player % 2) + 1):
            return -1
        elif self.global_board.is_full():
            return 0

    def get_winner(self):
        player = self.player
        opponent = (self.player % 2) + 1
        if self.global_board.has_tic_tac_toe(player):
            return player
        elif self.global_board.has_tic_tac_toe(opponent):
            return opponent
        else:
            return None


class MCTS(Thread):
    def __init__(self, global_board, player, time_limit):
        Thread.__init__(self, target=self.search)
        self.root = Node(UTTTState(global_board, player), None, None)
        self.current_node = self.root
        self.time_limit = time_limit

        self.local_board = None
        self.row = None
        self.col = None

    def search(self):
        # count = 0
        # start_time = time()
        self.time_limit = time() + self.time_limit
        while time() < self.time_limit or any(child.plays == 0 for child in self.root.children):
            # count += 1
            self.playout()
        # print(f'Actual search time: {time() - start_time} seconds')
        # print(f'Playouts: {count}\n')
        favorite_child = self.root.get_favorite_child()
        self.local_board, self.row, self.col = favorite_child.action

    def playout(self):
        while True:
            if self.current_node.state.is_terminal():
                self.backpropogate(self.current_node, self.current_node.state.get_reward())
                return
            else:
                if len(self.current_node.children) == 0:
                    self.current_node.birth_children()

                if any(child.plays == 0 for child in self.current_node.children):
                    useless_children = []
                    for child in self.current_node.children:
                        if child.plays == 0:
                            useless_children.append(child)
                    self.current_node = choice(useless_children)
                else:
                    self.current_node = self.current_node.get_favorite_child()

    def backpropogate(self, node, reward):
        while node is not None:
            node.plays += 1
            node.reward += reward
            # if winner is not None:
            #     if node.state.player == winner:
            #         node.reward += 1
            #     else:
            #         node.reward -= 1
            node = node.parent
        self.current_node = self.root

    def get_next_move(self, global_board):
        local_board = global_board.local_board_list[self.local_board.index]
        return local_board, self.row, self.col
