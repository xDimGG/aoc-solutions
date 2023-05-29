import parse

class Interval():
	def __init__(self, a, b):
		if a < b:
			self.left = a
			self.right = b
		else:
			self.left = b
			self.right = a

	def __str__(self):
		return str((self.left, self.right))

	def __eq__(self, other):
		return self.left == other.left and self.right == other.right

	@property
	def length(self):
		return self.right - self.left

	def union(self, other):
		# either a starts before b or they start at the same point
		a = self if self.left <= other.left else other
		b = other if a is self else self

		if b.left >= a.right:
			return None

		return Interval(b.left, min(a.right, b.right))

class Rectangle():
	def __init__(self, xa, xb, ya, yb):
		self.x = Interval(xa, xb)
		self.y = Interval(ya, yb)

	def __str__(self):
		return f'{self.x.left},{self.y.left} -> {self.x.right},{self.y.right}'

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	@property
	def area(self):
		return self.x.length * self.y.length

	def union(self, other):
		x = self.x.union(other.x)
		y = self.y.union(other.y)
		if x is None or y is None:
			return None

		return Rectangle(x.left, x.right, y.left, y.right)

rects = []
for l in open('./input.txt').readlines():
	xa, ya, xb, yb = parse.search('{:d},{:d} -> {:d},{:d}', l)
	r = Rectangle(xa, xb, ya, yb)
	r.x.right += 1
	r.y.right += 1
	rects += [r]

# lines = [r for r in rects if r.x.length == 1 or r.y.length == 1]
lines = rects
# No intersects, single intersects, double intersects, triple intersects, etc.
# Useful for total area
# unions = [{(i,): l for i, l in enumerate(lines)}]

# Useful for area of intersections
single_unions = {}
for i, line_a in enumerate(lines):
	for line_b in lines[i+1:]:
		u = line_a.union(line_b)
		if u is not None:
			single_unions[(len(single_unions),)] = u

unions = [single_unions]

while len(unions) < 10:
	new_unions = {}

	for indices_a, line_a in unions[0].items():
		for indices_b, line_b in unions[-1].items():
			if indices_a[0] in indices_b:
				continue

			k = tuple(sorted([*indices_a, *indices_b]))
			if k in new_unions:
				continue

			ol = line_b.union(line_a)
			if ol is not None:
				new_unions[k] = ol

	if len(new_unions) == 0:
		break

	unions += [new_unions]
	print([*map(len, unions)])

area = 0

for i, count in enumerate(unions):
	for components, rect in count.items():
		a = rect.area
		if i % 2 == 1:
			a = -a
		area += a

print(area)

# for i, a in enumerate(lines):
# 	for b in lines[i + 1:]:
# 		print(a, b)
# 		o = a.union(b)
# 		if o is None:
# 			continue
# 		print(0 if o is None else o.length)
