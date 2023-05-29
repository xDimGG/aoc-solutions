from collections import defaultdict
import numpy as np

paths = [[(c[0], int(c[1:])) for c in x.split(',')] for x in open('./input.txt').readlines()]

def points(path):
	delta = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

	x, y = 0, 0
	yield x, y

	for dir, mag in path:
		for _ in range(mag):
			dx, dy = delta[dir]
			x += dx
			y += dy
			yield x, y


point_map = defaultdict(int)
best_man_dist = np.inf
intersects = []

for path in paths:
	for p in points(path):
		point_map[p] += 1

		if point_map[p] == 2 and p != (0, 0):
			intersects += [p]
			x, y = p
			best_man_dist = min(best_man_dist, abs(x) + abs(y))

print(best_man_dist)

best_wire_dist = np.inf

for intersect in intersects:
	wire_dist_sum = 0

	for path in paths:
		wire_dist = -1

		for p in points(path):
			wire_dist += 1
			if p == intersect:
				break

		wire_dist_sum += wire_dist

		# optimization to avoid extra checks
		if wire_dist_sum > best_wire_dist:
			break

	best_wire_dist = min(best_wire_dist, wire_dist_sum)

print(best_wire_dist)
