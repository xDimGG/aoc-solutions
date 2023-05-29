import numpy as np

raw = open('./input.txt').read()
lines = list(map(lambda x: [list(map(int, p.split(','))) for p in x.rstrip().split(' -> ')], raw.splitlines()))

min_x, max_x = 500, 500
max_y = 0

for line in lines:
	for x, y in line:
		min_x = min(min_x, x)
		max_x = max(max_x, x)
		max_y = max(max_y, y)

for line in lines:
	for coords in line:
		coords[0] -= min_x
		coords[0] += 2

grid = np.zeros((max_y + 3, max_x - min_x + 2 + 2 + 1))

EMPTY = 0
WALL = 1
SAND = 2

for line in lines:
	for p1, p2 in zip(line, line[1:]):
		xs, ys = min(p1[0], p2[0]), min(p1[1], p2[1])
		xt, yt = max(p1[0], p2[0]), max(p1[1], p2[1])
		grid[ys:yt+1, xs:xt+1] = WALL

grid[-1, :] = WALL
grid[:, [0, -1]] = WALL

found_p1 = False

q = [(500 - min_x + 2, 0)]

for i in range(0, 99999999):
	if len(q) == 0:
		x0 = max_y - (500 - min_x)
		x1 = max_y - (max_x - 500)
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

	if not found_p1 and y > max_y:
		found_p1 = True
		print(i)

	grid[y, x] = SAND
