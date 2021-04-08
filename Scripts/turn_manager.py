import pygame
from team import TeamOfPlayers,Players
from core.game_object import GameObject
class TurnManager(GameObject):
	def __init__(self, left_team : TeamOfPlayers,right_team: TeamOfPlayers):
		self.__leftTeam = left_team
		self.__rightTeam = right_team
		self.__turn_for_left_team = True
	def update(self, delta):
		if self.__turn_for_left_team :
			self.__rightTeam.end_turn()
			self.__leftTeam.gain_turn()
			if self.__rightTeam.has_ball():
				self.__leftTeam.lose_ball()
			# if self.__leftTeam.auto_end_turn():
				self.__turn_for_left_team = not self.__turn_for_left_team
				self.__leftTeam.done_auto_end_turn()
		else :
			self.__leftTeam.end_turn()
			self.__rightTeam.gain_turn()
			if self.__leftTeam.has_ball():
				self.__rightTeam.lose_ball()
			# if self.__rightTeam.auto_end_turn():
				self.__turn_for_left_team = not self.__turn_for_left_team
				self.__rightTeam.done_auto_end_turn()
		self.__leftTeam.update(delta)
		self.__rightTeam.update(delta)
	def handle_input(self, event):
		if self.__turn_for_left_team:
			self.__leftTeam.handle_input(event)
		else: 
			self.__rightTeam.handle_input(event)
		if event.type == pygame.KEYDOWN:
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[pygame.K_BACKSPACE]:
				self.__turn_for_left_team = not self.__turn_for_left_team
				# self.__rightTeam.force_kick()
				# self.__leftTeam.force_kick()

	def render(self, window):
		self.__leftTeam.render(window)
		self.__rightTeam.render(window)