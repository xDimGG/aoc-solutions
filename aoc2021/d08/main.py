from collections import Counter, defaultdict

lines = []

for line in open('./input.txt').readlines():
	a, b = line.rstrip().split(' | ')
	lines += [(a.split(' '), b.split(' '))]

p1 = 0

for a, b in lines:
	c = Counter(map(len, b))
	p1 += c[2] + c[3] + c[4] + c[7]

print(p1)

digits = [
	0b1110111,
	0b0010010,
	0b1011101,
	0b1011011,
	0b0111010,
	0b1101011,
	0b1101111,
	0b1010010,
	0b1111111,
	0b1111011,
]

def decode(hints):
	acc = defaultdict(list)
	for hint in hints:
		acc[len(hint)] += [set(hint)]

	acf = acc[3][0]
	a = acf - acc[2][0]
	cf = acf - a
	bd = acc[4][0] - acf
	eg = acc[7][0] - acf - bd

	for three in acc[5]:
		if acf.issubset(three):
			break

	dg = three - acf
	d = dg & bd
	b = bd - d
	g = dg & eg	
	e = eg - g

	adeg = a | d | e | g
	for two in acc[5]:
		if adeg.issubset(two):
			break

	c = two - adeg
	f = cf - c

	return [*map(lambda x: x.pop(), [a, b, c, d, e, f, g])]

def convert(seq, encoded):
	code = 0
	for c in encoded:
		code |= (1 << (6 - seq.index(c)))

	return digits.index(code)

p2 = 0

for a, b in lines:
	seq = decode(a)
	num = int(''.join([str(convert(seq, e)) for e in b]))
	p2 += num

print(p2)
