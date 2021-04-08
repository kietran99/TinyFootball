from event_channel import trigger
from event_names import a_goal_scored
from game_object import GameObject
from ball import Ball

class Score(GameObject):
	def __init__(self,ball: Ball):
		self.__is_active = True
		self.__ball = ball
		trigger(a_goal_scored, self.__ball.goal_score())
	def update(self,delta):
		if not self.__is_active:
			return
		trigger(a_goal_scored,self.__ball.goal_score())
