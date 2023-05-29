raw = open('./input.txt').read()
lines = list(map(lambda x: x.rstrip().split(' '), raw.splitlines()))

cycles = [1] * len(lines) * 2
cycle = 1

for instr in lines:
	if instr[0] == 'noop':
		cycles[cycle + 1] = cycles[cycle]
		cycle += 1
	if instr[0] == 'addx':
		cycles[cycle + 2] = cycles[cycle + 1] = cycles[cycle]
		cycle += 2
		cycles[cycle] += int(instr[1])

print(sum([cycles[x] * x for x in [20, 60, 100, 140, 180, 220]]))

display = ['.'] * 240

for i, x in enumerate(cycles[1:len(display)]):
	if abs((i % 40) - x) <= 1:
		display[i] = '#'
	if cycles[i + 1] - (i % 40) == -1:
		display[i] = '#'

for i in range(6):
	print(''.join(display[i*40:(i+1)*40]))
