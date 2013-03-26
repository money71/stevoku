#!/bin/env python

import sys
import puzzle
import csp

def main():

	grid = puzzle.parsePuzzleFile( sys.argv[1] )
	csp.checkArcConsistency(grid)
	print grid

if __name__ == '__main__':
	main()
