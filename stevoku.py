#!/bin/env python

import sys
import time
import colorama

import puzzle
import csp

def main():

	colorama.init()

	grid = puzzle.parsePuzzleFile( sys.argv[1] )
	print grid
	startTime = time.time()
	grid = csp.solve(grid)
	endTime = time.time()
	print grid
	print 'Solved in', round(endTime - startTime, 3), 'seconds'

if __name__ == '__main__':
	main()
