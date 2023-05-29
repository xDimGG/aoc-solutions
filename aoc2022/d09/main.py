raw = open('./input.txt').read()
lines = list(map(lambda x: (x[0], int(x[2:])), raw.splitlines()))

# p1
# points = [[0, 0] for x in range(2)]
# p2
points = [[0, 0] for x in range(10)]

def chase(ax, ay, bx, by):
	if abs(ax - bx) <= 1 and abs(ay - by) <= 1:
		pass
	elif ay == by:
		dx = 1 if bx > ax else -1
		while abs(ax - bx) != 1:
			ax += dx
			yield ax, ay
	elif ax == bx:
		dy = 1 if by > ay else -1
		while abs(ay - by) != 1:
			ay += dy
			yield ax, ay
	else:
		ax += 1 if bx > ax else -1
		ay += 1 if by > ay else -1
		yield ax, ay
		yield from chase(ax, ay, bx, by)

visited = {(0, 0)}

def update(a, b):
	head, tail = points[a], points[b]
	for pos in chase(*tail, *head):
		tail[0], tail[1] = pos
		if b == len(points) - 1:
			visited.add(pos)
		else:
			update(a + 1, b + 1)

for dir, dist in lines:
	if dir == 'U':
		points[0][1] += dist
	if dir == 'D':
		points[0][1] -= dist
	if dir == 'R':
		points[0][0] += dist
	if dir == 'L':
		points[0][0] -= dist

	update(0, 1)

print(len(visited))
