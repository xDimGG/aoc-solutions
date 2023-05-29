from collections import Counter
import copy
from functools import cache
import itertools
import random
from parse import search

class DeterministicDie():
	index = 0

	def roll(self):
		val = self.index + 1
		self.index = val % 100
		return val

	def roll3sum(self):
		return self.roll() + self.roll() + self.roll()

class Player():
	def __init__(self, id, pos, score=0):
		self.id = id
		self.pos = pos
		self.score = score

d = DeterministicDie()
original_players = []
for line in open('./input.txt').readlines():
	res = search('Player {:d} starting position: {:d}', line)
	original_players += [Player(res[0], res[1])]

players = copy.deepcopy(original_players)

roll = 0
max_score = 0

while max_score < 1000:
	p = players[roll % 2]
	p.pos += d.roll3sum()
	p.pos = ((p.pos - 1) % 10) + 1
	p.score += p.pos
	max_score = max(p.score, max_score)
	roll += 3

print(*map(lambda x: x.score, players))
print(min(map(lambda x: x.score, players)) * roll)

sumOccurrences = Counter(map(sum, itertools.product([1, 2, 3], repeat=3)))

a = 0
b = 0

# P1 must beat P2
@cache
def count(p1goal, p2goal, p1last, p2last):
	wins = 0

	for p1roll, p1occurrences in sumOccurrences.items():
		p1next = ((p1last + p1roll - 1) % 10) + 1

		# P1 won
		if p1next >= p1goal:
			wins += p1occurrences 
			continue

		for p2roll, p2occurrences in sumOccurrences.items():
			p2next = ((p2last + p2roll - 1) % 10) + 1

			# P2 won
			if p2next >= p2goal:
				continue

			wins += p1occurrences * p2occurrences * count(p1goal - p1next, p2goal - p2next, p1next, p2next)

	return wins

print(count(21, 21, original_players[0].pos, original_players[1].pos))