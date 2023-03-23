"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_cnt = 0
    o_cnt = 0
    for row in board:
        for item in row:
            if item == X:
                x_cnt += 1
            elif item == O:
                o_cnt += 1
    if x_cnt == o_cnt:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return_set.add((i, j))
    return return_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if type(action) != tuple:
        raise Exception("Invalid move")
    elif len(action) != 2:
        raise Exception("Invalid move")
    board_copy = initial_state()
    for i in range(3):
        for j in range(3):
            board_copy[i][j] = board[i][j]
    current_player = player(board)
    i, j = action[0], action[1]
    board_copy[i][j] = current_player
    return board_copy
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check row
    for row in board:
        if row[0] == row[1] and row[0] == row[2] and row[0] != EMPTY:
            return row[0]
    
    # check col
    for col in range(3):
        if board[0][col] == board[1][col] and board[0][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    
    # check diagonal
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    
    # no winner
    return None
    

def isFull(board):
    """
    a helper function determins whether a board is empty
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or isFull(board):
        return True
    return False
            


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    if game_winner == O:
        return -1
    return 0


def minimax_score(board, action):
    """
    a helper function of minimax, to return a minimax score of a action
    """
    update_board = result(board, action)
    if terminal(update_board):
        return utility(update_board)
    update_actions = actions(update_board)
    update_player = player(update_board)
    score = []
    if update_player == X:
        for action in update_actions:
            score.append(minimax_score(update_board, action))
            return max(score)
    if update_player == O:
        for action in update_actions:
            score.append(minimax_score(update_board, action))
            return min(score)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    possible_actions = actions(board)
    current_player = player(board)
    action_score_pair = {}
    for action in possible_actions:
        action_score_pair.update({action: minimax_score(board, action)})
    if current_player == X:
        max_score = max(action_score_pair.values())
        for key in action_score_pair.keys():
            if action_score_pair[key] == max_score:
                return key
    if current_player == O:
        min_score = min(action_score_pair.values())
        for key in action_score_pair.keys():
            if action_score_pair[key] == min_score:
                return key


def main():
    """
    this function is used to test the program
    """
    board1 = [
        [O, X, EMPTY],
        [EMPTY, O, X],
        [EMPTY, EMPTY, EMPTY] 
    ]
    minimax(board1)

if __name__ == "__main__":
    main()