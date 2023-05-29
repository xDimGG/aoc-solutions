import copy
from parse import search

class Range():
	def __init__(self, left, right):
		if left > right:
			left, right = right, left
		self.left = left
		self.right = right

	def overlaps(self, other):
		return self.left < other.right and other.left < self.right

class Cuboid():
	def __init__(self, on, x_start, x_end, y_start, y_end, z_start, z_end):
		self.on = on
		self.x = Range(x_start, x_end)
		self.y = Range(y_start, y_end)
		self.z = Range(z_start, z_end)
		self.covers = []
		self.attributes = []

	@property
	def area(self):
		return (self.x.right - self.x.left) * (self.y.right - self.y.left) * (self.z.right - self.z.left)

	def overlaps(self, other):
		return self.x.overlaps(other.x) and self.y.overlaps(other.y) and self.z.overlaps(other.z)

def divide_cuboids(cs):
	xs, ys, zs = set(), set(), set()
	for c in cs:
		xs.add(c.x.left)
		xs.add(c.x.right)
		ys.add(c.y.left)
		ys.add(c.y.right)
		zs.add(c.z.left)
		zs.add(c.z.right)

	xs, ys, zs = sorted([*xs]), sorted([*ys]), sorted([*zs])
	subcuboids = []

	for (xa, xb) in zip(xs[:-1], xs[1:]):
		for (ya, yb) in zip(ys[:-1], ys[1:]):
			for (za, zb) in zip(zs[:-1], zs[1:]):
				subsect = Cuboid(None, xa, xb, ya, yb, za, zb)
				for i, c in enumerate(cs):
					if subsect.overlaps(c):
						subsect.attributes += [i]

				if len(subsect.attributes) > 0:
					subcuboids += [subsect]

	return subcuboids

input_cuboids = []
for line in open('./input.txt'):
	state, xa, xb, ya, yb, za, zb = search('{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}', line)
	input_cuboids += [Cuboid(state == 'on', xa, xb + 1, ya, yb + 1, za, zb + 1)]

parts = [copy.deepcopy(input_cuboids[:20]), input_cuboids]
for part, cuboids in enumerate(parts):
	for i in range(len(cuboids) - 1, -1, -1):
		for other in cuboids[:i]:
			if other.overlaps(cuboids[i]):
				other.covers += [cuboids[i]]

	total = 0
	for c in cuboids:
		if not c.on:
			continue

		for sub in divide_cuboids([c, *c.covers]):
			if sub.attributes == [0]:
				total += sub.area

	print(f'Part {part + 1}: {total}')
