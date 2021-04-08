import pygame

from game_object import GameObject

class BoxCollider(GameObject):
	def __init__(self, size: tuple[int, int], pos = (0, 0), visible = False):
		self.size = size
		self.pos = pos
		self.__visible = visible

	def render(self, window):
		if self.__visible:
			pygame.draw.rect(window, (255, 255, 0), pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]), 1)

	def set_pos(self, new_pos):
		self.pos = new_pos
