from z3 import *

s = Solver()

for line in open('./input.txt').readlines():
	l, r = line.rstrip().split(': ')
	if l == 'humn':
		continue

	if r.isdigit():
		r = int(r)
	else:
		a, op, b = r.split(' ')
		a = Int(a)
		b = Int(b)
		if l == 'root':
			s.add(a == b)
			continue

		r = eval(f'a {op} b')

	s.add(Int(l) == r)

# s.add(Int('root') == 1)
assert s.check() == sat

print(s.model()[Int('humn')])
