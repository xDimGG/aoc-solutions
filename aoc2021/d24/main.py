from z3 import *

s = Solver()
instructions = []

i = -1
for line in open('input.txt').readlines():
	instructions += [tuple(line.rstrip().split(' '))]

vars = {'w': [], 'x': [], 'y': [], 'z': []}

def new(var):
	i = Int(f'{var}{len(vars[var])}')
	vars[var] += [i]
	return i

def get(var):
	if len(vars[var]) == 0:
		return new(var)
	return vars[var][-1]

funcs = {
	'add': lambda a, b: a + b,
	'mul': lambda a, b: a * b,
	'div': lambda a, b: a / b,
	'mod': lambda a, b: a % b,
	'eql': lambda a, b: If(a == b, 1, 0),
}

for i, *args in instructions:
	if i == 'inp':
		a = new(args[0])
		s.add(1 <= a, a <= 9)
	else:
		fn = funcs[i]
		a, b = get(args[0]), args[1]
		s.add(new(args[0]) == fn(a, (int(b) if b.lstrip('-').isnumeric() else get(b))))

s.add(get('z') == 0)

def gt(new_digits):
	global s, vars
	ws = vars['w']
	s.add(Or([
		And(*[ws[j] == s for j, s in enumerate(new_digits[:i])], ws[i] > d)
		for i, d in enumerate(new_digits)
	]))

def lt(new_digits):
	global s, vars
	ws = vars['w']
	s.add(Or([
		And(*[ws[j] == s for j, s in enumerate(new_digits[:i])], ws[i] < d)
		for i, d in enumerate(new_digits)
	]))

while s.check() == sat:
	m = s.model()

	serial = [m[digit] for digit in vars['w']]
	print('W =', ''.join(map(str, serial)))
	# p1
	gt(serial)
	# p2
	# lt(serial)
