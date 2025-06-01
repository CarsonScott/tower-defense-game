from util import *
from enemy import create_enemy

class SpawnEvent:
	def __init__(self, spawn_rate, enemy_list, path_points):
		self.spawn_rate = spawn_rate
		self.enemy_list = enemy_list
		self.path_points = path_points
		self.duration = spawn_rate * len(enemy_list)
		self.timer = Timer()
		self.running = False
		self.done = False
		self.index = 0

	def start(self):
		self.running = True
		self.done = False
		self.index = 0

	def update(self, dt):
		enemy = None

		if self.running:
			self.timer.update(dt)

			if self.timer.is_done():
				pos = self.path_points[0] + np.array([np.random.uniform(-POS_RANDOM, POS_RANDOM) for i in range(2)])
				enemy = create_enemy(self.enemy_list[self.index], pos, self.path_points)
				self.timer.start(self.spawn_rate)
				self.index += 1

			if self.index == len(self.enemy_list)-1:
				self.running = False
				self.done = True

		return enemy
