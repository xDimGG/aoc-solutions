from collections import defaultdict
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

def greedy(remaining, current, minutes):
	best = None
	for r in remaining:
		# Cannot be reached, enabled, and utilized in remaining time
		if (dist[current][r] + 1) >= minutes:
			continue

		if best is None:
			best = r
			continue

		# Simple rate/dist heuristic
		if rates[r] / dist[current][r] > rates[best] / dist[current][best]:
			best = r

	if best is None:
		return 0

	remaining.remove(best)
	travel_time = 1 if current is None else dist[current][best]
	minutes_after_release = minutes - (travel_time + 1)
	print(best, rates[best], minutes_after_release)

	return minutes_after_release * rates[best] + greedy(remaining, best, minutes_after_release)

def exec(queue, current, minutes):
	if len(queue) == 0:
		return 0

	valve = queue[0]
	travel_time = 1 if current is None else dist[current][valve]
	minutes_after_release = minutes - (travel_time + 1)
	if minutes_after_release <= 0:
		return 0

	return minutes_after_release * rates[valve] + exec(queue[1:], valve, minutes_after_release)

print([k for k, v in rates.items() if v > 10])
first = [k for k, v in rates.items() if v >= 10]
items = [k for k, v in rates.items() if v > 0]
print(items)
best = 0

for p in itertools.permutations(first, r=3):
	for q in itertools.permutations([i for i in items if i not in p], r=4):
		released = exec(p + q, 'AA', 30)
		if released > best:
			best = released
			print(p + q, best)

# sol = exec([k for k, v in rates.items() if v > 0], 'AA', 30)

# items = [k for k, v in rates.items() if v > 0]
# first = [k for k, v in rates.items() if v >= 10]

# best = 0
# cache = {}

# for i in itertools.permutations(first, r=4):
# 	for j in itertools.permutations([item for item in items if item not in i], r=8):
# 		p = i[:2] + j[:4]
# 		q = i[2:] + j[4:]
# 		if p not in cache:
# 			cache[p] = exec(p, 'AA', 26)
# 		if q not in cache:
# 			cache[q] = exec(q, 'AA', 26)
# 		released = cache[p] + cache[q]
# 		if released > best:
# 			best = released
# 			print(best)
# 			print(p, q)
		# for q in itertools.permutations([i for i in items if i not in p], r=6):
		# 	released = exec(p, 'AA', 26) + exec(q, 'AA', 26)
		# 	if released > best:
		# 		best = released
		# 		print(best)
		# 		print(p, q)
