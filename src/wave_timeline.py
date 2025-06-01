from util import *

class WaveTimeline:
	def __init__(self):
		self.start_times = []
		self.spawn_events = []
		self.stop_watch = StopWatch()
		self.done = False

	def add_event(self, start_time, spawn_event):
		self.start_times.append(start_time)
		self.spawn_events.append(spawn_event)

	def update(self, dt):
		enemies = []

		if not self.done:
			done = True

			for i in range(len(self.start_times)):
				time = self.stop_watch.time
				start_time = self.start_times[i]
				spawn_event = self.spawn_events[i]

				if time >= start_time and not spawn_event.running and not spawn_event.done:
					spawn_event.start()

				enemy = spawn_event.update(dt)

				if enemy != None:
					enemies.append(enemy)

				if not spawn_event.done:
					done = False

			self.done = done
			self.stop_watch.update(dt)


		return enemies
