from gamelib import *

POS_RANDOM = 10

ENEMY_TEMPLATES = {
	0: {
		'move_speed': 50,
		'max_health': 25,
		'radius': 10,
		'reward_value': 12,
		'punish_value': 1
	},

	1: {
		'move_speed': 25,
		'max_health': 50,
		'radius': 20,
		'reward_value': 20,
		'punish_value': 2
	}
}

BALLISTIC_TEMPLATES = {
	0:{
		'move_speed': 300,
		'radius': 3,
		'damage': 10
	}
}

TOWER_TEMPLATES ={
	0: {
		'attack_radius': 150,
		'reload_duration': .75,
		'cost_value': 50
	}
}


class Timer:
	def __init__(self):
		self.time = 0 

	def start(self, t):
		self.time = t

	def update(self, dt):
		self.time -= dt 
		if self.time < 0:
			self.time = 0

	def is_done(self):
		return self.time == 0


class StopWatch:
	def __init__(self):
		self.time = 0

	def start(self):
		self.t = 0

	def update(self, dt):
		self.time += dt


def get_healthbar_surface(size, health, max_health):
	surface = pygame.Surface(size)
	surface.fill((255,0,0))

	x = int(size[0] * health / max_health)
	pygame.draw.rect(surface, (0,255,0), (0,0,x,size[1]))
	return surface

def generate_enemy_path(position, points):
	path = []

	closest_index = None
	min_distance = None

	for j in range(len(points)):
		point = points[j]

		distance = compute_distance(position, point)

		if min_distance == None or distance < min_distance:
			closest_index = j
			min_distance = distance

	if closest_index != None:
		prev_point = points[closest_index]
		rel_point = np.array(position)

		path.append(rel_point)

		for j in range(closest_index, len(points)-1):
			next_point = points[j+1]

			distance = compute_distance(prev_point, next_point)
			direction = compute_direction(prev_point, next_point)

			new_point = rel_point + direction * distance
			path.append(new_point)

			prev_point = next_point
			rel_point = np.array(new_point)

	return path

