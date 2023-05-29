import numpy as np

r = open('./input.txt').read()
trees = np.array(list(map(lambda x: [int(z) for z in x], r.splitlines()))).T

dirs = [
	((0, 0), (1, 0), (0, 1)),
	((len(trees[0]) - 1, 0), (-1, 0), (0, 1)),
	((0, 0), (0, 1), (1, 0)),
	((0, len(trees) - 1), (0, -1), (1, 0)),
]

visible = set()

def is_valid(coord):
	if coord[0] < 0 or coord[1] < 0:
		return False
	try:
		trees[coord]
		return True
	except:
		return False

for origin, search, shift in dirs:
	cur = origin
	last = None
	while is_valid(cur):
		if last is None or trees[cur] > last:
			visible.add(cur)
			last = trees[cur]

		cur = tuple(map(sum, zip(cur, search)))

		if last == 9 or not is_valid(cur):
			origin = tuple(map(sum, zip(origin, shift)))
			cur = origin
			last = None

print(len(visible))

best = 0

for coord, val in np.ndenumerate(trees):
	total = 1
	for _, dir, _ in dirs:
		cur = coord
		score = 0
		while True:
			cur = tuple(map(sum, zip(cur, dir)))
			if is_valid(cur):
				score += 1
				if trees[cur] >= val:
					break
			else:
				break

		total *= score

	best = max(total, best)
	
print(best)
