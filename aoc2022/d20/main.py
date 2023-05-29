from parse import search
import numpy as np

raw = open('./input.txt').read()
nums = list(map(int, raw.splitlines()))
copy = [*nums]

# Doubly-linked Circular List
class Node():
	def __init__(self, data):
		self.data = data
		self.prev = self
		self.next = self

	def __str__(self):
		return str(self.data)

	def insert_after(self, other):
		other.next = self.next
		other.prev = self
		self.next.prev = other
		self.next = other

	def delete(self):
		self.prev.next = self.next
		self.next.prev = self.prev
		self.next = self
		self.prev = self

	def shift(self, i):
		if i == 0:
			return

		proceed = self.prev
		self.delete()

		for _ in range(abs(i)):
			proceed = proceed.next if i > 0 else proceed.prev

		proceed.insert_after(self)

	def get(self, i):
		cur = self

		for x in range(abs(i)):
			cur = cur.next if i > 0 else cur.prev

		return cur

	# def insert_before(self, other):
	# 	other.prev = self.prev
	# 	other.next = self

	# 	self.prev.next = other
	# 	self.prev = other

	# def delete(self):
	# 	self.next.prev = self.prev
	# 	self.prev.next = self.next

	# def shift(self, i):
	# 	self.delete()

	# 	preceed = self.next if i >= 0 else self
	# 	for _ in range(abs(i)):
	# 		preceed = preceed.next if i > 0 else preceed.prev

	# 	self.insert_before(preceed)

AUG = 811589153

root = Node(nums[0] * AUG)
zero = None
nodes = [root]
for n in nums[1:]:
	new = Node(n * AUG)
	nodes[-1].insert_after(new)
	nodes += [new]
	if n == 0:
		zero = new

for x in range(10):
	for n in nodes:
		n.shift(n.data % (len(nodes) - 1))

cur = zero
for x in range(len(nodes)):
	cur = cur.next

print(zero.get(1000).data + zero.get(2000).data + zero.get(3000).data)
