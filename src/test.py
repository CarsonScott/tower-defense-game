from game import *

def text_list_surface(strings, text_align='left'):
	surfaces = []
	rects = []

	bottom = 0 
	max_width = None
	for string in strings:
		surf, rect = render_font(string)
		rect.top = bottom
		surfaces.append(surf)
		rects.append(rect)
		bottom = rect.bottom

		if max_width == None or rect.width > max_width:
			max_width = rect.width

	surface = pygame.Surface((max_width, bottom), pygame.SWSURFACE)

	for i in range(len(surfaces)):
		s = surfaces[i]
		r = rects[i]

		if text_align == 'center':
			r.centerx = int(max_width/2)
		elif text_align == 'right':
			r.right = max_width

		surface.blit(s, r)
	return surface



class GS(GameManager):

	def initialize(self):
		self.enemy_manager = EnemyManager()
		self.ballistic_manager = BallisticManager()
		self.tower_manager = TowerManager()

		points = np.array([
			[0,0],
			[300, 300],
			[600, 300],
			[800, 600]
		])

		self.points = points

		wave1 = WaveTimeline()
		wave1.add_event(0, SpawnEvent(0.5, [0, 0, 0, 0, 0, 0, 0, 1, 1], points))
		wave1.add_event(10, SpawnEvent(1.0, [0, 1, 1, 0, 0, 0, 1, 1, 1], points))

		wave2 = WaveTimeline()
		wave2.add_event(0, SpawnEvent(0.2, [0,0,0,1,1,0,0,0,1,1,1,1], points))
		wave2.add_event(10, SpawnEvent(0.5, [1,1,1,1,1,1,0,0,0,1,1,1,1], points))

		self.level = Level([wave1, wave2], 5, self.enemy_manager)
		self.level.start()

		self.coins = 100
		self.lives = 5

	def check_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if self.coins >= TOWER_TEMPLATES[0]['cost_value']:
					tower = create_tower(0, np.array(event.pos), self.ballistic_manager)
					self.tower_manager.add(tower)
					self.coins -= tower.cost_value

	def update(self):
		for i in range(1, len(self.points)):
			p1 = np.array(self.points[i-1], dtype=int)
			p2 = np.array(self.points[i], dtype=int)
			pygame.draw.line(self.screen, (255,255,255), p1, p2, 1)

		done_ballistics = self.ballistic_manager.get_done_ballistics()

		self.level.update(self.dt)

		self.enemy_manager.update(self.dt)
		self.enemy_manager.draw(self.screen)

		for enemy in self.enemy_manager.get_dead_enemies():
			self.coins += enemy.reward_value

		for enemy in self.enemy_manager.get_done_enemies():
			self.lives -= enemy.punish_value

		self.tower_manager.update(self.enemy_manager.enemies, self.dt)
		self.tower_manager.draw(self.screen)

		self.ballistic_manager.update(self.enemy_manager.enemies, self.dt)
		self.ballistic_manager.draw(self.screen)

		strings = [
			'Wave: ' + str(self.level.index),
			'Break Timer: ' + str(format(self.level.break_timer.time, '.2f')),
			'Coins: ' + str(self.coins),
			'Lives: ' + str(self.lives)
		]

		surf = text_list_surface(strings, 'right')
		rect = surf.get_rect(topright=(self.screen_size[0], 0))
		self.screen.blit(surf, rect)

if __name__ == "__main__":
	gs = GS((1200, 600))
	gs.run()