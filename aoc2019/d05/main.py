mem = [*map(int, open('./input.txt').read().split(','))]
HALT = 99

def exec(mem, input):
	mem += [0, 0, 0]
	output = []
	ip = 0

	while mem[ip] != 99:
		# print(ip)
		# print(mem)
		op, a, b, c = mem[ip:ip+4]
		ai = (op // 100) % 10
		bi = (op // 1000) % 10
		ci = (op // 10000) % 10
		op = op % 100

		# print(op, ai, bi, ci, a, b, c)

		assert op in [1, 2, 3, 4, 5, 6, 7, 8]

		if op not in [3, 4]:
			if ai == 0:
				a = mem[a]
			if bi == 0:
				b = mem[b]

		if op == 1:
			mem[c] = a + b
			ip += 4
		if op == 2:
			mem[c] = a * b
			ip += 4
		if op == 3:
			mem[a] = input.pop(0)
			ip += 2
		if op == 4:
			output += [mem[a]]
			ip += 2
		if op == 5:
			if a != 0:
				ip = b
			else:
				ip += 3
		if op == 6:
			if a == 0:
				ip = b
			else:
				ip += 3
		if op == 7:
			mem[c] = int(a < b)
			ip += 4
		if op == 8:
			mem[c] = int(a == b)
			ip += 4

	return output

print(exec([*mem], [1])[-1])
print(exec([*mem], [5])[-1])


# for noun in range(0, 100):
# 	for verb in range(0, 100):
# 		if exec([*mem], noun, verb) == 19690720:
# 			print(100 * noun + verb)
# 			exit()
