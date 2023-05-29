import copy


class Burrow():
	FREE = '.'
	ENERGY = {
		'A': 1,
		'B': 10,
		'C': 100,
		'D': 1000,
	}
	IDEAL = {
		'A': 0,
		'B': 1,
		'C': 2,
		'D': 3,
	}
	IDEAL_REV = list(IDEAL.keys())

	def __init__(self, rooms):
		self.rooms = rooms
		self.hallway = [self.FREE] * (len(self.rooms) * 2 + 3)
		self.last_move = None
		self.energy = 0

	def __str__(self):
		gen = []
		for i in range(len(self.rooms[0])):
			row = [room[i] for room in self.rooms]
			surr = '##' if i == 0 else '  '
			gen += [f'{surr}#{"#".join(row)}#{surr}']

		lines = [
			f'#{"#" * len(self.hallway)}#',
			f'#{"".join(self.hallway)}#',
			*gen,
			'  ' + '#' * (len(self.hallway) - 2),
		]

		return '\n'.join(lines)

	# Hash the position state
	def hashState(self):
		h = 0
		for place in self.hallway[1:-1:2]:
			if place != Burrow.FREE:
				h |= Burrow.IDEAL[place] + 1
			h <<= 3
		for room in self.rooms:
			for place in room:
				if place != Burrow.FREE:
					h |= Burrow.IDEAL[place] + 1
				h <<= 3
		return h

	def undo(self):
		if self.last_move is None:
			return

		(x, y), i = self.last_move
		if isinstance(i, tuple):
			self.rooms[x][y], self.rooms[i[0]][i[1]] = self.rooms[i[0]][i[1]], self.rooms[x][y]
		else:
			self.rooms[x][y], self.hallway[i] = self.hallway[i], self.rooms[x][y]
		
		self.last_move = None

	def copy(self):
		return copy.deepcopy(self)

	def is_valid(self, a, b):
		try:
			self.move(a, b)
		except Exception as ex:
			return False

		self.undo()
		return True

	def is_solved(self):
		for i, room in enumerate(self.rooms):
			for space in room:
				if space != Burrow.IDEAL_REV[i]:
					return False

		return True

	# From room to hallway or from hallway to room or from room to room but not hallway to hallway
	def move(self, a, b):
		# If room to room just move to hallway then to room
		if isinstance(a, tuple) and isinstance(b, tuple):
			if a[0] == b[0]:
				raise Exception('cannot move in same room')

			go_left = b[0] < a[0]
			stop = (2 + a[0] * 2) + (-1 if go_left else 1)
			energy = self.move(a, stop)
			try:
				energy += self.move(stop, b)
			except Exception as ex:
				self.undo()
				raise ex

			self.last_move = (a, b)

			return energy

		t, i = None, None

		if isinstance(a, tuple):
			t, i  = a, b
		else:
			i, t = a, b

		if not (isinstance(t, tuple) and isinstance(i, int)):
			raise Exception('one argument must be a tuple and the other must be an int')

		a, b = self.rooms[t[0]][t[1]], self.hallway[i]

		if a == Burrow.FREE and b == Burrow.FREE:
			raise Exception('neither a nor b is an amphipod')

		amphipod = b if a == Burrow.FREE else a
		hall_to_room = a == Burrow.FREE
		room_to_hall = not hall_to_room

		if self.last_move is not None and self.last_move == (a, b):
			raise Exception('cannot reverse previous move')

		if 1 < i < len(self.hallway) - 2 and (i % 2) == 0:
			raise Exception('is shy :(')

		if hall_to_room:
			if t[0] != Burrow.IDEAL[amphipod]:
				raise Exception('room is not destination')
		
			for slot in self.rooms[t[0]]:
				if slot == Burrow.FREE:
					continue
				if slot != amphipod:
					raise Exception('room contains amphipod of different species')

		exit = 2 + t[0] * 2
		ltr = i < exit
		rtl = not ltr

		roompath = self.rooms[t[0]][:t[1] + hall_to_room]
		if room_to_hall:
			reversed(roompath)

		l = min(i, exit)
		r = max(i, exit)
		hallpath = self.hallway[l + (hall_to_room and ltr):r + (room_to_hall or ltr)]
		if rtl:
			reversed(hallpath)

		path = [*roompath, *hallpath]
		if path != [Burrow.FREE] * len(path):
			raise Exception('path is not clear', ''.join(path))

		self.rooms[t[0]][t[1]], self.hallway[i] = b, a
		self.last_move = (t, i)

		return len(path) * Burrow.ENERGY[amphipod]

	def valid_moves(self):
		# Check hallway for valid moves to room
		for i, place in enumerate(self.hallway):
			if place == Burrow.FREE:
				continue

			target = self.IDEAL[place]
			room = self.rooms[target]

			# if we had more than two per room we'd check for the case ..10
			for j, room_place in enumerate(room):
				if room_place != place and room_place != Burrow.FREE:
					break

				if room_place == Burrow.FREE and j != len(room) - 1:
					continue

				slot = j - (0 if room_place == Burrow.FREE else 1)
				if self.is_valid(i, (target, slot)):
					yield i, (target, slot)
					return

		# Check rooms for valid moves to other rooms
		for i, room in enumerate(self.rooms):
			amphipod = -1
			for j, place in enumerate(room):
				if place != Burrow.FREE:
					amphipod = j
					break

			if amphipod == -1:
				continue

			place = room[amphipod]
			target = Burrow.IDEAL[place]
			if target == i:
				continue

			arr = self.rooms[target]
			for j, room_place in reversed(list(enumerate(arr))):
				if room_place == Burrow.FREE:
					if self.is_valid((i, amphipod), (target, j)):
						yield (i, amphipod), (target, j)
						return
					break

				if room_place != place:
					break

		# Check rooms for valid moves
		for i, room in enumerate(self.rooms):
			amphipod = -1
			for j, place in enumerate(room):
				if place != Burrow.FREE:
					amphipod = j
					break

			if amphipod == -1:
				continue

			rest = room[amphipod + 1:]
			if Burrow.IDEAL[place] == i and rest == [place] * len(rest):
				continue

			for j in range(len(self.hallway)):
				if 1 < j < len(self.hallway) - 1 and (j % 2) == 0:
					continue
				if self.is_valid((i, amphipod), j):
					yield (i, amphipod), j

def bfs_solve(b):
	en = 999999
	all_states = {}
	level = [b]
	next_level = []
	while len(level) > 0:
		print(len(level))
		for cur in level:
			for a, b in cur.valid_moves():
				c = cur.copy()
				c.energy += c.move(a, b)
				if c.is_solved():
					if c.energy < en:
						en = c.energy
						print('solved', en)
					continue
				k = c.hashState()
				if k in all_states:
					if all_states[k].energy > c.energy:
						all_states[k] = c
						next_level += [c]
				else:
					next_level += [c]

		# print('\n'.join(map(str, level)))
		level, next_level = next_level, []

rooms = None
for line in open('./input.txt').readlines()[2:-1]:
	amphipods = line.strip('\n #').split('#')
	if rooms is None:
		rooms = [[a] for a in amphipods]
	else:
		for i, a in enumerate(amphipods):
			rooms[i] += [a]

moves = [
	((2, 0), 3),
	((1, 0), (2, 0)),
	((1, 1), 5),
	(3, (1, 1)),
	((0, 0), (1, 0)),
	((3, 0), 7),
	((3, 1), 9),
	(7, (3, 1)),
	(5, (3, 0)),
	(9, (0, 0)),
]

# burr = Burrow(rooms)
# print(burr)
# for a, b in moves:
# 	valid_moves = burr.valid_moves()
# 	valid = (a, b) in valid_moves or (b, a) in valid_moves
# 	print(a, '->', b, '(valid)' if valid else '(invalid)')

# 	burr.move(a, b)
# print(burr)

bfs_solve(Burrow(rooms))
