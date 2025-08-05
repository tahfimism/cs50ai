"""
Tic Tac Toe Player
"""

import math
import copy

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
    # check the number of non-empty cell:
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O





def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i, j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    if not (0 <= row <= 2 and 0 <= col <= 2):
        raise ValueError("Action is out of bounds.")

    if board[row][col] is not EMPTY:
        raise ValueError("Invalid action, cell already taken.")

    new_board = copy.deepcopy(board)
    new_board[row][col] = player(board)
    return new_board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    
    if ((board[0][0] == board[0][1] == board[0][2] == "X") or
    (board[1][0] == board[1][1] == board[1][2] == "X") or
    (board[2][0] == board[2][1] == board[2][2] == "X") or
    (board[0][0] == board[1][0] == board[2][0] == "X") or
    (board[0][1] == board[1][1] == board[2][1] == "X") or
    (board[0][2] == board[1][2] == board[2][2] == "X") or
    (board[0][0] == board[1][1] == board[2][2] == "X") or
    (board[0][2] == board[1][1] == board[2][0] == "X")):
        return X

    if ((board[0][0] == board[0][1] == board[0][2] == "O") or
    (board[1][0] == board[1][1] == board[1][2] == "O") or
    (board[2][0] == board[2][1] == board[2][2] == "O") or
    (board[0][0] == board[1][0] == board[2][0] == "O") or
    (board[0][1] == board[1][1] == board[2][1] == "O") or
    (board[0][2] == board[1][2] == board[2][2] == "O") or
    (board[0][0] == board[1][1] == board[2][2] == "O") or
    (board[0][2] == board[1][1] == board[2][0] == "O")):
        return O
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) is not None:
        return True
      

    # check if there is any empty cell
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # if current board is terminal
    if terminal(board):
        return None

    playing = player(board)
    if playing == X:
        v = -math.inf
        for action in actions(board): # simulating O's turn, so min_value
            value = min_value(result(board, action))
            if value > v:
                v = value
                best_action = action
    else: # player is O
        v = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < v:
                v = value
                best_action = action
    return best_action
    

