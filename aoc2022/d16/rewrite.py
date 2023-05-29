import itertools
import math

edges = {}
rates = {}

for line in open('./input.txt').readlines():
	a, b = line.rstrip().split('; ')
	source = a[6:8]
	rates[source] = int(a[23:])
	edges[source] = b[22:].lstrip().split(', ')

# Floyd-Warshall algorithm
dist = {k: {i: math.inf for i in edges.keys()} for k in edges.keys()}

for source, dests in edges.items():
	for dest in dests:
		dist[source][dest] = 1

	dist[source][source] = 0

for k in dist.keys():
	for i in dist.keys():
		for j in dist.keys():
			if dist[i][j] > dist[i][k] + dist[k][j]:
				dist[i][j] = dist[i][k] + dist[k][j]

def visit(valve, remaining, current, time, score):
	travel_time = 1 if current is None else dist[current][valve]
	minutes_after_release = time - (travel_time + 1)
	if minutes_after_release <= 0:
		return None

	return remaining - {valve}, valve, minutes_after_release, score + minutes_after_release * rates[valve]

# state: (remaining, current, time, score)
# maps state to best score
best_scores = {}

def dfs(state):
	global best_scores, c
	local_best = state[3]

	for valve in state[0]:
		next_state = visit(valve, *state)
		if next_state == None:
			continue

		k = tuple(next_state[0]) + (next_state[1], next_state[2])
		if k in best_scores:
			if best_scores[k] > next_state[3]:
				continue

		best_scores[k] = next_state[3]
		local_best = max(dfs(next_state), local_best)

	return local_best

positive_valves = set(k for k, v in rates.items() if v > 0)
print(dfs((positive_valves, 'AA', 30, 0)))

best = 0

for c in itertools.combinations(positive_valves, len(positive_valves) // 2):
	best_a = dfs((set(c), 'AA', 26, 0))
	best_b = dfs((positive_valves - set(c), 'AA', 26, 0))
	best = max(best_a + best_b, best)

print(best)