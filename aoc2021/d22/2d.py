from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class Range():
	def __init__(self, left, right):
		if left > right:
			left, right = right, left
		self.left = left
		self.right = right

	def __str__(self) -> str:
		return f'({self.left}, {self.right})'

	@property
	def a(self):
		return self.left

	@property
	def b(self):
		return self.right

	def overlaps(self, other):
		return self.left < other.right and other.left < self.right

class Cuboid():
	def __init__(self, on, x_start, x_end, y_start, y_end):
		self.on = on
		self.x = Range(x_start, x_end)
		self.y = Range(y_start, y_end)
		self.covers = []
		self.attributes = []

	@property
	def area(self):
		return (self.x.b - self.x.a) * (self.y.b - self.y.a)

	def overlaps(self, other):
		return self.x.overlaps(other.x) and self.y.overlaps(other.y)

def divide_cuboids(cs):
	xs, ys = set(), set()
	for c in cs:
		xs.add(c.x.a)
		xs.add(c.x.b)
		ys.add(c.y.a)
		ys.add(c.y.b)

	xs, ys = sorted([*xs]), sorted([*ys])
	cuboids = []

	for (xa, xb) in zip(xs[:-1], xs[1:]):
		for (ya, yb) in zip(ys[:-1], ys[1:]):
			subsect = Cuboid(False, xa, xb, ya, yb)
			print('Subsect', subsect.x, subsect.y)
			for i, c in enumerate(cs):
				print(c.x, c.y, subsect.overlaps(c))
				if subsect.overlaps(c):
					subsect.attributes += [i]
					subsect.on = c.on

			if len(subsect.attributes) > 0:
				cuboids += [subsect]
			else:
				print('empty subsection')

	return cuboids

cuboids = [
	Cuboid(True, -20, 27, -36, 18),
	Cuboid(True, -20, 34, -21, 24),
	Cuboid(True, -22, 29, -29, 24),
]

def draw(cuboids):
	fig, ax = plt.subplots()
	fig.set_size_inches(8, 8)
	ax.set_xbound(-50, 50)
	ax.set_ybound(-50, 50)

	cols = [
		'#ff0000cc',
		'#ffff00cc',
		'#0000ffcc',
	]

	for i, c in enumerate(cuboids):
		ax.add_patch(
			Rectangle((c.x.a, c.y.a), c.x.b - c.x.a, c.y.b - c.y.a, fc=cols[i % len(cols)]))

	for c in cuboids:
		ax.add_patch(
			Rectangle((c.x.a, c.y.a), c.x.b - c.x.a, c.y.b - c.y.a, fc='none', edgecolor='black'))

	plt.show()

draw(cuboids)

for i in range(len(cuboids) - 1, -1, -1):
	for other in cuboids[:i]:
		if other.overlaps(cuboids[i]):
			other.covers += [cuboids[i]]

total = 0

for c in cuboids:
	div = divide_cuboids([c, *c.covers])
	draw(div)

	for sub in div:
		if sub.attributes == [0]:
			total += sub.area

print(total)
