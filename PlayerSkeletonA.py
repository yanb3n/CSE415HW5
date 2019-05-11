'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC

global output
WHITE = 1
BLACK = 0
PAWN = 0
LONG_LEAPER = 2
IMITATOR = 3
WITHDRAWER = 4
KING = 5
COORDINATOR = 6
FREEZER = 7
pieces = [['P','L','I','W','K','C','F'],['p','l','i','w','k','c','f']]  # pieces, use pieces[color][piece] to check 

# for chess board notation
a = 0
b = 1
c = 2
d = 3 
e = 4
f = 5
g = 6
h = 7

operators = {'p':[(1,0),(0,1),(-1,0),(0,-1)], #pawn 
             'l':[(2,0),(0,2),(-2,0),(0,-2)], #long leaper
             'i':[()], #imitator 
             'w':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)], #withdrawer (queen)
             'k':[(1,1),(1,-1),(-1,1),(-1,-1)], #king
             'c':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)], #coordinator
             'f':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]} #freezer


def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    

    # generate tree
    # run minimax on tree
    #   while running minimax do static eval on leaf node (V value)

    '''
    if useBasicStaticEval:
        output['CURRENT_STATE_STATIC_EVAL'] = basicStaticEval(currentState, board_list)  # implement minimax algorithm
    elif alphaBeta:
        pass  # temporary
    elif useZobristHashing:
        pass  # temporary
    output['N_STATES_EXPANDED'] = 0  # get states from minimax algorithm
    output['N_STATIC_EVALS'] = 0
    output['N_CUTOFFS'] = 0
    return output
    '''

def next_to_freezer(board_list, row, col):
    for op in [(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]:
        if ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
            and (col + op[1] < 8)):
            if board_list[row + op[0]][col + op[0]]:
                return True
    return False

def generate_moves(currentState):
    board_list = currentState.board  # list of current board positions in row-major order
    whose_move = currentState.whose_move
    possible_moves = []
    for row in range(8):
        for col in range(8):
            row_temp = row
            col_temp = col
            starting_square = index_to_notation(row_temp, col_temp)
            piece = board_list[row][col]
            if (board_list[row][col] != '-'
                and piece.lower() != 'k' 
                and piece in pieces[whose_move] 
                and not next_to_freezer(board_list, row_temp, col_temp)):
                current_ops = operators[board_list[row][col].lower()]
                for op1 in current_ops:
                    while can_move(row_temp, col_temp, op1, board_list):
                        row_temp += op1[0]
                        col_temp += op1[1]
                        ending_square = index_to_notation(row_temp, col_temp)
                        new_board_state = board_list.copy()
                        new_board_state[row_temp][col_temp] = new_board_state[row][col]
                        new_board_state[row][col] = '-'
                        if piece.lower() == 'p':
                            for op2 in current_ops:
                                if pincer_capturable(row, col, op2, board_list):
                                    return 'fasle'
                        possible_moves.append([[((row, col),(row_temp, col_temp)), new_board_state],"lmao"])
    return possible_moves

# check if piece can perform legal move
def can_move(row, col, op, board_list):
    return ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
            and (col + op[1] < 8) and (board_list[row + op[0]][col + op[1]] == '-'))

def pincer_capturable(row, col, op, board_list):
    new_row = row + 2*op[0]
    new_col = col + 2*op[1]
    return ((new_row >= 0) and (new_row < 8) and (new_col >= 0)
            and (new_col < 8) and (board_list[new_row][new_col] != '-') 
            and (board_list[row][col].isupper() == board_list[new_row][new_col].isupper()))

# Returns a list of form [[old_spot, new_spot], newState]
def minimax(ply, currentState):
    if ply == 0:
        return [[], currentState]
    newMoves = generate_moves(currentState)
    newMove = newMoves[0]
    if currentState.whose_move == WHITE:
        bestMove = float('-inf')
        for i in range(newMoves):
            newState = BC.BC_state(newMoves[i][1], BLACK)
            newValue = basicStaticEval(minimax(ply - 1, newState)[1])
            if newValue > bestMove:
                bestMove = newValue
                newMove = newMoves[i]
        return newMove
    else:
        bestMove = float('inf')
        for i in range(newMoves):
            newState = BC.BC_state(newMoves[i][1], WHITE)
            newValue = basicStaticEval(minimax(ply - 1, newState)[1])
            if newValue > bestMove:
                bestMove = newValue
                newMove = newMoves[i]
        return newMove


# implement alpha-beta pruning here
def alphabeta_pruning():
    pass

def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

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