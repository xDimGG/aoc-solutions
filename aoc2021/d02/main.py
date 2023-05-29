x = 0
y = 0
aim = 0

for line in open('input.txt'):
	a, b = line.rstrip().split(' ')
	b = int(b)

	if a == 'forward':
		x += b
		y += aim * b
	elif a == 'up':
		aim -= b
	elif a == 'down':
		aim += b

print(x, y, aim)
print(x * y)