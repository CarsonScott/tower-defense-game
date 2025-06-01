from util import *

class Level:
	def __init__(self, wave_timelines, break_duration, enemy_manager):
		self.wave_timelines = wave_timelines
		self.break_duration = break_duration
		self.enemy_manager = enemy_manager
		self.break_timer = Timer()
		self.running = False
		self.done = False
		self.index = 0

	def start(self):
		self.running = True

	def update(self, dt):
		if self.running:
			if self.break_timer.is_done():
				wave_timeline = self.wave_timelines[self.index]

				enemies = wave_timeline.update(dt)
				self.enemy_manager.add(*enemies)

				if wave_timeline.done and len(self.enemy_manager.enemies) == 0:
					self.index += 1
					self.break_timer.start(self.break_duration)

				if self.index == len(self.wave_timelines):
					self.running = False
					self.done = True

			self.break_timer.update(dt)
