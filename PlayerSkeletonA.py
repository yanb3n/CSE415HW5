'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC

global output

def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    board_list = BC.parse(currentState.board)  # list of current board positions in row-major order
    if useBasicStaticEval:
        output['CURRENT_STATE_STATIC_EVAL'] = basicStaticEval(currentState)  # implement minimax algorithm here
    elif alphaBeta:
        pass  # temporary
    elif useZobristHashing:
        pass  # temporary
    output['N_STATES_EXPANDED'] = 0  # get states from minimax algorithm
    output['N_STATIC_EVALS'] = 0
    output['N_CUTOFFS'] = 0
    return output


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
def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    output = {'CURRENT_STATE_STATIC_EVAL': None, 'N_STATES_EXPANDED': 0, 'N_STATIC_EVALS': 0, 'N_CUTOFFS': 0}
    pass

# Implement minimax algorithm here
def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    pass

# Implement alpha-beta pruning here
def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    pass

