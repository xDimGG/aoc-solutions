import numpy as np

class Board():
	def __init__(self, numbers):
		self.numbers = {}
		for m, col in enumerate(numbers):
			for n, num in enumerate(col):
				self.numbers[num] = (m, n)

		self.board = numbers
		self.marked = np.zeros(numbers.shape, dtype=bool)
	
	def mark(self, num):
		if num in self.numbers:
			self.marked[self.numbers[num]] = True

	def won(self):
		return self.marked.all(axis=0).any() or self.marked.all(axis=1).any()

	def sum_unmarked(self):
		return self.board[~self.marked].sum()

f = open('./input.txt').read().split('\n\n')
numbers = map(int, f[0].split(','))
boards = [Board(np.loadtxt(block.splitlines())) for block in f[1:]]
remaining = set(range(len(boards)))

for num in numbers:
	for i, board in enumerate(boards):
		board.mark(num)

		if i in remaining and board.won():
			if len(remaining) == len(boards) or len(remaining) == 1:
				print(int(board.sum_unmarked() * num))

			remaining -= {i}
