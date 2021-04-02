import sys
sys.path.append('core/')

from config import WINDOW_WIDTH, WINDOW_HEIGHT, MATCH_TIME
from window import Window
from event_channel import trigger, add_listener

from UI import *

from timer import *
from timer_text import TimerText
from character import *

time_left_text = TimerText("02:00", 32, (255, 255, 255), (WINDOW_WIDTH // 2, 16))
score_text = Text("0 - 0", 32, (255, 255, 255), (WINDOW_WIDTH // 2, 48))

game_objects = [
	UICanvas([time_left_text, score_text]),
	Timer(MATCH_TIME),
	Mover()
]

from event_names import game_over
add_listener(game_over, lambda _: print("Game Over"))
game = Window("Tiny Football", (WINDOW_WIDTH, WINDOW_HEIGHT), game_objects)
