import pygame

from game_object import GameObject
from utils import foreach
from color import WHITE

from config import WINDOW_WIDTH, WINDOW_HEIGHT

from box_collider import BoxCollider

class Rectangle(GameObject):
	def __init__(self, color: tuple[int, int, int], left: float, top: float, width: float, height: float):
		self.__left = left
		self.__top = top
		self.__width = width
		self.__height = height
		self.__color = color
		self.__box_collider = BoxCollider((width + 10, height + 10), (left, top), True)

	def render(self, window):
		pygame.draw.rect(window, self.__color, pygame.Rect(self.__left, self.__top, self.__width, self.__height))
		self.__box_collider.render(window)

class Playground(GameObject):
	def __init__(self, rect: pygame.rect, border_width: int, goal_len: int):
		# self.__rect = rect
		self.__borders = self.__setup_borders(rect, border_width, goal_len)

	def __setup_borders(self, rect: pygame.rect, border_width: int, goal_len: int) -> list[Rectangle]:
		side_border_height = (rect.height - goal_len) // 2
		lower_side_border_y = side_border_height + goal_len
		right_border_x = rect.left + rect.width - border_width

		return [
			Rectangle(WHITE, rect.left, rect.top, rect.width, border_width), 							# top
			Rectangle(WHITE, rect.left, rect.height, rect.width, border_width), 						# bottom
			Rectangle(WHITE, rect.left, rect.top, border_width, side_border_height),  					# top left
			Rectangle(WHITE, right_border_x, rect.top, border_width, side_border_height),  				# top right
			Rectangle(WHITE, rect.left, lower_side_border_y, border_width, side_border_height),			# bottom left
			Rectangle(WHITE, right_border_x, lower_side_border_y, border_width, side_border_height)		# bottom right
		]

	def render(self, window):
		foreach(lambda border: border.render(window), self.__borders)
