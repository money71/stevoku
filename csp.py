'''csp.py

Contains the constraint satisfaction algorithms to actually solve the sudoku
'''

def checkArcConsistency(grid):

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
					if cell not in grid.dirtyCells:
						grid.dirtyCells.append(cell)
