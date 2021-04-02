import pygame

from utils import *

from config import FONT_PATH
from game_object import GameObject

class Text(GameObject):
	def __init__(self, text: str, size: int, color: tuple[int, int, int], pos: tuple[int, int]):
		self.__text = text
		self.__size = size
		self.__color = color
		self.__pos = pos

	def render(self, window):
		# print("Render: " + self.__class__.__name__)
		render_text_fn = self.__bind(window, pygame.font.Font(FONT_PATH, self.__size))
		render_text_fn(self.__text, self.__color, self.__pos)

	def __bind(self, window, font):
		return lambda text, color, pos: self.__render_number(window, font, text, color, pos) if text.isdigit() else \
    		self.__render_text(window, font, text, color, pos)

	def __render_text(self, window, font, text : str, color, pos):
		time_text = font.render(text, True, color)
		time_text_rect = time_text.get_rect()
		time_text_rect.center = pos
		window.blit(time_text, time_text_rect)

	def __render_number(self, window, font, text : int, color, pos):
		textToPrint = ("0" if int < 10 else "") + text
		render_text(window, font, textToPrint, color, pos)

class UICanvas(GameObject):
	def __init__(self, UI_components: list[GameObject]):
		self.__UI_components = UI_components

	# def start(self):
		# print("Init: " + self.__class__.__name__)

	# def update(self):
		# print("Update: " + self.__class__.__name__)

	def render(self, window):
		foreach(lambda GO: GO.render(window), self.__UI_components)
	