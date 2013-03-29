'''csp.py

Contains the constraint satisfaction algorithms to actually solve the sudoku
'''
import threading
import multiprocessing
import time
from math import sqrt


def fixArcConsistency(grid):
	'''Check updated cells for consistency and fix if necessary. Returns dict of changes'''

	diff = {}

	# loop until the state is consistent (no more dirty cells)
	while len(grid.dirtyCells) != 0:

		dirty = grid.dirtyCells.popleft()

		# loop over each cell constrained by the dirty cell that is not the dirty cell itself
		for cell in (dirty.row | dirty.column | dirty.block) - set([dirty]):

			# arc consistency of cell -> dirty
			# for all v1 in cell.domain, there exists v2 in dirty.domain such that v1 != v2
			# if not, remove v1 from cell.domain and add cell to dirty list
			for v1 in set(cell.domain):
				if len(dirty.domain-set([v1])) == 0:

					cell.domain.remove(v1)

					# add value to diff list
					if cell not in diff:
						diff[cell] = []
					diff[cell].append(v1)

					if cell not in grid.dirtyCells:
						grid.dirtyCells.append(cell)

	return diff


def unfixArcConsistency(diff):
	'''Reverse the actions taken by a given call to fixArcConsistency'''

	for cell, vals in diff.items():
		cell.domain |= set(vals)


def solve(grid, complete=False):
	'''Returns the solved version of grid, or None if no solution
	If complete is enabled, returns list of all solutions, or [] if none
	'''

	grid.fails = 0
	outputLength = grid.base + int(sqrt(grid.base)) + 1
	#print (outputLength-1)*'\n'
	def printGrid(grid):
		while(True):
			print '\033[{}ACurrent state ({} fails):'.format(outputLength, grid.fails)
			print grid
			time.sleep(3)
	t = threading.Thread(target=printGrid, args=(grid,))
	t.daemon = True
	#t.start()

	fixArcConsistency(grid)
	return _recSolve(grid, complete)

	
def _recSolve(grid, complete=False):

	ret = []
	remainingCells = grid.unsolvedCells()
	#print 'Cells remaining:', len(remainingCells)

	# pick most constrained cell
	if len(remainingCells) == 0:
		#print 'Solution found!'
		if complete:
			return [grid.deepCopy()]
		else:
			return grid.deepCopy()
	else:
		cell = min(remainingCells, key = lambda c: len(c.domain))

	# if there are no possible solutions, fail
	if len(cell.domain) == 0:
		grid.fails += 1
		if complete:
			return []
		else:
			return None

	origDomain = cell.domain

	# find how much each option would change the grid
	expenseList = []
	for testVal in origDomain:
		cell.domain = set([testVal])
		grid.dirtyCells.append(cell)
		diff = fixArcConsistency(grid)
		counter = 0
		for changes in diff.values():
			counter += len(changes)
		expenseList.append((testVal, counter))
		unfixArcConsistency(diff)

	cell.domain = origDomain
	expenseList.sort(key=lambda x: x[1])
	checkList = [x[0] for x in expenseList]
	#checkList = origDomain

	for testVal in checkList:
		
		# make a guess and rebalance
		cell.value = testVal
		cell.domain = set([testVal])
		grid.dirtyCells.append(cell)
		diff = fixArcConsistency(grid)

		# explore possibilities
		consequence = _recSolve(grid, complete)

		# if a solution is found return it!
		if complete:
			ret.extend(consequence)
		elif consequence != None:
			return consequence

		# roll back domain changes and guess again
		unfixArcConsistency(diff)

	# if we have tried every possibility for the cell with no viable solutions
	# undo all picks and return failure
	cell.value = None
	cell.domain = origDomain

	if complete:
		return ret
	else:
		return None

