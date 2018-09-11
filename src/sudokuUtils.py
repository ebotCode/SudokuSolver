"""
Sudoku Solver utility functions. 

"""

import copy 

def cross(a,b):
    """ performs cross product of two strings a,b or list/tuple of strings """
    return [s + t for s in a for t in b]  

# define constants 
ROWS = 'ABCDEFGHI'  # row labels for the sudoku puzzle. 
COLS = '123456789'  # column labels for the sudoku puzzle 

#. BOXES: list of boxes in the sudoku puzzle. e.g "A1","A2",etc
BOXES = cross(ROWS,COLS)    

#. ROW_UNITS : list of boxes on each row. e.g ROW_UNITS[0] -> ["A1","A2",...,"A9"]
ROW_UNITS = [cross(r,COLS) for r in ROWS] 

#. COLUMN_UNITS : list of boxes on each column. e.g COLUMN_UNITS[0] -> ["A1","B1","C1",..,"I1"]
COLUMN_UNITS = [cross(ROWS,c) for c in COLS]

#. SQUARE_UNITS : lost of boxes in each 3 x 3 subgrid square.
#.                e.g SQUARE_UNITS[0] -> ["A1","A2","A3",
#.                                        "B1","B2","B3",
#.                                        "C1","C2","C3"]
SQUARE_UNITS = [cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#. A collection of all units: row_units, column_units and square_units
UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS
#. UNITS : a dictionary of :{ <box>:<row_unit,column_unit,square_unit> } associated with a box.
UNITS = dict( (s, [u for u in UNITLIST if s in u])  for s in BOXES)
#. PEERS
#. a dict of neighbors for each unit. the neighbors of a unit are 
#. 1. boxes that lie on the same row as the unit
#. 2. boxes that lie on the same col as the unit 
#. 3. boxes that lie in the same squre_grid as the unit. 
#. e.g The set list in UNITS['A1'] is shown below: (note : not ordered)
#. PEERS['A1'] -> ['B1','C1','D1','E1','F1','G1','H1','I1',
#.                     'A2','A3','A4','A5','A6','A7','A8','A9',
#.                      'B2','B3','C2','C3]
PEERS = dict((s, set(sum(UNITS[s],[])) - set([s])) for s in BOXES) # merge lists and removes duplicates.

def Display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    OUtput: None
    """

    width =  1+ max(len(values[s]) for s in BOXES)
    line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in COLS))
        if r in 'CF': print(line)
    return

def ConvertSudokuStringToGrid(sudoku_string,empty_delimiter = '.'):
    """
    Args: sudoku_string 
    Returns : a sudoku grid dictionary : 
        - keys : Box labels 
        - values : value in corresponding box for ' ' if it is empty. 
    """
    values = []
    replace_string = " "
    for c in sudoku_string:
        if c == empty_delimiter:
            values.append(replace_string)
        else:
            values.append(c)
    assert len(values) == 81
    return dict(zip(BOXES,values))

def ConvertSudokuStringToSearchGrid(sudoku_string,empty_delimiter = '.'):
    """ Convert grid string into a form {<box>:<possible-values>} that is suitable 
        for search
    Args:
        sudoku_sting: sudoku grid in string form, 81 characters long
        replace_string : the string to replace 
        empty_delimiter : the character that delimits empty sudoku squares
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: value in corresponding box, e.g. '8', or '.' if it is empty.
    """    
    # better solution
    values = []
    all_digits = '123456789'
    for c in sudoku_string:
        if c == empty_delimiter:
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
        else:
            raise ValueError("Invalid character %s"%c)
    assert len(values) == 81
    return dict(zip(BOXES,values))

def Eliminate(sudoku_search_grid):
    """
    Locate boxes that have single values, and eliminate that value from the 
    peers of that box.  
    Args:
    sudoku_search_grid: Sudoku in dictionary form
    Returns:
    Resulting Sudoku in dictionary form after eliminating values.
    """
    #. get boxes that have single values (a.k.a solved boxes)
    solved_values = [box for box in sudoku_search_grid.keys() if len(sudoku_search_grid[box]) == 1]
    # . for each of the solved boxes, eliminate the value from its peers
    for box in solved_values:
        digit = sudoku_search_grid[box]
        for peer in PEERS[box]:
            sudoku_search_grid[peer] = sudoku_search_grid[peer].replace(digit,'')
    return sudoku_search_grid

def OnlyChoiceConstraint(sudoku_search_grid):
    """ 
    Check through each row, col and square for boxes that are constrained to have
    a value. in otherwords, if a digit occors once in a unit (either row, col or square_unit)
    then the box that has that digit is constrained to have that value. 

    e.g if a row has -> ['1','245','234','268','67','259','268','47'].
             since digit '1' occurs once in the row, it is constrained to that box. 
             since digit '3' occurs once in the row, it is constrained to that box. hence 
                        the value changes from '234' to '3'
             since digit '9' occurs once in the row, it is contrained to that box. 
                        hence the value, at index 5 changes from '259' to '9'
            etc
    Args:
        sudoku_search_grid: Sudoku in dictionary form.
    Return: Resulting Sudoku in dictionary form after filling in only choices.

    """
    for unit in UNITLIST: # [row_units,col_units,square_units]
        for digit in '123456789':
            dplaces = [box for box in unit if digit in sudoku_search_grid[box]]
            if len(dplaces) == 1:
                sudoku_search_grid[dplaces[0]] = digit 
                # Notice the inplace modification. This allows new updates to the grid 
                # to be taken into account. Because, constraining a box, can cause a 
                # previously unconstrained box to become constrained.

    return sudoku_search_grid

def ReducePuzzle(sudoku_search_grid):
    """
    Using the Eliminate and OnlyChoice constraint, keep reducing the puzzle until it can't 
    be reduced any further. 
    Note: reducing the puzzle eliminates search spaces that are useless to explore. This is where
          the constraint propagation occurs. by pruning search spaces that do not meet the 
          constraint, we narrow down the search space and search efficiently. 
          If this is not done, then code would be searching the whole possible permutation
          of the possible configuration of the sudoku.
    Args:
        sudoku_search_grid: sudoku in dictionary form 
    Return : 
        a reduced sudoku grid. 
    """
    def CountSolvedBoxes(sudoku_search_grid):
        return len([box for box in sudoku_search_grid.keys() 
                                if len(sudoku_search_grid[box]) == 1 ])
    stalled = False
    #. if the number of solved boxes before applying Eliminate and OnlyChoiceContraint is the same
    #. as the result, then it can't be reduced further. stalled = True
    while not stalled:
        solved_values_before = CountSolvedBoxes(sudoku_search_grid)
        sudoku_search_grid = Eliminate(sudoku_search_grid)
        sudoku_search_grid = OnlyChoiceConstraint(sudoku_search_grid)
        # check how many BOXES have a determined value, to compare
        solved_values_after = CountSolvedBoxes(sudoku_search_grid)
        # if no new values were addeed, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in sudoku_search_grid.keys() if len(sudoku_search_grid[box]) == 0]):
            return False

    return sudoku_search_grid 

def IsSudokuSolved(sudoku_search_grid):
    # is_all_box_sigle = all(len(sudoku_search_grid[box]) == 1 for box in BOXES)    
    all_digit = '123456789'
    
    for digit in all_digit: 
        for unit in UNITLIST:
            dplaces = [box for box in unit if digit in sudoku_search_grid[box]]
            if len(dplaces) > 1:
                return False 
    return True 

    

def GetBoxWithFewestPossibilities(sudoku_search_grid):
    all_lengths = list( (len(sudoku_search_grid[box]),box) 
                          for box in BOXES 
                          if len(sudoku_search_grid[box]) > 1)
    if len(all_lengths) > 0:
        n,box_with_fewest_possibility = min(all_lengths)
        return box_with_fewest_possibility
    else:
        return None 

def SolveSudoku(sudoku_search_grid, use_constraint = True, display_count = False):
    """
    Solve the Sudoku
    Args:
        sudoku_search_grid : sudoku puzzle in dictionary form 
        use_constraint : boolean (True or False. default is True)
                         if True, the pruning methods 
                         'Eliminate' and 'OnlyChoiceConstraint' are applied. 
                         else, they are not. 
                         This can be used to see the effect of pruning on certain 
                         types of sudoku instances. 
    Returns:

    Note: 

    """
    SolveSudoku.count_search_instance = 0

    def Search(sudoku_search_grid): 
        SolveSudoku.count_search_instance += 1  
        if display_count:
            print("Search instances OPENED = ",SolveSudoku.count_search_instance)
        # first reduce the puzzle.n This prunes the search space
        if use_constraint:
            sudoku_search_grid = ReducePuzzle(sudoku_search_grid)

        #. if ReducePuzzle returns False, then the current state cannot be extended. 
        if sudoku_search_grid is False:
            return False ## Failed earlier

        #. if sudoku is solved, return the sudoku grid. 
        if IsSudokuSolved(sudoku_search_grid):
            return sudoku_search_grid ## solved!

        #. Advance the search using DFS. 
        # Choose one of the unfilled squares with the fewest possibilities
        chosen_box = GetBoxWithFewestPossibilities(sudoku_search_grid)
        if chosen_box == None : 
            return False 

        for digit in sudoku_search_grid[chosen_box]:
            # new_sudoku = sudoku_search_grid.copy() # make a new sudoku grid 
            new_sudoku_search_grid = copy.deepcopy(sudoku_search_grid)
            new_sudoku_search_grid[chosen_box] = digit         # insert this digit as the value of chosen_box
            attempt = Search(new_sudoku_search_grid)           # the recusively search. 
            if attempt:
                return attempt
        return False 


    search_result = Search(sudoku_search_grid)
    return search_result, SolveSudoku.count_search_instance
        
