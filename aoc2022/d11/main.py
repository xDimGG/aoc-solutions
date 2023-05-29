raw = open('./input.txt').read()

monkeys = []

thing = 1

for line in raw.split('\n\n'):
	lines = [x.strip().split(' ') for x in line.split('\n')]
	thing *= int(lines[3][-1])
	monkeys += [{
		'items': list(map(int, (''.join(lines[1][2:])).split(','))),
		'operation': [lines[2][4], lines[2][5]],
		'divisible': int(lines[3][-1]),
		'true': int(lines[4][-1]),
		'false': int(lines[5][-1]),
		'inspect': 0,
	}]

# for round in range(20):
for round in range(10000):
	for m in monkeys:
		items, operation, divisible, true, false = m['items'], m['operation'], m['divisible'], m['true'], m['false']
		for i, old in enumerate(items):
			items[i] = eval(f'old {operation[0]} {operation[1]}') % thing
			# items[i] = eval(f'old {operation[0]} {operation[1]}') // 3
			m['inspect'] += 1
			if (items[i] % divisible) == 0:
				monkeys[true]['items'] += [items[i]]
			else:
				monkeys[false]['items'] += [items[i]]
		m['items'] = []

inspects = sorted([m['inspect'] for m in monkeys], reverse=True)

print(inspects[0] * inspects[1])
