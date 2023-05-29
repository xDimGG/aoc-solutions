from itertools import product, permutations
from typing import Counter
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 12

f = open('input.txt')
scanners = []
for line in f.readlines():
	if line[0] == '\n':
		pass
	elif line.startswith('---'):
		scanners += [[]]
	else:
		scanners[-1] += [list(map(int, line.split(',')))]

scanners = list(map(np.array, scanners))

def rotations(array):
	if np.ndim(array) == 2:
		for x, y, z in permutations([0, 1, 2]):
			for sx, sy, sz in product([-1, 1], repeat=3):
				rotation_matrix = np.zeros((3, 3))
				rotation_matrix[0, x] = sx
				rotation_matrix[1, y] = sy
				rotation_matrix[2, z] = sz
				if np.linalg.det(rotation_matrix) == 1:
					yield np.array([np.matmul(rotation_matrix, x) for x in array])
	else:
		for x in rotations(np.array([array])):
			yield x[0]

def overlaps(scanner1, scanner2):
	for s2 in rotations(scanner2):
		c = Counter()
		for p2 in s2:
			for p1 in scanner1:
				c[tuple(p1 - p2)] += 1

		diff, count = c.most_common(1)[0]
		if count >= THRESHOLD:
			return np.array(diff), s2

	return None, None

matches = []
normalized = set([0])
queue = [0]
diffs = [np.zeros(3)] + [None] * (len(scanners) - 1)

while len(queue) > 0:
	i = queue.pop()

	for j, other in enumerate(scanners):
		if j in normalized:
			continue

		diff, rotated = overlaps(scanners[i], other)
		if not isinstance(diff, np.ndarray):
			continue

		scanners[j] = rotated + diff
		diffs[j] = diff
		normalized.add(j)
		queue += [j]

unique = set()
for beacons in scanners:
	for beacon in beacons:
		unique.add(tuple(beacon))

print(len(unique))
farthest = 0

for x1, y1, z1 in diffs:
	for x2, y2, z2 in diffs:
		farthest = max(farthest, abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1))

print(int(farthest))
