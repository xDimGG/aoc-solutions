import copy

lines = list(map(lambda x: [*x.strip()], open('./input.txt').readlines()))
iterations = 0

while iterations < 9e9:
	changed = False

	new_lines = copy.deepcopy(lines)

	for j, line in enumerate(lines):
		for i in range(len(line)):
			if line[i] == '>':
				n = (i + 1) % len(line)
				if line[n] == '.':
					new_lines[j][n] = '>'
					new_lines[j][i] = '.'
					changed = True

	lines = copy.deepcopy(new_lines)

	for i in range(len(lines[0])):
		for j in range(len(lines)):
			if lines[j][i] == 'v':
				n = (j + 1) % len(lines)
				if lines[n][i] == '.':
					new_lines[n][i] = 'v'
					new_lines[j][i] = '.'
					changed = True

	iterations += 1
	lines = new_lines
	if not changed:
		print('Part 1', iterations)
		break

	# print('After', iterations, 'steps')
	# print('\n'.join(map(''.join, lines)))
