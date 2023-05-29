r = open('./input.txt').read()
l = list(map(lambda x: [x[:len(x)//2], x[len(x)//2:]], r.splitlines()))

def value(s):
	if s.islower():
		return ord(s) - ord('a') + 1
	else:
		return ord(s) - ord('A') + 27

s = 0

for x in l:
	o = set(x[0]) & set(x[1])
	for c in o:
		s += value(c)

print(s)

g = [[]]

for l in r.splitlines():
	m = g[-1]
	if len(g[-1]) == 3:
		m = []
		g += [m]
	m += [l]

s = 0

for x in g:
	o = set(x[0]) & set(x[1]) & set(x[2])
	for c in o:
		s += value(c)

print(s)
