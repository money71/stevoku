#!/bin/env python

import sys
import puzzle
import csp

def main():

	grid = puzzle.parsePuzzleFile( sys.argv[1] )
	print grid
	grid = csp.solve(grid)
	print grid

if __name__ == '__main__':
	main()
