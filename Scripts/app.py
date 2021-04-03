import sys
sys.path.append('core/')

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, MATCH_TIME
from color import *
from window import Window
from event_channel import add_listener

from UI import UICanvas, Text

from timer import Timer
from timer_text import TimerText
from playground import Playground
from ball import Ball
from box_collider import BoxCollider

time_left_text = TimerText("02:00", 32, WHITE, (WINDOW_WIDTH // 2, 16))
score_text = Text("0 - 0", 32, WHITE, (WINDOW_WIDTH // 2, 48))

game_objects = [
	UICanvas([time_left_text, score_text]),
	Timer(MATCH_TIME),
	Playground(pygame.Rect(64, 80, WINDOW_WIDTH - 64 * 2, 864), 16, 320),
	Ball(32, (832, 482), YELLOW, True)
]

from event_names import game_over
add_listener(game_over, lambda _: print("Game Over"))
game = Window("Tiny Football", (WINDOW_WIDTH, WINDOW_HEIGHT), game_objects)
