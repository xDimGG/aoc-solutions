from parse import search

r = open('./input.txt').read()
stdout = list(map(lambda x: x.split(' '), r.splitlines()))

class Folder():
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.files = []
	
	def find(self, dir):
		for f in self.files:
			if f.name == dir:
				return f

	def size(self):
		s = 0
		for f in self.files:
			if isinstance(f, Folder):
				s += f.size()
			if isinstance(f, File):
				s += f.size

		return s

class File():
	def __init__(self, name, size):
		self.name = name
		self.size = size

command_response = []

i = 0

while i < len(stdout):
	_, cmd, *args = stdout[i]
	if cmd == 'cd':
		command_response += [([cmd, *args], [])]
	if cmd == 'ls':
		response = []
		while i + 1 < len(stdout) and stdout[i + 1][0] != '$':
			i += 1
			response += [stdout[i]]

		command_response += [([cmd], response)]

	i += 1

root = Folder('root', None)
ref = root

for command, response in command_response:
	cmd = command[0]
	if cmd == 'cd':
		arg = command[1]
		if arg == '/':
			continue
		elif arg == '..':
			ref = ref.parent
		else:
			ref = ref.find(arg)
	if cmd == 'ls':
		for type, name in response:
			if type == 'dir':
				ref.files.append(Folder(name, ref))
			if type.isdigit():
				ref.files.append(File(name, int(type)))

SIZE_MAX = 100000

def find(ref):
	s = 0
	if ref.size() < SIZE_MAX:
		s = ref.size()

	for f in ref.files:
		if isinstance(f, Folder):
			s += find(f)

	return s

print(find(root))

best = 999999999999
SIZE_MIN = root.size() - (70000000 - 30000000)

def recurse(ref):
	global best
	s = ref.size()
	if s >= SIZE_MIN and s < best:
		best = s

	for f in ref.files:
		if isinstance(f, Folder):
			recurse(f)

recurse(root)

print(best)
