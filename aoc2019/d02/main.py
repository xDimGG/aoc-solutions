mem = [*map(int, open('./input.txt').read().split(','))]
HALT = 99

def exec(mem, noun, verb):
	pc = 0
	mem[1] = noun
	mem[2] = verb

	while mem[pc] != 99:
		op, a, b, c = mem[pc:pc+4]
		a = mem[a]
		b = mem[b]
		assert op in [1, 2]
		if op == 1:
			mem[c] = a + b
		if op == 2:
			mem[c] = a * b
		pc += 4

	return mem[0]

print(exec([*mem], 12, 2))

for noun in range(0, 100):
	for verb in range(0, 100):
		if exec([*mem], noun, verb) == 19690720:
			print(100 * noun + verb)
			exit()
