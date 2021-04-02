from game_loop import *

class Window:
	def __init__(self, name: str, size: (int, int), game_objects: list[GameObject]):	
		pygame.init()
		pygame.display.set_caption(name)	
		GameLoop(pygame.display.set_mode(size), game_objects)
		