f = open('./input.txt').read()
rep = {
	'A': 1, # rock
	'B': 2, # paper
	'C': 3, # scissors
	'X': 1, # rock
	'Y': 2, # paper
	'Z': 3, # scissors
}

for k, v in rep.items():
	f = f.replace(k, str(v))

def score(a, b):
	if a == b:
		return 3 + b
	elif b == ((a % 3) + 1):
		return 6 + b
	else:
		return b

total = sum([score(*map(int, line.split(' '))) for line in f.splitlines()])

print(total)

def new_score(a, b):
	if b == 1:
		return score(a, 3 if a == 1 else a - 1)
	elif b == 2:
		return score(a, a)
	elif b == 3:
		return score(a, ((a % 3) + 1))

total = sum([new_score(*map(int, line.split(' '))) for line in f.splitlines()])

print(total)
