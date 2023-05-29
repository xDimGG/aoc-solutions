import itertools

directions = itertools.cycle(open('./input.txt').read())

shapes = itertools.cycle([
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
])

ROCKS = 10

WIDTH = 7
field = [[0] * WIDTH for i in range(ROCKS * 2 + 4)]
max_height = 0

def collides(x, y, shape):
	global field
	for dy in range(len(shape)):
		for dx, rock in enumerate(shape[len(shape) - (dy + 1)]):
			if rock == 1 and field[y + dy][x + dx] == 1:
				return True

	return False


for _ in range(ROCKS):
	shape = next(shapes)
	x, y = 2, max_height + 4

	while True:
		if next(directions) == '<':
			new_x = max(0, x - 1)
		else:
			new_x = min(WIDTH - 1 - len(shape[0]), x + 1)
		
		if not collides(new_x, y, shape):
			x = new_x

		if y == 0 or collides(x, y - 1, shape):
			break
		else:
			y -= 1

	max_height = max(max_height, y + len(shape))
	for dy in range(len(shape)):
		for dx, rock in enumerate(shape[len(shape) - (dy + 1)]):
			if rock == 1:
				field[y + dy][x + dx] = 1

print(max_height)