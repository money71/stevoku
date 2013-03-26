'''puzzle.py

Parse sudoku files and store in an inferrable format
'''
import sys
from math import sqrt
from collections import deque
import prettyprint as pp

supportedAlphabets = {
	 4: '1234',
	 9: '123456789',
	16: '0123456789abcdef',
	25: 'abcdefghijklmnopqrstuvwxy',
	36: 'abcdefghijklmnopqrstuvwxyz0123456789',
	49: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw',
	64: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
}

class Cell:
	'''Used to store a single cell in the sudoku grid'''

	def __init__(self, base = 9, value = None, given = False):

		self.row = None
		self.column = None
		self.block = None

		self.domain = set()
		self.value = value
		self.base = base
		self.given = given

	def __str__(self):

		if self.value != None:
			if self.given:
				return pp.format( supportedAlphabets[self.base][self.value], pp.BOLD )
			else:
				return supportedAlphabets[self.base][self.value]
		elif len(self.domain) == 1:
			val = list(self.domain)[0]
			return pp.format( supportedAlphabets[self.base][val], pp.TEXT_GREEN )
		else:
			#return pp.format( str(len(self.domain)), pp.TEXT_RED )
			return '.'


class Grid:
	'''Stores the overall grid arrangement as sets'''

	def __init__(self, base = 9):

		self.base = base
		self.rows = [set() for i in range(base)]
		self.columns = [set() for i in range(base)]
		self.blocks = [set() for i in range(base)]
		self.dirtyCells = deque()

	
	def blockAt(self, x, y):

		blockBase = int(sqrt(self.base))
		blockX = int(x/blockBase)
		blockY = int(y/blockBase)

		if x < self.base and y < self.base:
			return self.blocks[blockBase*blockY + blockX]
		else:
			raise IndexError('Coordinates out of range')


	def cellAt(self, x, y):
	
		intersect = self.columns[x].intersection(self.rows[y])
		if len(intersect) != 0:
			return list(intersect)[0]
		else:
			return None


	def insertCellAt(self, cell, x, y):

		block = self.blockAt(x,y)
		if cell not in self.columns[x] and cell not in self.rows[y] and cell not in block:

			self.columns[x].add(cell)
			self.rows[y].add(cell)
			block.add(cell)
			
			cell.row = self.rows[y]
			cell.column = self.columns[x]
			cell.block = block

			self.dirtyCells.append(cell)


	def unsolvedCells(self):

		totalSet = set()
		solvedSet = set()
		for s in self.rows:
			totalSet |= s
			for c in s:
				if c.value != None:
					solvedSet.add(c)

		return totalSet - solvedSet


#	def dumpDomains(self):
#		'''Take a snapshot of the cell domains for backtracking purposes'''
#		
#		ret = []
#		for row in range(self.base):
#			ret.append([])
#			for col in range(self.base):
#				cell = self.cellAt(col,row)
#				if cell.value != None:
#					ret[row].append(cell.value)
#				else:
#					ret[row].append(list(cell.domain))
#
#		return ret
					

	def __str__(self):

		ret = ''
		blockBase = int(sqrt(self.base))
		for row in range(self.base):
			if row != 0 and row % blockBase == 0:
				div = ('---'*blockBase+'-+-')*blockBase+'\n'
				ret += div[:-4]+'\n'
			for col in range(self.base):
				if col != 0 and col % blockBase == 0:
					ret += ' | '
				ret += ' {} '.format(self.cellAt(row, col))
			ret += '\n'
		return ret

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

		raise SyntaxError('Puzzle not of proper dimensions')

	else:
		base = int(base)

	if base not in supportedAlphabets:
		raise IndexError('{} is not a supported base'.format(base))

	# start reading in numbers
	grid = Grid(base)
	blockBase = int(sqrt(base))
	dividers = '|-+'
	divFlag = False

	ri,ci = 0,0
	for row in input:
		ci = 0
		for focus in row:

			# check for dividers, but don't store them
			if focus in dividers:
				if ri % blockBase == 0 or ci % blockBase == 0:
					divFlag = True
					continue
				else:
					raise SyntaxError('Unexpected divider near ({},{})'.format(ri,ci))

			divFlag = False
			if focus != ' ':

				# read the cell value if provided in the correct radix
				value = supportedAlphabets[base].find(focus)
				if value == -1:
					raise ValueError('Value {} at ({},{}) is not a valid base-{} character'.format(focus, ri,ci, base))
				newCell = Cell(base, value, given=True)
				newCell.domain = set([value])
				grid.insertCellAt( newCell, ri, ci )

			else:

				# fill in a blank cell
				newCell = Cell(base)
				newCell.domain = set(range(base))
				grid.insertCellAt( newCell, ri, ci )
				

			ci = ci+1

		if not divFlag:
			ri = ri+1

	return grid

