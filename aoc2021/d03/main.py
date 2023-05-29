g = ''
e = ''

t = []
lines = []

for l in open('./input.txt').readlines():
	l = l.rstrip()
	lines += [l]

	for i, x in enumerate(l):
		if i < len(t):
			t[i] += x
		else:
			t += [x]

for l in t:
	ones = l.count('1')
	zeros = l.count('0')
	if ones > zeros:
		g += '1'
		e += '0'
	else:
		g += '0'
		e += '1'

print(int(g, 2) * int(e, 2))

less = [*lines]
more = lines

i = 0
while len(more) > 1:
	a = [x for x in more if x[i] == '0']
	b = [x for x in more if x[i] == '1']
	more = b if len(b) >= len(a) else a

	i += 1

i = 0
while len(less) > 1:
	a = [x for x in less if x[i] == '1']
	b = [x for x in less if x[i] == '0']
	less = b if len(b) <= len(a) else a

	i += 1

print(int(less[0], 2) * int(more[0], 2))