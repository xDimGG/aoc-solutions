import numpy as np
import parse

straight_lines = []
diagonal_lines = []

for l in open('./input.txt').readlines():
	xa, ya, xb, yb = parse.search('{:d},{:d} -> {:d},{:d}', l)
	el = (xa, ya), (xb, yb)
	if yb == ya or xb == xa:
		straight_lines += [el]
	else:
		diagonal_lines += [el]

lines = [*straight_lines, *diagonal_lines]
max_x = max([max(l[0][0], l[1][0]) for l in lines])
max_y = max([max(l[0][1], l[1][1]) for l in lines])

grid = np.zeros((max_y + 1, max_x + 1))

for (xa, ya), (xb, yb) in straight_lines:
	grid[min(ya, yb):max(ya, yb) + 1, min(xa, xb):max(xa, xb) + 1] += 1

print((grid > 1).sum())

for (xa, ya), (xb, yb) in diagonal_lines:
	x = min(xa, xb)
	x_end = max(xa, xb)
	y = ya if x == xa else yb
	# Do we go down or up
	dy = 1 if y < max(ya, yb) else -1

	while x <= x_end:
		grid[y, x] += 1
		# Always go right
		x += 1
		y += dy

print((grid > 1).sum())
