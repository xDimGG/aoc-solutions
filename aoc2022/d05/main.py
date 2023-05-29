import parse

r = open('./input.txt').read()
l = list(map(lambda x: x, r.splitlines()))


parts = r.split('\n\n')

groups = [[] for x in range(9)]

for line in parts[0].split('\n'):
	for i, c in enumerate(line):
		if c.isalpha():
			groups[(i - 1) // 4] += [c]

for line in parts[1].split('\n'):
	a, b, c = parse.search('move {:d} from {:d} to {:d}', line)
	
	b -= 1
	c -= 1
	# Part 1 part 2
	# for el in groups[b][:a]:
	for el in reversed(groups[b][:a]):
		groups[c].insert(0, el)
	del groups[b][:a]

print(''.join(map(lambda x: x[0] if len(x) > 0 else '', groups)))

# raw, instr = r.split('\n\n')

# groups = [[] for x in range(9)]

# for line in raw.split('\n'):
# 	for i, c in enumerate(line):
# 		if c.isalpha():
# 			groups[(i - 1) // 4] += [c]

# for line in instr.split('\n'):
# 	a, b, c = parse.search('move {:d} from {:d} to {:d}', line)

# 	b -= 1
# 	c -= 1
# 	rem = groups[b][:a]
# 	del groups[b][:a]
# 	for el in rem:
# 		groups[c].insert(0, el)

# print(''.join(map(lambda x: x[0] if len(x) > 0 else '', groups)))
