#!/usr/local/bin/python3

from queue import PriorityQueue
import sys
#import math

#Dictionary of valid moves
MOVES = {"original": { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }, \
                      "circular": { "R": (0, -3), "L": (0, 3), "D": (-3, 0), "U": (3,0) }, \
                      "luddy": { "A": (2,1), "B": (2,-1), "C": (-2,1), "D": (-2,-1), "E": (1,2), "F": (1,-2), "G": (-1,2), "H": (-1,-2) } }

#Returns the index (board position) for a given row, col pair
def rowcol2ind(row, col):
    return row*4 + col

#Returns row, col pair for a given index
def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

#Check if the row, col is present in a 4x4 grid
def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

#Swaps two given indices in a given state
def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

#
def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

#Check if board is solvable
def permutation_inversion(start_state):
    perm_inv = 0

    for i in range(len(start_state)-1):
        for j in range(i+1, len(start_state)-1):
            if start_state[i] > start_state[j]:
                perm_inv += 1
    
    return (perm_inv % 2 == 0)

#Heuristic function
def misplaced_tiles(state):
     #Misplaced Tiles
     goal_state = [ i for i in range(1,len(state))] + [0]
     misplaced_tiles = 0
     
     for i in range(len(state)):
         if state[i] != goal_state[i]:
             misplaced_tiles += 1
     
     return misplaced_tiles
 
# =============================================================================
# #Heuristic function (unused)
# def manhattan_dist(state):
#     
#     goal_state = [ i for i in range(1,len(state))] + [0]
#     manhattan_dist = 0
#     
#     for i in range(len(state)):
#         (goal_row, goal_col) = ind2rowcol(goal_state.index(i))
#         (state_row, state_col) = ind2rowcol(goal_state.index(i))
#         manhattan_dist += abs(state_row - goal_row) + abs(state_col - goal_col)
#     
#     return manhattan_dist
# =============================================================================

#return a list of possible successor states
def successors(state, variant):
    if variant in ("original", "luddy"):
        (empty_row, empty_col) = ind2rowcol(state.index(0))
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                 for (c, (i, j)) in MOVES[variant].items() if valid_index(empty_row+i, empty_col+j) ]
    
    elif variant == "circular":
        ind = state.index(0)
        (empty_row, empty_col) = ind2rowcol(ind)
        if ind not in (5, 6, 9, 10):
            moves_circular = [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                     for (c, (i, j)) in MOVES["circular"].items() if valid_index(empty_row+i, empty_col+j) ]
            moves_original = [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                    for (c, (i, j)) in MOVES["original"].items() if valid_index(empty_row+i, empty_col+j) ]
            return moves_circular + moves_original
        else:
            return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                    for (c, (i, j)) in MOVES["original"].items() if valid_index(empty_row+i, empty_col+j) ]
 

#check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
#The solver! - using A*
def solve(initial_board, variant):
   
    if permutation_inversion(initial_board):
        fringe = PriorityQueue()
        fringe.put( ( 0 + misplaced_tiles(initial_board), initial_board , "" ) )
        moves = 0
        while not fringe.empty():
            _, state, route_so_far = fringe.get()
            moves += 1
            for (succ, move) in successors( state, variant ):
                if is_goal(succ):
                    return( route_so_far + move )
                fringe.put( ( moves + misplaced_tiles(succ), succ, route_so_far + move ) )
        return False

# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    
    variant = sys.argv[2]

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))
    print("Solving...")
    
    route = solve(tuple(start_state), variant)
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + route if route else "Inf")