from util import *

class TowerManager:
	def __init__(self):
		self.towers = []

	def add(self, *towers):
		self.towers += list(towers)

	def update(self, enemies, dt):

		for tower in self.towers:
			tower.update(enemies, dt)

	def draw(self, screen):
		for tower in self.towers:
			tower.draw(screen)
