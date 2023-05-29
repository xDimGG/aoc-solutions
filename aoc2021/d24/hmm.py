lines = list(map(lambda l: l.rstrip().split(' ')[-1], open('input.txt').readlines()))

A = map(int, lines[4::18])
B = map(int, lines[5::18])
C = map(int, lines[15::18])

print([*A])
print([*B])
print([*C])

W = [1] * 14
# W = map(int, [*'65984919997939'])

# for _ in range(1_000_000_000):
x, y, z = 0, 0, 0
for a, b, c, w in zip(A, B, C, W):
	x = (z % 26 + b) != w
	z //= a
	z *= (25 * x) + 1
	z += (w + c) * x

print(z)