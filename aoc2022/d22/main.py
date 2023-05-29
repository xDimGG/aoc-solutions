import re

grid, path = open('./input.txt').read().split('\n\n')
grid = grid.splitlines()
path = re.findall(r'\d+|[LR]', path)

# dx, dy definitions
forward = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1),
]
VERTICAL = [1, 3]

# Inclusive bounds
x_bounds = []
y_bounds = []

for row in grid:
	for i, char in enumerate(row):
		if char != ' ':
			x_bounds.append((i, len(row) - 1))
			break

for x in range(max(len(row) for row in grid)):
	start, end = None, None
	for y in range(len(grid)):
		if len(grid[y]) <= x or grid[y][x] == ' ':
			continue
		if start is None:
			start = y
		end = y
	y_bounds.append((start, end))

# Right: 0, Down: 1, Left: 2, Up: 3
direction, x, y = 0, x_bounds[0][0], 0

for move in path:
	if not move.isdigit():
		if move == 'R':
			direction += 1
		else:
			direction -= 1
		direction %= 4
		continue

	dx, dy = forward[direction]

	for i in range(int(move)):
		if direction in VERTICAL:
			bounds = y_bounds[x]
			pos = y + dy
		else:
			bounds = x_bounds[y]
			pos = x + dx

		if pos < bounds[0]:
			pos = bounds[1]
		elif pos > bounds[1]:
			pos = bounds[0]

		if direction in VERTICAL:
			nx, ny = x, pos
		else:
			nx, ny = pos, y

		if grid[ny][nx] == '#':
			break

		x, y = nx, ny

print(1000 * (y + 1) + 4 * (x + 1) + direction)