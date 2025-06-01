from util import *

class Ballistic:
	def __init__(self, position, target, move_speed, radius, damage):
		position = np.array(position)
		target = np.array(target)

		self.position = position
		self.target = target

		self.move_speed = move_speed
		self.radius = radius
		self.damage = damage
		
		self.done = False

	def update(self, enemies, dt):
		if not self.done:
			current_angle = compute_angle(self.position, self.target)

			direction = compute_direction(self.position, self.target)
			velocity = direction * self.move_speed

			next_position = self.position + velocity * dt
			next_angle = compute_angle(next_position, self.target)

			if abs(angle_difference(next_angle, current_angle)) > 0.1:
				self.done = True

			else:
				self.position = next_position

				for enemy in enemies:
					distance = compute_distance(self.position, enemy.position)

					if distance <= self.radius + enemy.radius:
						enemy.apply_damage(self.damage)
						self.done = True
						break

	def draw(self, screen):
		pos = np.array(self.position, dtype=int)
		pygame.draw.circle(screen, (0,255,0), pos, self.radius)


def create_ballistic(template_index, position, target):
	ball_t = BALLISTIC_TEMPLATES[template_index]

	return Ballistic(
		position=position,
		target=target,
		move_speed=ball_t['move_speed'],
		radius=ball_t['radius'],
		damage=ball_t['damage'])
