'''puzzle.py

Parse sudoku files and store in an inferrable format
'''
import sys
from math import sqrt
import prettyprint as pp

class Cell:
	'''Used to store a single cell in the sudoku grid'''

	def __init__(self, row, column, block):

		self.row = row
		self.column = column
		self.block = block
		self.domain = []
		self.value = None
		self.given = False

class Grid:
	'''Stores the overall grid arrangement as sets'''

	def __init__(self, base = 10):

		self.base = base
		self.rows = [set() for i in range(base)]
		self.columns = [set() for i in range(base)]
		self.blocks = [set() for i in range(base)]


	def cellAt(self, x, y):
	
		return list(columns[x].intersection(rows[y]))[0]


def parsePuzzleFile( filename ):
	'''Parse a puzzle file into a Grid object

	A properly formatted puzzle file should contain only value characters (in some squared base),
	spaces, and dividers (|-+). The correct base is inferred based on the width/height of the grid.

	For example, a properly formatted base-4 sudoku file might contain this:

		1 | 4
		 4|  
		--+--
		  |  
		41|23
	'''

	input = []
	with open(filename, 'r') as ifp:
		if ifp == None:
			print pp.format('Could not open file: '+filename, pp.RED_TEXT)
			return None

		input = ifp.readlines()
		input = [line[:-1] for line in input]


	# calculate the base, make sure it's valid
	l = len(input)
	base = ((sqrt(5+4*l)-1)/2)**2
	if len(input[0]) != len(input) or int(base) != base:
		print 'Input file improperly formatted!'
		print len(input[0]), 'by', len(input)
		print 'Base:', base
		return None
	else:
		base = int(base)

	print 'Sudoku base:', base


	# start reading in numbers
	blockBase = int(sqrt(base))
	dividers = '|-+'

	for row in range(base):
		for col in range(base):

			

if __name__ == '__main__':
	parsePuzzleFile( sys.argv[1] )
