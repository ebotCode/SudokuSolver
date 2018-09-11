from sudokuUtils import *

"""
Author : Tobe 
SudokuSolver.py

This code solves the sudoku puzzle using backtracking with constraint propagation. 
Backtracking is just a Depth First Search (DFS) on the sudoku search space. This search space 
is huge, with lots of useless states, that would never lead to a solution. Hence, pruning (or 
constrait propagation) is needed. 
The pruning strategies used here are : Eliminate and OnlyChoiceConstraint

Eliminate : this searches the puzzle for boxes that are already filled.
            once identified, the value is eliminated from the list of possible values for
            its peers(boxes in the same row, col or square) 

OnlyChoiceConstraint : This constraint looks for boxes that are constrained to a value. 
                    A box is said to be constrained to a value, when one of its possible value 
                    occurs only once in either the containing row, column or square. 

The pruning strategies are applied until the puzzle cannot be further reduced. At this point, 
we select the box with the fewest possibilities (greater than 1), select one of its possible values
and we proceed. Whenever we cannot advance a solution, we backtrack.                             

"""

testString = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# testString = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

# testString =  '.......12....35......6...7.7.....3.....4..8..1...........12.....8.....4..5....6..'

#. very simple puzzle. 
testString = '483921.579673458.125187649354813297672956.13813679824537268951481425376969541738.'

#. convert the sudoku string into a more suitable format. 
initial_sudoku_grid = ConvertSudokuStringToGrid(testString)
#. convert the sudoku string into a format suitable for searching 
sudoku_search_grid = ConvertSudokuStringToSearchGrid(testString)
#. Perform Depth first search with constraint propagation (pruning)
solution,ninstances = SolveSudoku(sudoku_search_grid, use_constraint = True)

print()
print()
Display(initial_sudoku_grid)
print('*************************')
print()

if solution:
    print("< Solution Found after %d instances >"%ninstances)
    print()
    Display(solution)
    print('*************************')
else:
    print("< No Solution Found >")
