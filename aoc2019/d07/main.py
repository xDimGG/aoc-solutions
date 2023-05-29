import itertools
from functools import partial

mem = [*map(int, open('./input.txt').read().split(','))]
HALT = 99

class Process():
	def __init__(self, program):
		self.memory = [*program] + [0] * (len(program) % 4)
		self.ip = 0
		self.output = []

	def flush(self):
		op = self.output
		self.output = []
		return op

	# returns True if process ran to completion, False if waiting
	def run(self, input):
		mem = self.memory

		# 99 means HALT
		while mem[self.ip] != 99:
			op, a, b, c = mem[self.ip:self.ip+4]
			ai = (op // 100) % 10
			bi = (op // 1000) % 10
			ci = (op // 10000) % 10
			op = op % 100

			assert op in [1, 2, 3, 4, 5, 6, 7, 8]

			if op not in [3, 4]:
				if ai == 0:
					a = mem[a]
				if bi == 0:
					b = mem[b]

			if op == 1:
				mem[c] = a + b
			if op == 2:
				mem[c] = a * b
			if op == 3:
				if len(input) == 0:
					return False
				mem[a] = input.pop(0)
			if op == 4:
				self.output += [mem[a]]
			if op == 5:
				if a == 0:
					self.ip += 3
				else:
					self.ip = b
			if op == 6:
				if a == 0:
					self.ip = b
				else:
					self.ip += 3
			if op == 7:
				mem[c] = int(a < b)
			if op == 8:
				mem[c] = int(a == b)

			if op in [1, 2, 7, 8]:
				self.ip += 4
			if op in [3, 4]:
				self.ip += 2

		return True

best = 0

for seq in itertools.permutations([0, 1, 2, 3, 4], 5):
	last = 0
	for setting in seq:
		p = Process(mem)
		rtc = p.run([setting, last])
		assert rtc is True
		last = p.flush()[0]

	if last > best:
		best = last

print(best)

def run_seq(seq):
	devices = [Process(mem) for _ in range(5)]

	# set phases
	for device, phase in zip(devices, seq):
		assert device.run([phase]) is False

	last = 0

	while True:
		for device in devices:
			rtc = device.run([last])
			last = device.flush()[0]
			if rtc and device == devices[-1]:
				return last

best = 0

for seq in itertools.permutations([5, 6, 7, 8, 9], 5):
	last = run_seq(seq)

	if last > best:
		best = last

print(best)