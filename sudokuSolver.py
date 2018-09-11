from utils import *
from functions import *


#testString = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
#testString = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

testString =  '.......12....35......6...7.7.....3.....4..8..1...........12.....8.....4..5....6..'

sudokuGrid = grid_values(testString)

solved_sudokuGrid = search(sudokuGrid)


print('*************************')
display(solved_sudokuGrid)
print('*************************')
