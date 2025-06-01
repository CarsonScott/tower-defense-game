from util import *
from ballistic import create_ballistic

class Tower:
	def __init__(self, position, type, attack_radius, reload_duration, ballistic_manager, cost_value):
		position = np.array(position)
		self.position = position
		self.type = type
		self.attack_radius = attack_radius
		self.reload_duration = reload_duration
		self.ballistic_manager = ballistic_manager
		self.cost_value = cost_value
		self.reload_timer = Timer()
		self.target = None

	def update(self, enemies, dt):
		self.reload_timer.update(dt)

		if self.reload_timer.is_done():
			targets = []
			distances = []

			for i in range(len(enemies)):
				enemy = enemies[i]

				distance = compute_distance(self.position, enemy.position)
				if distance <= self.attack_radius:
					targets.append(i)
					distances.append(distance)

			if len(targets) > 0:
				enemy = enemies[targets[distances.index(min(distances))]]
				direction = compute_direction(self.position, enemy.position)
				target = self.position + direction * self.attack_radius

				ballistic = create_ballistic(self.type, self.position, target)
				self.ballistic_manager.add(ballistic)

				self.reload_timer.start(self.reload_duration)


	def draw(self, screen):
		pos = np.array(self.position, dtype=int)
		pygame.draw.circle(screen, (255,255,255), pos, 3)
		pygame.draw.circle(screen, (255,255,255), pos, self.attack_radius, 2)


def create_tower(template_index, position, ballistic_manager):
	tower_t = TOWER_TEMPLATES[template_index]
	ball_t = BALLISTIC_TEMPLATES[template_index]

	return Tower(
		position=position, 
		type=template_index,
		attack_radius=tower_t['attack_radius'],
		reload_duration=tower_t['reload_duration'],
		ballistic_manager=ballistic_manager,
		cost_value=tower_t['cost_value'])