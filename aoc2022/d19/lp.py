import re
import cvxpy
import numpy as np

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
