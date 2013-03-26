'''csp.py

Contains the constraint satisfaction algorithms to actually solve the sudoku
'''
import copy

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


def solve(grid):
	'''Returns the solved version of grid, or None if no solution'''

	fixArcConsistency(grid)
	return _recSolve(grid)

	
def _recSolve(grid):

	remainingCells = grid.unsolvedCells()

	# pick most constrained cell
	if len(remainingCells) == 0:
		return grid
	else:
		cell = min(remainingCells, key = lambda c: len(c.domain))

	# if there are no possible solutions, fail
	if len(cell.domain) == 0:
		return None

	# for each possible value of the most constrained cell
	origDomain = cell.domain
	for testVal in origDomain:
		
		# make a guess and rebalance
		cell.value = testVal
		cell.domain = set([testVal])
		grid.dirtyCells.append(cell)
		diff = fixArcConsistency(grid)

		# explore possibilities
		consequence = _recSolve(grid)

		# if a solution is found return it!
		if consequence != None:
			return consequence

		# otherwise roll back domain changes and guess again
		else:
			unfixArcConsistency(diff)

	# if we have tried every possibility for the cell with no viable solutions
	# undo all picks and return failure
	cell.value = None
	cell.domain = origDomain
	return None

