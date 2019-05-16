'''Nick_Monsees_BC_Player.py
Written by Jeffrey Gao (jgao117@uw.edu) and Ben Yan (yanb3@uw.edu).

'''

import BC_state_etc as BC
import time
import random

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
remarks = ['Really now?', 'Is that all you\'ve got?', 'Are you sure about that move?', 'Do you know what you are doing?',
           'You sure you don\'t want to take that back?', 'Who taught you how to play?', 'Did you miss a move?', 'What do you think about this?',
            'Don\'t you just love this game?', 'How are you feeling about this move?']

operators = {'p':[(1,0),(0,1),(-1,0),(0,-1)],  # pawn
             'l':[(2,0),(0,2),(-2,0),(0,-2)],  # long leaper
             'i':[],  # imitator (1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1),(2,0),(0,2),(-2,0),(0,-2)
             'w':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # withdrawer (queen)
             'k':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # king
             'c':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],  # coordinator
             'f':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]}  # freezer

adjacent_squares= [(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]

values = {'P': 10, 'L': 25, 'I': 10, 'W': 20, 'K': 1000, 'C': 25, 'F': 20,
              'p': -10, 'l': -25, 'i': -10, 'w': -20, 'k': -1000, 'c': -25, 'f': -20}
centralization_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [2, 4, 6, 6, 6, 6, 4, 2],
                        [2, 4, 6, 6, 6, 6, 4, 2],
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]]

flatten = lambda l: [item for sublist in l for item in sublist]

def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    best_move = [0, [((), ()), currentState, 0, 0]]
    if alphaBeta:
        bestMove = alphabeta_pruning(ply, [[((), ()), currentState], 'remark'], float('inf'), float('-inf'))[1]
    else:
        bestMove = minimax(ply, [[((), ()), currentState], 'remark'])[1]
    if useBasicStaticEval:
        output['CURRENT_STATE_STATIC_EVAL'] = basicStaticEval(bestMove[1])
    elif useZobristHashing:
        pass  # temporary
    output['N_STATES_EXPANDED'] = states_expanded
    output['N_STATIC_EVALS'] = states_evaluated
    output['N_CUTOFFS'] = 0
    return output


def next_to_freezer(board_list, row, col):
    for op in [(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]:
        if ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
           and (col + op[1] < 8)):
            if (board_list[row + op[0]][col + op[1]].isupper() != board_list[row][col].isupper() and
                    board_list[row + op[0]][col + op[1]].lower() == 'f'):
                return True
    return False


def generate_moves(currentState):
    board_list = currentState.board  # list of current board positions in row-major order
    whose_move = currentState.whose_move
    possible_moves = []
    #king_position = [[-1, -1], [-1, -1]]]
    
    for row in range(8):
        for col in range(8):
            row_temp = row
            col_temp = col
            piece = board_list[row][col]
            if (board_list[row][col] is not '-' and not next_to_freezer(board_list, row_temp, col_temp)):
                if (piece.lower() == 'k'
                    and piece in pieces[whose_move]):
                    #king_position[whose_move] = [row, col]
                    #print(king_position)
                    for king_op in operators['k']:
                        row_temp = row
                        col_temp = col
                        if king_case(row, col, king_op, board_list):
                            row_temp += king_op[0]
                            col_temp += king_op[1]
                            new_board_state = [r[:] for r in board_list]
                            new_board_state[row_temp][col_temp] = new_board_state[row][col]
                            new_board_state[row][col] = '-'
                            possible_moves.append([((row, col),(row_temp, col_temp)),
                                                    BC.BC_state(new_board_state, 1 - whose_move)])
                elif (piece.lower() == 'l' 
                    and piece in pieces[whose_move]):
                    current_ops = operators['p']
                    for op in current_ops:
                        row_temp = row
                        col_temp = col
                        while can_move(row_temp, col_temp, op, board_list):
                            row_temp += op[0]
                            col_temp += op[1]
                            #ending_square = index_to_notation(row_temp, col_temp)
                            new_board_state = [r[:] for r in board_list]
                            new_board_state[row_temp][col_temp] = new_board_state[row][col]
                            new_board_state[row][col] = '-'
                            possible_moves.append([((row, col),(row_temp, col_temp)),
                                                    BC.BC_state(new_board_state, 1 - whose_move)])
                    for op in operators['l']:
                        row_temp = row
                        col_temp = col
                        if (can_move(row_temp, col_temp, op, board_list)
                            and long_leaper_capturable(row, col, op, board_list)):
                            row_temp += op[0]
                            col_temp += op[1]
                            new_board_state = [r[:] for r in board_list]
                            new_board_state[row_temp][col_temp] = new_board_state[row][col]
                            new_board_state[row][col] = '-'
                            new_board_state[int(row + op[0] / 2)][int(col + op[1] / 2)] = '-'
                            possible_moves.append([((row, col),(row_temp, col_temp)),
                                                    BC.BC_state(new_board_state, 1 - whose_move)])
                elif (piece.lower() != 'i' 
                    and piece in pieces[whose_move]):
                    current_ops = operators[board_list[row][col].lower()]
                    for op in current_ops:
                        row_temp = row
                        col_temp = col
                        while can_move(row_temp, col_temp, op, board_list):
                            row_temp += op[0]
                            col_temp += op[1]
                            #ending_square = index_to_notation(row_temp, col_temp)
                            new_board_state = [r[:] for r in board_list]
                            new_board_state[row_temp][col_temp] = new_board_state[row][col]
                            new_board_state[row][col] = '-'
                            if piece.lower() == 'p':
                                for op_cap in current_ops:
                                    if pincer_capturable(row_temp, col_temp, op_cap, new_board_state):
                                        new_board_state[row_temp + op_cap[0]][col_temp + op_cap[1]] = '-'
                            elif piece.lower() == 'w':
                                if withdrawer_capturable(row, col, op, board_list):
                                    new_board_state[row - op[0]][col - op[1]] = '-'
                            elif piece.lower() == 'c':
                                #capture = coordinator_capturable(row_temp, col_temp, new_board_state, king_position, whose_move)
                                capture = coordinator_capturable(row_temp, col_temp, new_board_state, whose_move)

                                for captured in capture:
                                    new_board_state[captured[0]][captured[1]] = '-'
                            possible_moves.append([((row, col),(row_temp, col_temp)),
                                                    BC.BC_state(new_board_state, 1 - whose_move)])
                elif (piece.lower() == 'i' 
                    and piece in pieces[whose_move] 
                    and not next_to_freezer(board_list, row_temp, col_temp)):
                    current_ops = operators['p']
                    for op in current_ops:
                        row_temp = row
                        col_temp = col
                        while can_move(row_temp, col_temp, op, board_list):
                            row_temp += op[0]
                            col_temp += op[1]
                            #ending_square = index_to_notation(row_temp, col_temp)
                            new_board_state = [r[:] for r in board_list]
                            new_board_state[row_temp][col_temp] = new_board_state[row][col]
                            new_board_state[row][col] = '-'
                            possible_moves.append([((row, col),(row_temp, col_temp)),
                                BC.BC_state(new_board_state, 1 - whose_move)])
                    for op in operators['l']:
                        row_temp = row
                        col_temp = col
                        if can_move(row_temp, col_temp, op, board_list):
                            row_temp += op[0]
                            col_temp += op[1]
                            if (board_list[int(row + op[0] / 2)][int(col + op[1] / 2)].lower() == 'l' and
                                long_leaper_capturable(row, col, op, board_list)):
                                new_board_state = [r[:] for r in board_list]
                                new_board_state[row_temp][col_temp] = new_board_state[row][col]
                                new_board_state[row][col] = '-'
                                new_board_state[int(row + op[0] / 2)][int(col + op[1] / 2)] = '-'
                                possible_moves.append([((row, col),(row_temp, col_temp)),
                                                    BC.BC_state(new_board_state, 1 - whose_move)])
                    
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
    new_row = row - op[0]
    new_col = col - op[0]
    return (((new_row >= 0) and (new_row < 8) and (new_col >= 0) and (new_col < 8)) and 
    board_list[row][col].isupper() != board_list[new_row][new_col].isupper())


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
    new_row = int(row + op[0] / 2)
    new_col = int(col + op[1] / 2)
    return (board_list[row][col].isupper() != board_list[new_row][new_col].isupper())


# Checks for whether there is a capturable piece by a move of the cinator
# Returns the (rank, file) of a piece if capturable; if none, returns empty list
def coordinator_capturable(c_new_row, c_new_col, new_board_list, whose_move):
    capturable = []
    #if king_position[whose_move] is [-1, -1]:
    for r in range(8):
        for c in range(8):
            if new_board_list[r][c] == pieces[whose_move][KING]:
                kings_row = r
                kings_col = c
    #else:
    #    kings_row = king_position[whose_move][0]
    #    kings_col = king_position[whose_move][1]
    if c_new_col == kings_col and c_new_row == kings_row:
        return capturable
    if (new_board_list[kings_row][c_new_col] != '-'
       and new_board_list[kings_row][c_new_col].isupper() != new_board_list[c_new_row][c_new_col].isupper()):
        capturable.append([kings_row, c_new_col])
    if (new_board_list[c_new_row][kings_col] != '-'
       and new_board_list[c_new_col][kings_col].isupper() != new_board_list[c_new_row][c_new_col].isupper()):
        capturable.append([c_new_col, kings_col])
    #print(capturable)
    return capturable


# Returns a list: [bestValue, [((), ()), newState]]
# stateList: [((),()), BC.BC_state(new_board_state, 1 - whose_move)]
def minimax(ply, stateList):
    currentState = stateList[1]
    if ply == 0:
        return [staticEval(currentState), stateList]
    newMoves = generate_moves(currentState)
    bestMove = []
    if currentState.whose_move == WHITE:
        best = float('-inf')
        for nextMove in newMoves:
            newValue = minimax(ply - 1, nextMove)[0]
            if newValue > best:
                best = newValue
                bestMove = nextMove
        return [best, bestMove]
    else:
        best = float('inf')
        for nextMove in newMoves:
            newValue = minimax(ply - 1, nextMove)[0]
            if newValue < best:
                best = newValue
                bestMove = nextMove
        return [best, bestMove]


# Returns a list: [bestValue, [((), ()), newState]]
# stateList: [((),()), BC.BC_state(new_board_state, 1 - whose_move)]
def alphabeta_pruning(ply, stateList, alpha, beta, start_time):
    if time.time() - start_time > 0.9:
        return
    global states_expanded
    states_expanded += 1
    currentState = stateList[1]
    if ply == 0:
        global states_evaluated
        states_evaluated += 1
        return [staticEval(currentState), stateList]
    start_time = time.time()
    newMoves = generate_moves(currentState)
    bestMove = []
    if currentState.whose_move == WHITE:
        best = float('-inf')
        for nextMove in newMoves:
            temp = alphabeta_pruning(ply - 1, nextMove, alpha, beta, start_time)
            if temp == None:
                return
            newValue = temp[0]
            if newValue > best:
                best = newValue
                bestMove = nextMove
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return [best, bestMove]
    else:
        best = float('inf')
        for nextMove in newMoves:
            temp = alphabeta_pruning(ply - 1, nextMove, alpha, beta, start_time)
            if temp == None:
                return
            newValue = temp[0]
            if newValue < best:
                best = newValue
                bestMove = nextMove
            beta = max(beta, best)
            if beta <= alpha:
                break
        return [best, bestMove]


def makeMove(currentState, currentRemark, timelimit=1):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.
    translated_board = [r[:] for r in currentState.board]
    for r in range(8):
        for c in range(8):
            translated_board[r][c] = BC.CODE_TO_INIT[translated_board[r][c]]
    newCurrentState = BC.BC_state(translated_board, currentState.whose_move)

    global states_expanded
    states_expanded = 0
    global states_evaluated
    states_evaluated = 0
    start_time = time.time()
    ply = 1
    best_move = [0, [((), ()), currentState, 0, 0]]
    while time.time() - start_time < timelimit and ply <= 2:
        # best_move = minimax(ply, [((), ()), newCurrentState])[1]
        temp = alphabeta_pruning(ply, [((), ()), newCurrentState], float('-inf'), float('inf'), start_time)
        if temp == None:
            break
        best_move = temp[1]
        ply += 1

    newState = best_move[1]
    newBoard = newState.board
    for r in range(8):
        for c in range(8):
            newBoard[r][c] = BC.INIT_TO_CODE[newBoard[r][c]]
    newState.board = newBoard

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = best_move[0]

    # Make up a new remark
    newRemark = random.choice(remarks)
    print("states expanded: " + str(states_expanded))
    print("states evaluated: "  + str(states_evaluated))
    return [[move, newState], newRemark]


def index_to_notation(row, col):
    notation_val = ''
    notation_val = chr(col + 97) + str(8 - row)
    return notation_val 


def nickname():
    return "Nick"


def introduce():
    return '''I'm Nick Monsees, a \"champion\" Baroque Chess agent.
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
    sum = 0
    board_list = state.board
    for row in range(8):
        for col in range(8):
            piece = board_list[row][col]
            if piece != '-' and not next_to_freezer(board_list, row, col):
                sum += values[board_list[row][col]]
                if piece.isupper():
                    sum += centralization_table[row][col]
                else:
                    sum -= centralization_table[row][col]
                if piece.isupper():
                    sum += 6 * attacked_pieces(board_list, row, col)
                else:
                    sum -= 6 * attacked_pieces(board_list, row, col)
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    return sum


# computes value for pieces that have a wider range of attack
def attacked_pieces(board_list, row, col):
    piece = board_list[row][col].lower()
    attacked = 0
    for op in operators[piece]:
        if can_move(row, col, op, board_list):
            if piece == 'l':
                if long_leaper_capturable(row, col, op, board_list):
                    attacked += 1
            if piece == 'w':
                if withdrawer_capturable(row, col, op, board_list):
                    attacked += 1
                    #print(attacked)
    return attacked


# computes value of proximity of pieces within another piece
def adjacent_pieces(board_list, row, col):
    friendly_pieces = 0
    opposing_pieces = 0
    for square in adjacent_squares:
        if ((row + square[0] >= 0) and (row + square[0] < 8) and (col + square[1] >= 0)
           and (col + square[1] < 8) and board_list[row + square[0]][col + square[1]] != '-'):
            if board_list[row][col].isupper() == board_list[row + square[0]][col + square[1]].isupper():
                friendly_pieces += 1
            else:
                opposing_pieces += 1
    return [friendly_pieces, opposing_pieces]