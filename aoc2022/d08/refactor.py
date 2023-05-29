import numpy as np

grid = np.array([list(map(int, line.rstrip())) for line in open('./input.txt').readlines()])

VISIBLE = 1 << 4
visible_count = 0

for _ in range(4):
	for col in grid:
		tallest = -1
		for i, tree in enumerate(col):
			height = tree & ~VISIBLE
			if height > tallest:
				tallest = height
				col[i] |= VISIBLE
				if (tree & VISIBLE) == 0:
					visible_count += 1

	grid = np.rot90(grid)

print(visible_count)
