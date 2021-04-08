import pygame

from game_object import GameObject
from utils import add_tuple

from core.Physics import Vector,magntude
# from ball import Ball

UP = 1 << 0
DOWN = 1 << 2
LEFT = 1 << 3
RIGHT = 1 << 4

class Mover(GameObject):
	def __init__(self, move_speed: int, pos: tuple[int, int], keycode = None):
		self.__holding_key = None
		self.__move_speed = move_speed
		self.pos = pos
		self.__keycode = keycode

	def update(self, delta):
		if not self.__holding_key:
			return

		move_vect = (0, 0)
		
		if self.__holding_key & UP:
			move_vect = add_tuple(move_vect, (0, -self.__move_speed))
		
		if self.__holding_key & DOWN:
			move_vect = add_tuple(move_vect, (0, self.__move_speed))

		if self.__holding_key & LEFT:
			move_vect = add_tuple(move_vect, (-self.__move_speed, 0))

		if self.__holding_key & RIGHT:
			move_vect = add_tuple(move_vect, (self.__move_speed, 0))

		self.pos = add_tuple(self.pos, move_vect)

	def handle_input(self, event):
		if event.type == pygame.KEYUP:
			self.__holding_key = None
			return

		if event.type != pygame.KEYDOWN:
			return
		if(self.__keycode != None):
			self.__holding_key = 0x0000
			pressed_keys = pygame.key.get_pressed()

			if pressed_keys[self.__keycode[0]]:
				self.__holding_key |= UP

			if pressed_keys[self.__keycode[1]]:
				self.__holding_key |= DOWN

			if pressed_keys[self.__keycode[2]]:
				self.__holding_key |= LEFT

			if pressed_keys[self.__keycode[3]]:
				self.__holding_key |= RIGHT
			return
		# self.__holding_key = 0x0000
		# pressed_keys = pygame.key.get_pressed()

		# if pressed_keys[pygame.K_w]:
		# 	self.__holding_key |= UP

		# if pressed_keys[pygame.K_s]:
		# 	self.__holding_key |= DOWN

		# if pressed_keys[pygame.K_a]:
		# 	self.__holding_key |= LEFT

		# if pressed_keys[pygame.K_d]:
		# 	self.__holding_key |= RIGHT
