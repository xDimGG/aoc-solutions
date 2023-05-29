import random
from parse import search
import re

class Blueprint():
	ORE = 0
	CLAY = 1
	OBISIDIAN = 2
	GEODE = 3

	def __init__(self, id, ore_bot, clay_bot, obs_bot_ore, obs_bot_clay, geode_bot_ore, geode_bot_obs):
		self.id = id
		self.ore = ore_bot
		self.clay = clay_bot
		self.obsidian = (obs_bot_ore, obs_bot_clay)
		self.geode = (geode_bot_ore, geode_bot_obs)

	def execute(self, minutes, make_decision):
		initial_state = (
			# ore [0], clay [1], obisidian [2], geodes [3]
			0, 0, 0, 0,
			# ore bots [4], clay bots [5], obsidian bots [6], geode bots [7]
			1, 0, 0, 0,
		)
		state = list(initial_state)
		previous_state = None

		for minute in range(minutes):
			state_before_buy = tuple(state)

			for bot in [3, 2, 1, 0]:
				if self.affords(bot, state) and make_decision(previous_state, state, bot, minute + 1):
					self.purchase(bot, state)
					break

			previous_state = tuple(state)

			for i in range(4):
				state[i] += state_before_buy[i + 4]

		return state

	def affords(self, bot, state):
		match bot:
			case self.GEODE:
				return state[0] >= self.geode[0] and state[2] >= self.geode[1]
			case self.OBISIDIAN:
				return state[0] >= self.obsidian[0] and state[1] >= self.obsidian[1]
			case self.CLAY:
				return state[0] >= self.clay
			case self.ORE:
				return state[0] >= self.ore

	def purchase(self, bot, state):
		state[bot + 4] += 1

		match bot:
			case self.GEODE:
				state[0] -= self.geode[0]
				state[2] -= self.geode[1]
			case self.OBISIDIAN:
				state[0] -= self.obsidian[0]
				state[1] -= self.obsidian[1]
			case self.CLAY:
				state[0] -= self.clay
			case self.ORE:
				state[0] -= self.ore

	def quality_level(self, minutes, attempts):
		def make_decision(prev, state, bot, minute):
			if bot == self.ORE and state[self.ORE + 4] == max_ore:
				return False

			if bot == self.CLAY and state[self.CLAY + 4] == max_clay:
				return False

			# if bot == self.CLAY and state[self.CLAY + 4] == 0:
			# 	return True

			# If we could afford a bot 1 state ago but did not purchase it, do not purchase it during this step
			if prev is not None and self.affords(bot, prev) and prev[bot] == state[bot]:
				return False

			# if bot == self.OBISIDIAN and state[self.OBISIDIAN + 4] == 0:
			# 	return True

			# if bot == self.GEODE and state[self.GEODE + 4] == 0:
			# 	return True

			return random.choice([True, False])
			# return True

		best = [0] * 8

		for x in range(attempts):
			max_ore = max(self.clay, self.obsidian[0], self.geode[0]) + 1
			max_clay = self.obsidian[1] // 2

			state = self.execute(minutes, make_decision)
			if state[3] > best[3]:
				best = state
				print(best)

		return best[3]

blueprints = []

for line in open('./input.txt').readlines():
	blueprints.append(Blueprint(*map(int, re.findall('\d+', line))))

# print(blueprints[0].execute(24, lambda x, y, z: True))

# s = 0

# for b in blueprints:
# 	s += b.id * b.quality_level(24, 50000)

# print(s)

s = 1

for b in blueprints[:3]:
	q = b.quality_level(32, 400000)
	print(q)
	s *= q

print(s)