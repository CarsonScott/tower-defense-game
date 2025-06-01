from util import *

class EnemyManager:
	def __init__(self):
		self.enemies = []
		self.done_indices = []
		self.dead_indices = []

	def add(self, *enemies):
		self.enemies += list(enemies)

	def get_done_enemies(self):
		return [self.enemies[i] for i in self.done_indices]

	def get_dead_enemies(self):
		return [self.enemies[i] for i in self.dead_indices]

	def update(self, dt):
		for enemy in [self.enemies[i] for i in self.done_indices + self.dead_indices]:
			self.enemies.remove(enemy)

		self.done_indices = []
		self.dead_indices = []

		for i in range(len(self.enemies)):
			enemy = self.enemies[i]
			enemy.update(dt)

			if enemy.done:
				self.done_indices.append(i)
			elif enemy.is_dead():
				self.dead_indices.append(i)

	def draw(self, screen):
		surface = pygame.Surface(screen.get_rect().size)
		surface.fill((255,0,255))
		surface.set_colorkey((255,0,255))

		for enemy in self.enemies:
			enemy.draw(screen)
			surf = get_healthbar_surface((50,5), enemy.health, enemy.max_health)
			rect = surf.get_rect(centerx=enemy.position[0], centery=enemy.position[1]-enemy.radius-5)
			surface.blit(surf, rect)

		screen.blit(surface, (0,0))
