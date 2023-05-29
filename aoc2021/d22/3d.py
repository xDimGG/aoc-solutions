from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class Range():
	def __init__(self, a, b):
		if a > b:
			a, b = b, a
		self.a = a
		self.b = b
	
	def overlaps(self, other):
		return (self.a >= other.a and self.a < other.b) or (self.b <= other.b and self.b > other.b)

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
		return (self.x.b - self.x.a) * (self.y.b - self.y.a) * (self.z.b - self.z.a)

	def overlaps(self, other):
		return self.x.overlaps(other.x) and self.y.overlaps(other.y) and self.z.overlaps(other.z)

def divide_cuboids(cs):
	xs, ys, zs = set(), set(), set()
	for c in cs:
		xs.add(c.x.a)
		xs.add(c.x.b)
		ys.add(c.y.a)
		ys.add(c.y.b)
		zs.add(c.z.a)
		zs.add(c.z.b)

	xs, ys, zs = [*xs], [*ys], [*zs]
	cuboids = []

	for (xa, xb) in zip(xs[:-1], xs[1:]):
		for (ya, yb) in zip(ys[:-1], ys[1:]):
			for (za, zb) in zip(zs[:-1], zs[1:]):
				subsect = Cuboid(False, xa, xb, ya, yb, za, zb)
				for i, c in enumerate(cs):
					if subsect.overlaps(c):
						subsect.attributes += [i]
						subsect.on = c.on

				if len(subsect.attributes) > 0:
					cuboids += [subsect]

	return cuboids

cuboids = [
	Cuboid(True, 1, 6 + 1, 1, 6 + 1, 1, 6 + 1),
	Cuboid(False, 1, 3 + 1, 1, 3 + 1, 1, 3 + 1),
	Cuboid(False, 2, 4 + 1, 2, 4 + 1, 2, 4 + 1),
	Cuboid(False, 4, 6 + 1, 4, 6 + 1, 4, 6 + 1),
]

for i in range(len(cuboids) - 1, -1, -1):
	for other in cuboids[:i]:
		if other.overlaps(cuboids[i]):
			other.covers += [cuboids[i]]

total = 0

for target in range(len(cuboids)):
	if not cuboids[target].on:
		continue
	for sub in divide_cuboids(cuboids):
		if sub.attributes == [target]:
			total += sub.area

print(total)
