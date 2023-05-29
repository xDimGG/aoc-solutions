from parse import search

directions = open('./input.txt').read()

shapes = [
	[[1, 1, 1, 1]],
	[
		[0, 1, 0],
		[1, 1, 1],
		[0, 1, 0],
	],
	[
		[0, 0, 1],
		[0, 0, 1],
		[1, 1, 1]
	],
	[
		[1],
		[1],
		[1],
		[1],
	],
	[
		[1, 1],
		[1, 1],
	],
]

WIDTH = 7
TARGET = 5000000

pit = [[0] * WIDTH for _ in range(TARGET * 4)]

height = 0
j = 0

def collides(pit, shape, x, y):
	if y < 0:
		return True

	for dy, row in enumerate(shape[::-1]):
		for dx, val in enumerate(row):
			if val == 1 and pit[y + dy][x + dx] == 1:
				return True

	return False

cycles = {}
cycle_found = False
GOAL = 1000000000000

i = 0
while True:
	shape = shapes[i % len(shapes)]
	x = 2
	y = height + 3

	if i == 2022:
		print(height)

	while True:
		new_x = x
		if directions[j % len(directions)] == '<':
			new_x = max(x - 1, 0)
		else:
			new_x = min(x + 1, WIDTH - len(shape[0]))
		j += 1
		if new_x != x and not collides(pit, shape, new_x, y):
			x = new_x
		if collides(pit, shape, x, y - 1):
			break
		y -= 1

	for dy, row in enumerate(shape[::-1]):
		for dx, val in enumerate(row):
			if val == 1:
				pit[y + dy][x + dx] = val

	height = max(height, y + len(shape))

	if cycle_found:
		remaining -= 1
		if remaining == 0:
			break
	elif height > 50:
		above = tuple(sum(pit[height-30:height], [i % len(shapes), j % len(directions)]))
		if above in cycles:
			last_height, last_i = cycles[above]
			remaining = GOAL - last_i - 1
			estimate = last_height + (height - last_height) * (remaining // (i - last_i))
			height_at_estimate = height
			remaining %= i - last_i
			cycle_found = True
		else:
			cycles[above] = (height, i)

	i += 1

print(estimate + (height - height_at_estimate))

# for row in pit[::-1]:
# 	s = ''
# 	for val in row:
# 		s += '#' if val else '.'
# 	print(s)

# print(height)
