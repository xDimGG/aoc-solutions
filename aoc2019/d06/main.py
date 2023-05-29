import functools

parents = {}

for line in open('./input.txt').readlines():
	a, b = line.rstrip().split(')')
	parents[b] = a

@functools.cache
def count(k):
	if k not in parents:
		return 0

	return 1 + count(parents[k])

total = 0

for k in parents.keys():
	total += count(k)

print(total)

def ancestors(k):
	if k not in parents:
		return []

	return [parents[k]] + ancestors(parents[k])

you = ancestors('YOU')
san = ancestors('SAN')

for first in you:
	if first in san:
		break

print(you.index(first) + san.index(first))
