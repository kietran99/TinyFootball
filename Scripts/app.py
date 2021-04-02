import sys
sys.path.append('core/')

from config import WINDOW_WIDTH, WINDOW_HEIGHT
from window import Window

from UI import *

time_left_text = Text("02:00", 32, (255, 255, 255), (300, 16))
score_text = Text("0 - 0", 32, (255, 255, 255), (300, 48))

game_objects = [
	UICanvas([time_left_text, score_text])
]

game = Window("Tiny Football", (WINDOW_WIDTH, WINDOW_HEIGHT), game_objects)