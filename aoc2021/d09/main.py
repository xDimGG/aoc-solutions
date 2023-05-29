import heapq


inp = [*map(lambda l: [*map(int, [*l.rstrip()])], open('./input.txt').readlines())]

def s(i, j):
	global inp
	if 0 <= i < len(inp) and 0 <= j < len(inp[i]):
		return inp[i][j]
	return 10


def expand(i, j):
	global inp

	size = 0
	Q = [(i, j)]
	explored = {(i, j)}

	while len(Q) > 0:
		i, j = Q.pop()

		if s(i, j) >= 9:
			continue

		size += 1

		neighbors = [
			(i - 1, j),
			(i + 1, j),
			(i, j - 1),
			(i, j + 1),
		]

		for n in neighbors:
			if n not in explored:
				explored |= {n}
				Q += [n]

	return size

p1 = 0
basins = []

for i, col in enumerate(inp):
	for j, el in enumerate(col):
		if s(i - 1, j) > el and s(i, j - 1) > el and s(i + 1, j) > el and s(i,  j + 1) > el:
			p1 += el + 1
			heapq.heappush(basins, expand(i, j))

print(p1)

p2 = 1

for b in heapq.nlargest(3, basins):
	p2 *= b

print(p2)
