from collections import defaultdict
from parse import search
import numpy as np

raw = open('./input.txt').read()
lines = list(map(lambda x: [int(f) + 1 for f in x.rstrip().split(',')], raw.splitlines()))
SIZE = 24
grid = np.zeros((SIZE, SIZE, SIZE))

for x, y, z in lines:
	grid[z, y, x] = 1

def neighbors(x, y, z):
	coords = [x, y, z]
	for i in range(3):
		coords[i] += 1
		yield tuple(coords)
		coords[i] -= 2
		yield tuple(coords)
		coords[i] += 1

def valid_neighbors(ox, oy, oz):
	for x, y, z in neighbors(ox, oy, oz):
		if 0 <= x < SIZE and 0 <= y < SIZE and 0 <= z < SIZE:
			yield x, y, z

def surface_area(x, y, z):
	q = [(x, y, z)]
	seen = {(x, y, z)}
	total = 0

	while len(q) > 0:
		v = q.pop(0)

		for n in valid_neighbors(*v):
			x, y, z = n
			if grid[z, y, x] == 0:
				total += 1
				continue
			if n not in seen:
				seen.add(n)
				q.append(n)

	return total, seen

outside = set()
inside = set()

def is_border(x, y, z):
	return x == 0 or x == SIZE-1 or y == 0 or y == SIZE-1 or z == 0 or z == SIZE-1

def is_inside(x, y, z):
	global outside, inside

	q = [(x, y, z)]
	seen = {(x, y, z)}

	while len(q) > 0:
		v = q.pop(0)
		if v in outside or is_border(*v):
			outside |= seen
			return False
		if v in inside:
			inside |= seen
			return True

		for n in valid_neighbors(*v):
			x, y, z = n
			if grid[z, y, x] == 1:
				continue
			if n not in seen:
				seen.add(n)
				q.append(n)

	inside |= seen
	return True

def exterior_surface_area(x, y, z):
	q = [(x, y, z)]
	seen = {(x, y, z)}
	total = 0

	while len(q) > 0:
		v = q.pop(0)

		for n in valid_neighbors(*v):
			x, y, z = n
			if grid[z, y, x] == 0:
				if not is_inside(x, y, z):
					total += 1
				continue
			if n not in seen:
				seen.add(n)
				q.append(n)

	return total, seen

all_seen = set()
areas = 0
p2 = 0

for x, y, z in lines:
	if (x, y, z) in all_seen:
		continue

	area, seen = surface_area(x, y, z)
	all_seen |= seen
	areas += area
	ext, _ = exterior_surface_area(x, y, z)
	p2 += ext

print(areas)
print(p2)
