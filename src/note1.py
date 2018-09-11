#pragma once

/* Sudoku solver*/

#ifndef SUDOKUSOLVER_H
#define SUDOKUSOLVER_H

#include <vector> 
#include <iostream> 

#include <iomanip> 

class SudokuBoard {

public: 

	SudokuBoard():
	nrow(9), ncolumn(9)
	{
		grid.resize(nrow); 
		for (int i = 0; i < nrow; i++) {
			grid.at(i).resize(ncolumn); 
		}
		// initialise to zero. 
		for (int row = 0; row < nrow; row++) {
			for (int col = 0; col < ncolumn; col++) {
				grid.at(row).at(col) = 0; 
			}
		}
		// number of open squares.
		open_count = nrow * ncolumn; 
	}

	void fillValue(int row, int col, int value) {
		if (grid.at(row).at(col) == 0) {
			open_count -= 1;
		}
		grid.at(row).at(col) = value;
	}

	void freeValue(int row, int col) {
		if (grid.at(row).at(col) != 0) {
			open_count += 1;
		}
		grid.at(row).at(col) = 0; 
	}

	void print() {
		for (int row = 0; row < nrow; row++)
		{
			for (int col = 0; col < ncolumn; col++)
			{
				std::cout << grid.at(row).at(col) << " ";
				if ((col+1) % 3 == 0)
				{
					std::cout << "| ";
				}
			}
			std::cout << std::endl;
			if ((row +1) % 3 == 0) {
				for (int col = 0; col < ncolumn; col++)
				{
					std::cout << "--" << " ";
				}
			}
			std::cout << std::endl;
			
		}
	}

	int nrow, ncolumn; 
	int open_count; 
	std::vector<std::vector<int>> grid; 

};

struct Cell{
	int row;
	int column; 
};

class SudokuSolver {
public:
	SudokuSolver(SudokuBoard& board_in){
		board_ = &board_in; 
		finished_ = false; 
		count_is_solution_ = 0; 
	}
	void solve() {
		solvePuzzle(*board_);
	}
	void solvePuzzle(SudokuBoard& board_in) {
		
		if (is_solved(board_in) ) {
			
			finished_ = true;
			std::cout << "solution found " << std::endl; 
		}
		else {
			Cell next_cell;
			std::vector<int> candidates = cellCandidates(next_cell,board_in);

			//debug:
			//std::cout << "just computed the next cell to solve " << next_cell.row <<" " << next_cell.column << std::endl;

			if (candidates.size() == 0) { return; } // look-ahead. 
			// debug:
			if (candidates.size() == 0) {
				std::cout << "***************************************************" << std::endl; 
				std::cout << "Tobe caught one here without candidates"<<std::endl; 
				std::cout << next_cell.row << " " << next_cell.column << std::endl;

				board_in.print();
				int bdummy; 
				std::cin >> bdummy; 
				
			}
			// debug: 
			
			std::cout << "is solution count = " << count_is_solution_ << std::endl; 
			/* std::cout << "Candidates for cell (" << next_cell.row << ", " << next_cell.column << ") = ";
			for (int i = 0; i < candidates.size(); i++) {
				std::cout << candidates.at(i) << ", ";
			}
			std::cout << std::endl; 

			//int adummy; 
			//std::cin >> adummy;

			*/

			for (size_t i = 0; i < candidates.size(); i++) {
				
				board_in.fillValue(next_cell.row, next_cell.column, candidates.at(i));
				//std::cout << "Move made::: printting table " << std::endl; 
				//board_in.print(); 
				solvePuzzle(board_in);
				if (finished_)
				{
					return; 
				}
				board_in.freeValue(next_cell.row, next_cell.column);
			}
		}

	}

	Cell nextCellToFill(SudokuBoard& board_in) {
		// picks the most constrained empty cell. 
		Cell next_cell{ -1,-1 };
		std::vector<int> candidates;

		int min_candidates = 9;
		for (int row = 0; row < board_in.nrow; row++) {
			for (int col = 0; col < board_in.ncolumn; col++) {
				if (board_in.grid.at(row).at(col) == 0) // if it is empty 
				{
					candidates = cellCandidatesLocalCount(row, col, board_in); // most constrained.
					if (candidates.size() < min_candidates) {
						next_cell.row = row;
						next_cell.column = col;
						min_candidates = candidates.size();
					}
				}

			}
		}
		return next_cell; 
	}
	std::vector<int> cellCandidatesLocalCount(int row, int column, SudokuBoard& board_in) {
		// given a position on the board, return the candidates for that position 
		std::vector<int> possible(10);
		for (int i = 0; i < possible.size(); i++) {
			possible.at(i) = 1;
		}
		// check the column. 
		for (int i = 0; i < board_in.ncolumn; i++) {
			if (board_in.grid.at(row).at(i) != 0)
				possible.at(board_in.grid.at(row).at(i)) = 0;
		}
		// check the row. 
		for (int i = 0; i < board_in.nrow; i++) {
			if (board_in.grid.at(i).at(column) != 0) {
				possible.at(board_in.grid.at(i).at(column)) = 0;
			}
		}
		// check the local section 
		int local_square_top_left_row = (row / 3) * 3;
		int local_square_top_left_col = (column / 3) * 3;

		for (int irow = local_square_top_left_row; irow <= local_square_top_left_row + 2; irow++) {
			for (int jcol = local_square_top_left_col; jcol <= local_square_top_left_col + 2; jcol++) {
				if (board_in.grid.at(irow).at(jcol) != 0) {
					possible.at(board_in.grid.at(irow).at(jcol)) = 0;
				}
			}
		}

		// prepare candidates .
		std::vector<int> candidates;
		for (int i = 1; i < possible.size(); i++) {
			if (possible.at(i) == 1) {
				candidates.push_back(i);
			}
		}

		//std::cout << "len candidates = " << candidates.size() << std::endl; 
		return candidates;

	}
	std::vector<int> cellCandidatesLookAhead(int row, int column, std::vector<int>proposal,SudokuBoard& board_in)
	{
		// prune the proposals to eliminate any option that would result in 
		std::vector<int> new_proposal;
		Cell next_cell; 
		std::vector<int> local_candidates; 
		// go through the proposal, and only include ones that do not result in a zero option cell. 
		for (int i = 0; i < proposal.size(); i++) 
		{
			board_in.fillValue(row, column, proposal.at(i));
			next_cell = nextCellToFill(board_in);
			if ((next_cell.row != -1) && (next_cell.column != -1)) {

				local_candidates = cellCandidatesLocalCount(next_cell.row, next_cell.column, board_in);
				if (local_candidates.size() > 0)
				{
					new_proposal.push_back(proposal.at(i));

				}
				board_in.freeValue(row, column);
			}
		}

		return new_proposal; 
	}

	std::vector<int> cellCandidates(Cell& next_cell, SudokuBoard& board_in) {
		Cell next_cell_to_fill = nextCellToFill(board_in);
		std::vector<int> local_candidates;

		if ((next_cell_to_fill.row != -1) && (next_cell_to_fill.column != -1))
		{
			local_candidates = cellCandidatesLocalCount(next_cell_to_fill.row,
				next_cell_to_fill.column,
				board_in);

			next_cell.row = next_cell_to_fill.row; 
			next_cell.column = next_cell_to_fill.column; 
		}
		//std::vector<int> ahead_candidates = cellCandidatesLookAhead(row, column, local_candidates, board_in);
		return local_candidates; 
	}
		//*/

	bool is_solved(SudokuBoard& board_in) {
		count_is_solution_ += 1;
		return (board_in.open_count == 0); // board is considerd solved when the number of open squares is zero. 
	}

private:
	SudokuBoard* board_; 
	bool finished_;
	int count_is_solution_;


};



void SolveSudoku1()
{
	SudokuBoard puzzle;
	puzzle.fillValue(3, 0, 7);
	puzzle.fillValue(5, 0, 1);
	puzzle.fillValue(7, 1, 8);
	puzzle.fillValue(8, 1, 5);
	puzzle.fillValue(2, 3, 6);
	puzzle.fillValue(6, 3, 1);
	puzzle.fillValue(1, 4, 3);
	puzzle.fillValue(6, 4, 2);
	puzzle.fillValue(1, 5, 5);
	puzzle.fillValue(3, 6, 3);
	puzzle.fillValue(4, 6, 8);
	puzzle.fillValue(8, 6, 6);
	puzzle.fillValue(0, 7, 1);
	puzzle.fillValue(2, 7, 7);
	puzzle.fillValue(7, 7, 4);
	puzzle.fillValue(0, 8, 2);

	std::cout << "sudoku board before solution " << std::endl; 
	puzzle.print();

	std::cout << " open squares " << puzzle.open_count << std::endl; 
	std::cout << "starting solution " << std::endl; 
	SudokuSolver solve_puzzle(puzzle);
	solve_puzzle.solve();
	std::cout << "Done " << std::endl;


	std::cout << "after solution " << std::endl; 
	puzzle.print();

}



void SolveSudoku2()
{
	SudokuBoard puzzle;
	puzzle.fillValue(3, 0, 7);
	puzzle.fillValue(5, 0, 1);
	puzzle.fillValue(7, 1, 8);
	puzzle.fillValue(8, 1, 5);
	puzzle.fillValue(2, 3, 6);
	puzzle.fillValue(6, 3, 1);
	puzzle.fillValue(1, 4, 3);
	puzzle.fillValue(6, 4, 2);
	puzzle.fillValue(1, 5, 5);
	puzzle.fillValue(3, 6, 3);
	puzzle.fillValue(4, 6, 8);
	puzzle.fillValue(8, 6, 6);
	puzzle.fillValue(0, 7, 1);
	puzzle.fillValue(2, 7, 7);
	puzzle.fillValue(7, 7, 4);
	puzzle.fillValue(0, 8, 2);

	std::cout << "sudoku board before solution " << std::endl;
	puzzle.print();

	std::cout << " open squares " << puzzle.open_count << std::endl;

	SudokuSolver solve_puzzle(puzzle);
	solve_puzzle.solve();


	std::cout << "after solution " << std::endl;
	puzzle.print();

}



#endif 