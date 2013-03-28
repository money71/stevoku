#!/bin/env python

import sys
import time
import colorama

import puzzle
import csp

def main():

	colorama.init()

	if len(sys.argv) != 3:
		printUsage()

	elif sys.argv[1] == 'solve':
		grid = puzzle.parsePuzzleFile( sys.argv[2] )
		#print grid
		startTime = time.time()
		grid = csp.solve(grid)
		endTime = time.time()
		print grid
		print 'Solved in {} seconds with {} backtracks'.format(round(endTime - startTime, 3), grid.fails)

	elif sys.argv[1] == 'generate':
		grid = puzzle.generatePuzzle(int(sys.argv[2]))
		print grid


def printUsage():
		print \
'''Stevoku - A sudoku generator/solver
Usage:
   stevoku.py solve <puzzle file>
   stevoku.py generate <size: 4,9,16,25,36,49,64>
'''

if __name__ == '__main__':
	main()
