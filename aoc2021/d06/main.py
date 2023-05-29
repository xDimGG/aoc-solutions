from collections import Counter

lanterns = Counter(map(int, open('./input.txt').read().split(',')))
DAYS = 256

for x in range(DAYS):
	zeros = lanterns[0]
	for i in range(8):
		lanterns[i] = lanterns[i + 1]
	
	lanterns[6] += zeros
	lanterns[8] = zeros

	if x == 79 or x == 255:
		print(sum(lanterns.values()))
