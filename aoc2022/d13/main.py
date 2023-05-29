from functools import cmp_to_key

raw = open('./input.txt').read()

CONTINUE = 'xd'

def compare(a, b):
	if isinstance(a, int) and isinstance(b, int):
		if a == b:
			return CONTINUE
		else:
			return a < b

	elif isinstance(a, list) and isinstance(b, list):
		for x, y in zip(a, b):
			res = compare(x, y)
			if res != CONTINUE:
				return res
		if len(a) == len(b):
			return CONTINUE
		return len(a) < len(b)

	else:
		if isinstance(a, int):
			a = [a]
		if isinstance(b, int):
			b = [b]
		return compare(a, b)

s = 0
p1 = [[2]]
p2 = [[6]]

packets = [
	p1,
	p2
]

for i, pair in enumerate(raw.split('\n\n')):
	lines = pair.split('\n')
	a, b = eval(lines[0]), eval(lines[1])
	correct = compare(a, b)
	packets += [a, b]
	if correct:
		s += i + 1

print(s)

ordered = sorted(packets, key=cmp_to_key(lambda a, b: -1 if compare(a, b) else 1))

print((ordered.index(p1) + 1) * (ordered.index(p2) + 1))
