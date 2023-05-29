import math
import random
import re

class Blueprint():
	ORE = 0
	CLAY = 1
	OBSIDIAN = 2
	GEODE = 3

	def __init__(self, id, ore_bot, clay_bot, obs_bot_ore, obs_bot_clay, geode_bot_ore, geode_bot_obs):
		self.id = id
		self.ore = { self.ORE: ore_bot }
		self.clay = { self.ORE: clay_bot }
		self.obsidian = {
			self.ORE: obs_bot_ore,
			self.CLAY: obs_bot_clay,
		}
		self.geode = {
			self.ORE: geode_bot_ore,
			self.OBSIDIAN: geode_bot_obs,
		}

		self.costs = [
			self.ore,
			self.clay,
			self.obsidian,
			self.geode,
		]

		self.max_ore = max(ore_bot, clay_bot, obs_bot_ore, geode_bot_ore)

blueprints = []

for line in open('./input.txt').readlines():
	blueprints.append(Blueprint(*map(int, re.findall('\d+', line))))

def advanced(state, minutes):
	return [
		state[0] + (state[4] * minutes),
		state[1] + (state[5] * minutes),
		state[2] + (state[6] * minutes),
		*state[3:7],
		state[7] - minutes,
	]

def generate_states(bp: Blueprint, state):
	next_states = []
	for i, cost in enumerate(bp.costs):
		ttr = [] # time to each resource
		for resource, amount in cost.items():
			rate = state[resource + 4]
			if rate == 0:
				ttr = None # resources can't be reached from this state
				break
			ttr.append(max(0, (amount - state[resource]) / rate))

		if ttr is None:
			continue

		# time to resource that takes the longest
		ttr = int(math.ceil(max(ttr)))

		# resource can't be built with remaining time
		if ttr >= state[7]:
			continue

		# advance to when we have resources
		new_state = advanced(state, ttr + 1)

		# don't save # of geode bots, just how many geodes were cracked
		if i == Blueprint.GEODE:
			new_state[3] += new_state[7]
		else:
			new_state[i + 4] += 1

		# apply costs
		for resource, amount in cost.items():
			new_state[resource] -= amount

		next_states.append(new_state)

	return next_states


def exec(bp, minutes):
	global best, global_best
	best = {}
	global_best = 0

	def dfs(state):
		global best, global_best
		local_best = state[3]

		for next_state in generate_states(bp, state):
			next_state[0] = min(bp.max_ore * 2 - next_state[4], next_state[0])

			if next_state[4] > bp.max_ore:
				continue

			if (global_best - next_state[3]) > ((next_state[7] ** 2) / 2):
				continue

			k = tuple(next_state)
			if k in best:
				local_best = max(local_best, best[k])
			else:
				n = dfs(next_state)
				local_best = max(local_best, n)
				global_best = max(global_best, n)
				best[k] = n

		return local_best

	return dfs([
		# Ore, clay, obs, geodes
		0, 0, 0, 0,
		# Ore bots, clay bots, obs bots
		# No need to store geode bots as their geodes created can be calculated
		1, 0, 0,
		# Minutes remaining
		minutes,
	])

s = 0

for bp in blueprints:
	s += bp.id * exec(bp, 24)

print(s)

s = 1

for bp in blueprints[:3]:
	s *= exec(bp, 32)

print(s)
