r = open('./input.txt').read()
l = list(map(lambda x: [list(map(int, c.split('-'))) for c in x.split(',')], r.splitlines()))

def contains(a, b, c, d):
	# return (c <= b and d >= a) or (b <= d and a >= c)
	return (c >= a and d <= b) or (a >= c and b <= d)
	# if c <= a:
	# 	a, b, c, d = c, d, a, b
	# [  ]
	#   [  ]
	# [        ]
	#  [  ]
	# return d <= b

print(sum([contains(*a, *b) for a, b in l]))

def overlaps(a, b, c, d):
	return max(a, c) <= min(b, d)

print(sum([overlaps(*a, *b) for a, b in l]))
