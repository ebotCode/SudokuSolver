# SudokuSolver 

This repository contains code for solving a sudoku puzzle. 

The code implements backtracking search, with constraint propagation to search for a valid solution to the given sudoku puzzle. 

This code solves the sudoku puzzle using backtracking with constraint propagation. 
Backtracking is just a Depth First Search (DFS) on the sudoku search space. This search space 
is huge, with lots of useless states, that would never lead to a solution. Hence, pruning (or 
constrait propagation) is needed. 

The pruning strategies used here are : Eliminate and OnlyChoiceConstraint (see src/sudokuUtils.py)

Eliminate : 

this searches the puzzle for boxes that are already filled. once identified, the value is eliminated from the list of possible values for its peers(boxes in the same row, col or square) 

OnlyChoiceConstraint : 

This constraint looks for boxes that are constrained to a value. A box is said to be constrained to a value, when one of its possible value occurs only once in either the containing row, column or square. 

The pruning strategies are applied until the puzzle cannot be further reduced. At this point, 
we select the box with the fewest possibilities (greater than 1), select one of its possible values
and we proceed. Whenever we cannot advance a solution, we backtrack.                             

## Sample Sudoku Grid: 

    3 |  2   |6     
9     |3   5 |    1 
    1 |8   6 |4     
------+------+------
    8 |1   2 |9     
7     |      |    8 
    6 |7   8 |2     
------+------+------
    2 |6   9 |5     
8     |2   3 |    9 
    5 |  1   |3     
*************************

Solution : The program found the solution after just expanding one-instance (by using the pruning methods only.)

< Solution Found after 1 instances >

4 8 3 |9 2 1 |6 5 7 
9 6 7 |3 4 5 |8 2 1 
2 5 1 |8 7 6 |4 9 3 
------+------+------
5 4 8 |1 3 2 |9 7 6 
7 2 9 |5 6 4 |1 3 8 
1 3 6 |7 9 8 |2 4 5 
------+------+------
3 7 2 |6 8 9 |5 1 4 
8 1 4 |2 5 3 |7 6 9 
6 9 5 |4 1 7 |3 8 2 
*************************

## Sample Sudoku Puzzle 2 : (a harder puzzle)

4     |      |8   5 
  3   |      |      
      |7     |      
------+------+------
  2   |      |  6   
      |  8   |4     
      |  1   |      
------+------+------
      |6   3 |  7   
5     |2     |      
1   4 |      |      
*************************

Solution : The program found the solution after just expanding 54 instances.

< Solution Found after 54 instances >

4 1 7 |3 6 9 |8 2 5 
6 3 2 |1 5 8 |9 4 7 
9 5 8 |7 2 4 |3 1 6 
------+------+------
8 2 5 |4 3 7 |1 6 9 
7 9 1 |5 8 6 |4 3 2 
3 4 6 |9 1 2 |7 5 8 
------+------+------
2 8 9 |6 4 3 |5 7 1 
5 7 3 |2 9 1 |6 8 4 
1 6 4 |8 7 5 |2 9 3 
*************************


## Importance of Pruning

Without Search pruning (constraint propagation), the program would try all possible values for each unfilled box. How long would it take? Well, it depends on the problem. for some sudoku puzzles it takes long. For the example puzzle below, searching without pruning took a total of 4227 instances to get the solution. But with pruning, it only took 1 instances.

puzzle: 

4 8 3 |9 2 1 |  5 7 
9 6 7 |3 4 5 |8   1 
2 5 1 |8 7 6 |4 9 3 
------+------+------
5 4 8 |1 3 2 |9 7 6 
7 2 9 |5 6   |1 3 8 
1 3 6 |7 9 8 |2 4 5 
------+------+------
3 7 2 |6 8 9 |5 1 4 
8 1 4 |2 5 3 |7 6 9 
6 9 5 |4 1 7 |3 8   
*************************

soulution without pruning. 

< Solution Found after 4227 instances >

4 8 3 |9 2 1 |6 5 7 
9 6 7 |3 4 5 |8 2 1 
2 5 1 |8 7 6 |4 9 3 
------+------+------
5 4 8 |1 3 2 |9 7 6 
7 2 9 |5 6 4 |1 3 8 
1 3 6 |7 9 8 |2 4 5 
------+------+------
3 7 2 |6 8 9 |5 1 4 
8 1 4 |2 5 3 |7 6 9 
6 9 5 |4 1 7 |3 8 2 
*************************
