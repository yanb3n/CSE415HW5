'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import time

global output
WHITE = 1
BLACK = 0
PAWN = 0
LONG_LEAPER = 1
IMITATOR = 2
WITHDRAWER = 3
KING = 4
COORDINATOR = 5
FREEZER = 6
pieces = [['p','l','i','w','k','c','f'],['P','L','I','W','K','C','F']]  # pieces, use pieces[color][piece] to check

# for chess board notation

'''
a = 0
b = 1
c = 2
d = 3 
e = 4
f = 5
g = 6
h = 7
'''

operators = {'p':[(1,0),(0,1),(-1,0),(0,-1)],  # pawn
             'l':[(2,0),(0,2),(-2,0),(0,-2)],  # long leaper
             'i':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1),(2,0),(0,2),(-2,0),
                  (0,-2)],  # imitator
             'w':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # withdrawer (queen)
             'k':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # king
             'c':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # coordinator
             'f':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]}  # freezer


def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    if alphaBeta:
        bestMove = alphabeta_pruning(ply, currentState, float('-inf'), float('inf'))[1][1]
    else:
        bestMove = minimax(ply, currentState)[1]
    if useBasicStaticEval:
        output['CURRENT_STATE_STATIC_EVAL'] = basicStaticEval(bestMove)  # implement minimax algorithm
    elif alphaBeta:
        pass  # temporary
    elif useZobristHashing:
        pass  # temporary
    output['N_STATES_EXPANDED'] = 0  # get states from minimax algorithm
    output['N_STATIC_EVALS'] = 0
    output['N_CUTOFFS'] = 0
    return output


def next_to_freezer(board_list, row, col):
    for op in [(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]:
        if ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
           and (col + op[1] < 8)):
            print(board_list[row + op[0]][col + op[1]].isupper())
            print(board_list[row][col].isupper())
            print(board_list[row + op[0]][col + op[1]].isupper() != board_list[row][col].isupper())
            print((board_list[row + op[0]][col + op[1]].lower()))
            print((board_list[row + op[0]][col + op[1]].lower()) != 'f')
            if (board_list[row + op[0]][col + op[1]].isupper() != board_list[row][col].isupper() and
                    board_list[row + op[0]][col + op[1]].lower() != 'f'):
                return True
    return False

def generate_moves(currentState):
    board_list = currentState.board  # list of current board positions in row-major order
    whose_move = currentState.whose_move
    possible_moves = []
    king_position = [[0 for x in range(2)] for x in range(2)]
    king_position[WHITE] = [-1, -1]
    king_position[BLACK] = [-1, -1]
    for row in range(8):
        for col in range(8):
            row_temp = row
            col_temp = col
            #starting_square = index_to_notation(row_temp, col_temp)
            piece = board_list[row][col]
            if (piece.lower() is 'k'
                and piece in pieces[whose_move]
                and not next_to_freezer(board_list, row_temp, col_temp)):
                current_ops = operators['k']
                king_position[whose_move] = [row, col]
                for king_op in current_ops:
                    row_temp += king_op[0]
                    col_temp += king_op[1]
                    if king_case(row, col, king_op, board_list):
                        new_board_state = board_list.copy()
                        new_board_state[row_temp][col_temp] = new_board_state[row][col]
                        new_board_state[row][col] = '-'
                        possible_moves.append([[((row, col),(row + king_op[0], col + king_op[1])),
                                                BC.BC_state(new_board_state, 1 - whose_move)],"lmao"])
            elif (board_list[row][col] is not '-'
                and piece.lower() != 'k' 
                and piece in pieces[whose_move] 
                and not next_to_freezer(board_list, row_temp, col_temp)):
                current_ops = operators[board_list[row][col].lower()]
                for op in current_ops:
                    while can_move(row_temp, col_temp, op, board_list):
                        row_temp += op[0]
                        col_temp += op[1]
                        #ending_square = index_to_notation(row_temp, col_temp)
                        new_board_state = board_list.copy()
                        new_board_state[row_temp][col_temp] = new_board_state[row][col]
                        new_board_state[row][col] = '-'
                        if piece.lower() == 'p':
                            for op_cap in current_ops:
                                if pincer_capturable(row, col, op_cap, new_board_state):
                                    new_board_state[row_temp + op_cap[0]][col_temp + op_cap[1]] = '-'
                        elif piece.lower() == 'l':
                            if long_leaper_capturable(row, col, op_cap, board_list):
                                new_board_state[row + op[0] / 2][col + op[1] / 2] = '-'
                        elif piece.lower() == 'w':
                            if withdrawer_capturable(row, col, op, board_list):
                                new_board_state[row - op[0]][col - op[1]] = '-'
                        elif piece.lower() == 'c':
                            capture = coordinator_capturable(row_temp, col_temp, new_board_state, king_position, whose_move)
                            for captured in capture:
                                new_board_state[captured[0]][captured[1]] = '-'
                        possible_moves.append([[((row, col),(row_temp, col_temp)),
                                                BC.BC_state(new_board_state, 1 - whose_move)],"lmao"])
    return possible_moves

# check if piece can perform legal move
def can_move(row, col, op, board_list):
    return ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
            and (col + op[1] < 8) and (board_list[row + op[0]][col + op[1]] == '-'))

# check if king can capture or move
def king_case(row, col, op, board_list):
    new_row = row + op[0]
    new_col = col + op[1]
    return ((new_row >= 0) and (new_row < 8) and (new_col >= 0) and (new_col < 8)
            and (board_list[new_row][new_col] == '-'
            or board_list[row][col].isupper() != board_list[new_row][new_col].isupper()))

# check if withdrawer capture
def withdrawer_capturable(row, col, op, board_list):
     return (board_list[row][col].isupper() != board_list[row - op[0]][col - op[1]].isupper())

# check if pincer move causes captures
def pincer_capturable(row, col, op, board_list):
    new_row = row + 2*op[0]
    new_col = col + 2*op[1]
    return ((new_row >= 0) and (new_row < 8) and (new_col >= 0)
            and (new_col < 8) and (board_list[new_row][new_col] != '-')
            and (board_list[row][col].isupper() == board_list[new_row][new_col].isupper())
            and board_list[row][col].isupper() != board_list[row + op[0]][col + op[1]].isupper())

# check if leaper move captures
def long_leaper_capturable(row, col, op, board_list):
    new_row = row + op[0] / 2
    new_col = col + op[1] / 2
    return (board_list[row][col].isupper() != board_list[new_row][new_col].isupper())

# Checks for whether there is a capturable piece by a move of the coordinator
# Returns the (rank, file) of a piece if capturable; if none, returns empty list
def coordinator_capturable(c_new_row, c_new_col, new_board_list, king_position, whose_move):
    capturable = []
    kings_row = 0
    kings_col = 0
    if king_position[whose_move] is [-1, -1]:
        for r in range(8):
            for c in range(8):
                if new_board_list[r][c] == pieces[whose_move][KING]:
                    kings_row = r
                    kings_col = c
    else:
        kings_row = king_position[0]
        kings_col = king_position[1]
    if (new_board_list[kings_row][c_new_col] != '-' 
       and new_board_list[kings_row][c_new_col].isupper() != new_board_list[c_new_row][c_new_col].isupper()):
        capturable.append([kings_row, c_new_col])
    if (new_board_list[c_new_row][kings_col] != '-'
       and new_board_list[c_new_col][kings_col].isupper() != new_board_list[c_new_row][c_new_col].isupper()):
        capturable.append([c_new_col, kings_col])
    return capturable


# # Returns a list of form [[old_spot, new_spot], newState]
# def minimax(ply, currentState):
#     if ply == 0:
#         return basicStaticEval(currentState)
#     newMoves = generate_moves(currentState)
#     if currentState.whose_move == WHITE:
#         best = float('-inf')
#         for move in range(len(newMoves)):
#             newValue = minimax(ply - 1, move[0][1])
#             if newValue >= best:
#                 best = newValue
#         return best
#     else:
#         best = float('inf')
#         for move in range(len(newMoves)):
#             newValue = minimax(ply - 1, move[0][1])
#             if newValue >= best:
#                 best = newValue
#         return best

# Returns a list of form [value, [[[old_spot, new_spot], newState], remark]]
# generate_moves: [[(old_spot, new_spot), newState, 1 - whose_move)], remark]
# Not sure if this works
def minimax(ply, stateList):
    currentState = stateList[0][1]
    if ply == 0:
        return [basicStaticEval(currentState), stateList]
    newMoves = generate_moves(currentState)
    bestMove = newMoves[0]
    if currentState.whose_move == WHITE:
        best = float('-inf')
        for nextMove in newMoves:
            newValue = minimax(ply - 1, nextMove)[0]
            if newValue >= best:
                best = newValue
                bestMove = nextMove
        return [best, bestMove]
    else:
        best = float('inf')
        for nextMove in newMoves:
            newValue = minimax(ply - 1, nextMove)[0]
            if newValue >= best:
                best = newValue
                bestMove = nextMove
        return [best, bestMove]

# # Returns a list of form [[old_spot, new_spot], newState]
# def minimax(ply, currentState):
#     if ply == 0:
#         return [((), ()), currentState]
#     newMoves = generate_moves(currentState)
#     newMove = newMoves[0]
#     if currentState.whose_move == WHITE:
#         bestMove = float('-inf')
#         for i in range(len(newMoves)):
#             newState = BC.BC_state(newMoves[i][1], BLACK)
#             newValue = basicStaticEval(minimax(ply - 1, newState)[1])
#             if newValue > bestMove:
#                 bestMove = newValue
#                 newMove = newMoves[i]
#         return newMove
#     else:
#         bestMove = float('inf')
#         for i in range(len(newMoves)):
#             newState = BC.BC_state(newMoves[i][1], WHITE)
#             newValue = basicStaticEval(minimax(ply - 1, newState)[1])
#             if newValue > bestMove:
#                 bestMove = newValue
#                 newMove = newMoves[i]
#         return newMove


# Returns a list: [bestValue, [[((old_spot), (new_spot)), newState], remark]]
# stateList is same format as return value of generate_moves:
#   [[((row, col),(row_temp, col_temp)), newState, 1 - whose_move)],"lmao"]
def alphabeta_pruning(ply, stateList, alpha, beta):
    currentState = stateList[0][1]  # new state also within the stateList
    if ply == 0:
        return [basicStaticEval(currentState), stateList]
    newMoves = generate_moves(currentState)
    bestMove = newMoves[0]
    if currentState.whose_move == WHITE:
        best = float('-inf')
        for nextMove in newMoves:
            newValue = alphabeta_pruning(ply - 1, nextMove, alpha, beta)[0]
            best = max(best, newValue)
            alpha = max(alpha, best)
            if newValue >= best:
                best = newValue
                bestMove = nextMove
            if beta <= alpha:
                break
        return [best, bestMove]
    else:
        best = float('inf')
        for nextMove in newMoves:
            newValue = alphabeta_pruning(ply - 1, nextMove, alpha, beta)[0]
            best = max(best, newValue)
            alpha = max(alpha, best)
            if newValue >= best:
                best = newValue
                bestMove = nextMove
            if beta <= alpha:
                break
        return [best, bestMove]


# # SYNTAX will be cleaned up for sake of clarity and readability
# def alphabeta_pruning(ply, currentState, alpha, beta):
#     if ply == 0:
#         return [basicStaticEval(currentState), ((), ()), currentState]
#     newMoves = generate_moves(currentState)
#     newMove = [0, newMoves[0]]  # [value, [((oldspot), (newspot)), state]]
#     if currentState.whose_move == WHITE:
#         best = float('-inf')
#         for i in range(len(newMoves)):
#             newState = BC.BC_state(newMoves[i][1], BLACK)
#             newValue = alphabeta_pruning(ply - 1, newState, alpha, beta)[0]
#             newMove = newMoves[i]
#             best = max(best, newValue[0])
#             alpha = max(alpha, best)
#             if beta <= alpha:
#                 break
#         return [best, newMove[1:]]
#     else:
#         best = float('inf')
#         for i in range(len(newMoves)):
#             newState = BC.BC_state(newMoves[i][1], WHITE)
#             newValue = alphabeta_pruning(ply - 1, newState, alpha, beta)[0]
#             newMove = newMoves[i]
#             best = max(best, newValue[0])
#             alpha = max(alpha, best)
#             if beta <= alpha:
#                 break
#         return [best, newMove[1:]]


def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # Maps piece numbers to characters
    board_list = currentState.board
    for r in range(8):
        for c in range(8):
            board_list[r][c] = BC.CODE_TO_INIT[board_list[r][c]]
    currentState.board = board_list

    start_time = time.time()
    ply = 1
    while time.time() - start_time < timelimit:
        best_move = minimax(ply, currentState)[1]
        ply += 1

    # The following is a placeholder that just copies the current state.
    # newState = BC.BC_state(currentState.board)
    newState = best_move[0][1]

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    # move = ((6, 4), (3, 4))
    move = best_move[0][0]

    # Make up a new remark
    newRemark = "I END MY TURN."

    return [[move, newState], newRemark]

def index_to_notation(row, col):
    notation_val = ''
    notation_val = chr(col + 97) + str(8 - row)
    return notation_val 

def nickname():
    return "Gary"

def introduce():
    return '''I'm Gary Exasparov, a \"champion\" Baroque Chess agent.
    I was created by Jeffrey Gao (jgao117) and Ben Yan (yanb3).'''

# initialize data structures and fields here
def prepare(player2Nickname="My Dear Opponent", playWhite=True):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    '''if playWhite:
        for i in range(7):
            pieces[i] = pieces[i].upper()
    '''
    output = {'CURRENT_STATE_STATIC_EVAL': None, 'N_STATES_EXPANDED': 0, 'N_STATIC_EVALS': 0, 'N_CUTOFFS': 0}
    pass

def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    values = {'P': 1, 'L': 2, 'I': 2, 'W': 2, 'K': 100, 'C': 2, 'F': 2,
              'p': -1, 'l': -2, 'i': -2, 'w': -2, 'k': -100, 'c': -2, 'f': -2}
    sum = 0
    board_list = state.board
    for row in range(8):
        for col in range(8):
            if board_list[row][col] != '-':
                sum += values[board_list[row][col]]
    return sum

def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    pass