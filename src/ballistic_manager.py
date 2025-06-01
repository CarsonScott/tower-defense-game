from util import *

class BallisticManager:
	def __init__(self):
		self.ballistics = []
		self.done_indices = []

	def add(self, *ballistics):
		self.ballistics += list(ballistics)

	def get_done_ballistics(self):
		return [self.ballistics[i] for i in self.done_indices]

	def update(self, enemies, dt):
		for ballistic in [self.ballistics[i] for i in self.done_indices]:
			self.ballistics.remove(ballistic)

		self.done_indices = []

		for i in range(len(self.ballistics)):
			ballistic = self.ballistics[i]
			ballistic.update(enemies, dt)

			if ballistic.done:
				self.done_indices.append(i)

	def draw(self, screen):
		for ballistic in self.ballistics:
			ballistic.draw(screen)
