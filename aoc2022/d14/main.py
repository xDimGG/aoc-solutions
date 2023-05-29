import math
import numpy as np
np.set_printoptions(linewidth=500)

raw = open('./input.txt').read()
lines = list(map(lambda x: [list(map(int, p.split(','))) for p in x.rstrip().split(' -> ')], raw.splitlines()))

min_x, max_x = 500, 500
max_y = 0

for line in lines:
	for x, y in line:
		min_x = min(min_x, x)
		max_x = max(max_x, x)
		max_y = max(max_y, y)

max_y += 3
min_x -= max_y

for line in lines:
	for coords in line:
		coords[0] -= min_x

grid = np.zeros((max_y, max_y * 2))
sand_x = 500 - min_x

EMPTY = 0
WALL = 1
SAND = 2

for line in lines:
	for p1, p2 in zip(line, line[1:]):
		x, y = min(p1[0], p2[0]), min(p1[1], p2[1])
		x_target, y_target = max(p1[0], p2[0]), max(p1[1], p2[1])
		dx = 1 if p1[0] != p2[0] else 0
		dy = 1 if p1[1] != p2[1] else 0
		while x != x_target or y != y_target:
			grid[y, x] = WALL
			x += dx
			y += dy
		grid[y, x] = WALL

grid[-1, :] = WALL

x0 = max_y - 2
x1 = max_x - min_x + 2
grid[:, [x0, x1]] = WALL

x0 = max_y - abs(x0 - sand_x) - 1
x1 = max_y - (x1 - sand_x) - 1

found_p1 = False

q = [(sand_x, 0)]

for i in range(0, 99999999):
	if grid[0, sand_x] == SAND:
		# print(x0, x1)
		print(i + (x0 * (x0 + 1) // 2) + (x1 * (x1 + 1) // 2))
		break

	x, y = q[-1]
	while True:
		if grid[y + 1, x] == EMPTY:
			y += 1
		elif grid[y + 1, x - 1] == EMPTY:
			x -= 1
			y += 1
		elif grid[y + 1, x + 1] == EMPTY:
			x += 1
			y += 1
		else:
			x, y = q.pop()
			break
		q.append((x, y))

	if not found_p1 and y > max_y-3:
		found_p1 = True
		print(i)

	grid[y, x] = SAND

# for row in grid:
# 	s = ''
# 	for el in row:
# 		if el == EMPTY:
# 			s += '.'
# 		if el == WALL:
# 			s += '#'
# 		if el == SAND:
# 			s += 'o'
# 	print(s)
