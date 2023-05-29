from parse import search

r = open('./input.txt').read()
AMT = 4
# AMT = 14

for i in range(len(r)):
	window = r[i:i+AMT]
	if len(set(window)) == len(window):
		print(i + AMT)
		break
