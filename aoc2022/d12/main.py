from collections import defaultdict
import math

class DiGraph():
	def __init__(self):
		self.edges = defaultdict(set)

	def add_edge(self, src, dst):
		self.edges[src].add(dst)

	def neighbors(self, src):
		return self.edges[src]

	def dijkstra(self, source):
		dist = defaultdict(lambda: math.inf)
		dist[source] = 0
		queue = set(self.edges.keys())

		while len(queue) > 0:
			u = None
			for el in queue:
				if u is None or dist[el] < dist[u]:
					u = el
			queue.remove(u)

			for v in self.neighbors(u):
				if v not in queue:
					continue
				alt = dist[u] + 1
				if alt < dist[v]:
					dist[v] = alt

		return dist

g = DiGraph()

def convert(char):
	if char == 'S':
		return 0
	if char == 'E':
		return 27

	return ord(char) - ord('a') + 1

height_map = [[convert(x) for x in line.rstrip()] for line in open('./input.txt').readlines()]

directions = [
	[1, 0],
	[0, 1],
	[-1, 0],
	[0, -1],
]

g = DiGraph()
reverse_g = DiGraph()

start, end = None, None

for y, row in enumerate(height_map):
	for x, height in enumerate(row):
		if height == 0:
			start = (x, y)
		if height == 27:
			end = (x, y)
		for dx, dy in directions:
			neighbor_x, neighbor_y = (x + dx, y + dy)
			if neighbor_x < 0 or neighbor_x >= len(row):
				continue
			if neighbor_y < 0 or neighbor_y >= len(height_map):
				continue
			neighbor_height = height_map[neighbor_y][neighbor_x]
			if height >= neighbor_height - 1:
				g.add_edge((x, y), (neighbor_x, neighbor_y))
				reverse_g.add_edge((neighbor_x, neighbor_y), (x, y))

assert start is not None
assert end is not None

print(g.dijkstra(start)[end])
print(min([dist for coords, dist in reverse_g.dijkstra(end).items() if height_map[coords[1]][coords[0]] == 1]))
