from event_channel import add_listener
from event_names import a_goal_scored
from UI import Text
from ball import Ball

class ScoreText(Text):
	def __init__(self, text, size, color, pos):
		super().__init__(text, size, color, pos)
		# self.__ball = ball
		# self.__lef_team_score = 0
		# self.__right_team_score = 0
		add_listener(a_goal_scored, self.__show_current_score)

	def __show_current_score(self, goal_score):
		# min = cur_time_milsec // 60000
		# # print("Min: " + str(min))
		# sec = cur_time_milsec % 60000 // 1000
		# # print("Sec: " + str(sec))
		self.text = str(goal_score[0]) + " - " + str(goal_score[1])