import pygame

from game_object import GameObject

class Mover(GameObject):
	def handle_input(self, event):
		if event.type != pygame.KEYDOWN:
			return

		if event.key == pygame.K_w:
			print("Pressed: W")