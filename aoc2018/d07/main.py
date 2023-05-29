import copy
from functools import total_ordering
import heapq
from parse import search

deps = {}

for line in open('./input.txt').readlines():
	a, b = search('Step {} must be finished before step {} can begin.', line)

	if a not in deps:
		deps[a] = set()
	if b not in deps:
		deps[b] = set()

	deps[b] |= {a}

dep_copy = copy.deepcopy(deps)

# Part 1
order = []

while len(deps) > 0:
	candidates = []

	for k, v in deps.items():
		if len(v) == 0:
			candidates += [k]

	choice = min(candidates)
	order += [choice]
	del deps[choice]
	for v in deps.values():
		v -= {choice}

print(''.join(order))

# Part 2
WORKER_COUNT = 5
BASE_RUNTIME = 60
deps = dep_copy
workers = [None] * WORKER_COUNT
elapsed = 0

class Process():
	def __init__(self, task):
		self.task = task
		self.duration = BASE_RUNTIME + (1 + ord(task) - ord('A'))

	def __eq__(self, o):
		return isinstance(o, self.__class__) and self.task == o.task


# Returns list of all completed tasks and mutates all processes
def run():
	global workers, elapsed
	completed = []
	shortest = min([w.duration for w in workers if w is not None])
	elapsed += shortest

	for i, w in enumerate(workers):
		if w is None:
			continue

		w.duration -= shortest
		if w.duration == 0:
			completed += [w.task]
			workers[i] = None

	return completed

while len(deps) > 0:
	tasks = []

	for k, v in deps.items():
		if len(v) == 0 and Process(k) not in workers:
			heapq.heappush(tasks, k)

	for i in range(len(workers)):
		if len(tasks) == 0:
			break

		if workers[i] is None:
			workers[i] = Process(heapq.heappop(tasks))

	completed = set(run())
	for c in completed:
		del deps[c]

	for v in deps.values():
		v -= completed

print(elapsed)
