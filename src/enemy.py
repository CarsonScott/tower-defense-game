from util import *

class Enemy:
	def __init__(self, position, move_speed, path_points, max_health, radius, reward_value, punish_value):
		position = np.array(position)

		self.position = position
		self.velocity = np.zeros((2,))

		self.move_speed = move_speed
		self.max_health = max_health
		self.health = max_health
		self.radius = radius

		self.reward_value = reward_value
		self.punish_value = punish_value

		self.path = generate_enemy_path(position, path_points)
		self.path_index = 0
		self.done = False

	def apply_damage(self, damage):
		self.health -= damage
		if self.health < 0:
			self.health = 0 

	def is_dead(self):
		return self.health == 0

	def update(self, dt):
		if not self.done:
			current_point = self.path[self.path_index]

			next_point = self.path[self.path_index+1]
			current_angle = compute_angle(self.position, next_point)

			direction = compute_direction(self.position, next_point)
			velocity = direction * self.move_speed

			next_position = self.position + velocity * dt
			next_angle = compute_angle(next_position, next_point)

			if abs(angle_difference(next_angle, current_angle)) > 0.1:
				self.path_index += 1

			else: 
				self.position = next_position

			if self.path_index == len(self.path)-1:
				self.done = True

	def draw(self, screen):
		pos = np.array(self.position, dtype=int)
		pygame.draw.circle(screen, (255,0,0), pos, self.radius)


def create_enemy(template_index, position, path_points):
	enemy_t = ENEMY_TEMPLATES[template_index]

	return Enemy(
		position=position,
		path_points=path_points,
		move_speed=enemy_t['move_speed'],
		max_health=enemy_t['max_health'],
		radius=enemy_t['radius'],
		reward_value=enemy_t['reward_value'],
		punish_value=enemy_t['punish_value'])