from collections import defaultdict
import numpy as np

grid = np.array([list(map(int, [*line.rstrip()])) for line in open('./input.txt').readlines()])

def d(G, current, neighbor):
	return G[neighbor]

def h(G, current, goal):
	return abs(goal[0] - current[0]) + abs(goal[1] - current[1])

def neighbors(G, current):
	for x in [(0, 1), (1, 0)]:
		n = tuple(map(sum, zip(current, x)))
		if n[0] < G.shape[0] and n[1] < G.shape[1]:
			yield n

def reconstruct_path(cameFrom, end):
	path = [end]
	while path[-1] in cameFrom:
		path.append(cameFrom[path[-1]])
	return path[::-1]

def inf():
	return np.inf

def A_star(G, start, goal):
	openSet = {start}

	cameFrom = {}

	gScore = defaultdict(inf)
	gScore[start] = 0

	fScore = defaultdict(inf)
	fScore[start] = h(G, start, goal)

	while len(openSet) > 0:
		current = None
		for node in openSet:
			if current is None or fScore[node] < fScore[current]:
				current = node

		if current == goal:
			return reconstruct_path(cameFrom, current)

		openSet.remove(current)
		for neighbor in neighbors(G, current):
			tentative_gScore = gScore[current] + d(G, current, neighbor)
			if tentative_gScore < gScore[neighbor]:
				cameFrom[neighbor] = current
				gScore[neighbor] = tentative_gScore
				fScore[neighbor] = tentative_gScore + h(G, neighbor, goal)
				if neighbor not in openSet:
					openSet.add(neighbor)

	return []

path = A_star(grid, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1))
print(sum(map(lambda x: grid[x], path[1:])))