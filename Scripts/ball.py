import pygame

from game_object import GameObject
from utils import add_tuple

from box_collider import BoxCollider
from character import Mover

class Ball(GameObject):
	def __init__(self, size: int, pos: (0, 0), color = (255, 255, 255), show_collider = False):
		self.__size = size
		self.__pos = (pos[0] - size // 2, pos[1] - size // 2)
		self.__color = color
		self.__box_collider = BoxCollider((size * 2, size * 2), (self.__pos[0] - size, self.__pos[1] - size), show_collider)
		self.__mover = Mover(10, self.__pos)

	def update(self, delta):		
		self.__mover.update(delta)
		self.__pos = self.__mover.pos
		self.__box_collider.set_pos(add_tuple(self.__pos, (-self.__size, -self.__size)))

	def handle_input(self, event):
		self.__mover.handle_input(event)

	def render(self, window):
		pygame.draw.circle(window, self.__color, self.__pos, self.__size)
		self.__box_collider.render(window)
		
