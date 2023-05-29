a, b = map(int, open('./input.txt').read().split('-'))

def has_pair(p):
	l = ''
	for c in p:
		if c == l:
			return True
		l = c
	return False

def increasing(p):
	l = 0
	for c in p:
		c = int(c)
		if c < l:
			return False
		l = c
	return True

c = 0

for p in range(a, b + 1):
	if has_pair(str(p)) and increasing(str(p)):
		c += 1

print(c)

def has_pair(p):
	l = p[0]
	r = 1
	for c in p[1:]:
		if c == l:
			r += 1
		else:
			if r == 2:
				return True
			r = 1
		l = c
	return r == 2

c = 0

for p in range(a, b + 1):
	if has_pair(str(p)) and increasing(str(p)):
		c += 1

print(c)
