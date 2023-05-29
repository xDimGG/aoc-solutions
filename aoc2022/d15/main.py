from parse import search

raw = open('./input.txt').read()
lines = list(map(lambda x: x, raw.splitlines()))

# max_x, max_y = 0, 0
sensors = []
# limit = 20
# y = 10
limit=4000000
y=2000000
ignore = set()

for line in lines:
	x0, y0, x1, y1 = search('Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', line)
	if y1 == y:
		ignore.add(x1)
	dist = abs(y1 - y0) + abs(x1 - x0)
	sensors += [[x0, y0, x1, y1, dist]]

points = set()

for x0, y0, x1, y1, dist in sensors:
	dev = dist - abs(y - y0)
	for x in range(x0 - dev, x0 + dev + 1):
		points.add(x)

print(len(points - ignore))

lineqs = []

def out_of_reach(x, y):
	for x0, y0, x1, y1, dist in sensors:
		if abs(x0 - x) + abs(y0 - y) <= dist:
			return False
	return True

for x0, y0, x1, y1, dist in sensors:
	points = [
		(1, x0, y0 - dist),
		(1, x0, y0 + dist),
		(-1, x0 - dist, y0),
		(-1, x0 + dist, y0),
	]
	sensor_lineqs = []
	for m, x0, y0 in points:
		b = (m*-x0)+y0
		sensor_lineqs += [(m, b)]
	lineqs += [sensor_lineqs]

for i, set_a in enumerate(lineqs):
	for set_b in lineqs[i+1:]:
		for m0, b0 in set_a:
			for m1, b1 in set_b:
				d = (m0 - m1)
				if d == 0:
					continue
				x = (b1 - b0) / d
				y = m0 * x + b0
				for dx, dy in [
					(-1, 0),
					(1, 0),
					(0, 1),
					(0, -1)
				]:
					xd, yd = x + dx, y + dy
					if 0 <= xd <= limit and 0 <= yd <= limit and out_of_reach(xd, yd):
						print(int(4000000 * xd + yd))
						exit()
