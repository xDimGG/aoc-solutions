import functools

defs = {}

class Node():
	def __init__(self, data, left = None, right = None):
		self.data = data
		self.parent = None
		self.left = left
		self.right = right
		if left is not None:
			left.parent = self
		if right is not None:
			right.parent = self

for line in open('./input.txt').readlines():
	l, r = line.rstrip().split(': ')
	defs[l] = r

humn = None

def build(root):
	global humn
	d = defs[root]

	if d.isdigit():
		n = Node(int(d))
		if root == 'humn':
			humn = n
		return n
	else:
		l, op, r = d.split(' ')
		return Node(op, build(l), build(r))

def exec(node: Node):
	if isinstance(node.data, int):
		return node.data
	
	match node.data:
		case '+': return exec(node.left) + exec(node.right)
		case '-': return exec(node.left) - exec(node.right)
		case '*': return exec(node.left) * exec(node.right)
		case '/': return exec(node.left) / exec(node.right)

inverses = { '+': '-', '-': '+', '*': '/', '/': '*' }
root = build('root')

def solve(var, left, right):
	queue = []
	cur = var
	while cur != left and cur != right:
		sibling = cur.parent.right if cur.parent.left == cur else cur.parent.left
		queue.append((inverses[cur.parent.data], exec(sibling)))
		cur = cur.parent

	num = exec(left if cur == right else right)
	for op, val in queue[::-1]:
		num = eval(f'num {op} {val}')

	return num

print(exec(root))
print(solve(humn, root.left, root.right))

print(exec(root.right))
humn.data = 3342154812537
print(exec(root.left))

# print(exec(root.right))
# humn.data = 8764479278267
# print(exec(root.left))

