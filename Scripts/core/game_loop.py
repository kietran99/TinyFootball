import pygame

from config import *
from utils import *
from game_object import *

class GameLoop:
	def __init__(self, window, game_objects: list[GameObject]):	
		self.__delta_time = DELTA_TIME
		self.__window = window
		# self.__game_objects = game_objects
		self.__foreach_GO = lambda fn: foreach(fn, game_objects)
		self.__foreach_GO(lambda GO: GO.start())
		self.__loop()

	def __loop(self):
		isRunning = True

		while (isRunning):
			pygame.time.delay(self.__delta_time)
			self.__foreach_GO(lambda GO: GO.update())

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					isRunning = False

				self.__foreach_GO(lambda GO: GO.handle_input(event))

			self.__foreach_GO(lambda GO: GO.render(self.__window))
			pygame.display.update()

		pygame.quit()