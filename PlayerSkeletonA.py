'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC

global output
pieces = ['p','l','i','w','k','c','f']  # pieces
operators = {'p':[(1,0),(0,1),(-1,0),(0,-1)],
             'l':[(2,0),(0,2),(-2,0),(0,-2)],
             'i':[()],
             'w':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],
             'k':[(1,1),(1,-1),(-1,1),(-1,-1)],
             'c':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)],
             'f':[(1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1)]}


def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    board_list = BC.parse(currentState.board)  # list of current board positions in row-major order
    possible_moves = []
    for row in range(8):
        for col in range(8):
            row_temp = row
            col_temp = col
            if board_list[row][col] is not '-':
                current_ops = operators[board_list[row][col].lower()]
                for op in current_ops:
                    while can_move(row_temp, col_temp, op, board_list):
                        row_temp += op[0]
                        col_temp += op[1]
                        possible_moves.append([row_temp, col_temp])

    # generate tree
    # run minimax on tree
    #   while running minimax do static eval on leaf node (V value)


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

# check if piece can perform legal move
def can_move(row, col, op, board_list):
    return ((row + op[0] >= 0) and (row + op[0] < 8) and (col + op[1] >= 0)
            and (col + op[1] < 8) and (board_list[row + op[0]][col + op[1]] == '-'))

# implement minimax algorithm here
def minimax():
    pass

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
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

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
    if playWhite:
        for i in range(7):
            pieces[i] = pieces[i].upper()
    output = {'CURRENT_STATE_STATIC_EVAL': None, 'N_STATES_EXPANDED': 0, 'N_STATIC_EVALS': 0, 'N_CUTOFFS': 0}
    pass

def basicStaticEval(state, board_list):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    values = {'P': 1, 'L': 2, 'I': 2, 'W': 2, 'K': 100, 'C': 2, 'F': 2,
              'p': -1, 'l': -2, 'i': -2, 'w': -2, 'k': -100, 'c': -2, 'f': -2}
    sum = 0
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

