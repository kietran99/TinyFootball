import pygame

from utils import *

from core_config import FONT_PATH
from game_object import GameObject

class Text(GameObject):
	def __init__(self, text: str, size: int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.text = text
		self.__size = size
		self.__color = color
		self.__pos = pos

	def render(self, window):
		render_text_fn = self.__bind(window, pygame.font.Font(FONT_PATH, self.__size))
		render_text_fn(self.text, self.__color, self.__pos)

	def __bind(self, window, font):
		return lambda text, color, pos: self.__render_number(window, font, text, color, pos) if text.isdigit() else \
    		self.__render_text(window, font, text, color, pos)

	def __render_number(self, window, font, text : int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.__render_text(window, font, self._format_num(text), color, pos)

	def _format_num(self, num: int):
		return ("0" if num < 10 else "") + str(num)

	def __render_text(self, window, font, text : str, color: tuple[int, int, int], pos: tuple[int, int]):
		time_text = font.render(text, True, color)
		time_text_rect = time_text.get_rect()
		time_text_rect.center = pos
		window.blit(time_text, time_text_rect)

class UICanvas(GameObject):
	def __init__(self, UI_components: list[GameObject]):
		self.__UI_components = UI_components

	def render(self, window):
		foreach(lambda GO: GO.render(window), self.__UI_components)
	