from event_channel import add_listener
from event_names import a_second_passed
from UI import Text

class TimerText(Text):
	def __init__(self, text, size, color, pos):
		super().__init__(text, size, color, pos)
		add_listener(a_second_passed, self.__show_current_time)

	def __show_current_time(self, cur_time_milsec):
		min = cur_time_milsec // 60000
		# print("Min: " + str(min))
		sec = cur_time_milsec % 60000 // 1000
		# print("Sec: " + str(sec))
		self.text = self._format_num(min) + ":" + self._format_num(sec)