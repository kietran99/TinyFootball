from event_channel import trigger
from event_names import a_second_passed, game_over
from game_object import GameObject

class Timer(GameObject):
	def __init__(self, match_time):
		self.__is_active = True
		self.__match_time = match_time
		self.__time_passed = 0
		trigger(a_second_passed, self.__match_time)

	def update(self, delta):
		if not self.__is_active:
			return

		self.__time_passed += delta

		if self.__match_time <= self.__time_passed:
			self.__is_active = False
			trigger(game_over, None)

		if self.__time_passed % 1000 == 0:
			print(self.__match_time - self.__time_passed)
			trigger(a_second_passed, self.__match_time - self.__time_passed)