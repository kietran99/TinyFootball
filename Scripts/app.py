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
from character import Mover
from team import TeamOfPlayers,Players
from turn_manager import TurnManager
# from scoring_manager import Score_manager
from score_text import ScoreText
from score import Score

time_left_text = TimerText("02:00", 32, WHITE, (WINDOW_WIDTH // 2, 16))
score_text = ScoreText("0 - 0", 32, WHITE, (WINDOW_WIDTH // 2, 48))

pg = Playground(pygame.Rect(64, 80, WINDOW_WIDTH - 64 * 2, 864), 16, 320)
ball = Ball(32, (832, 482), YELLOW, False,pg.borders)
teamleft = TeamOfPlayers(ball,True)
teamright = TeamOfPlayers(ball,False)
turn_manager = TurnManager(teamleft, teamright)
# score_manager = Score_manager(ball)
game_objects = [
	UICanvas([time_left_text, score_text]),
	Timer(MATCH_TIME),
	Score(ball),
	pg,
	ball,
	turn_manager
	# Mover(10, (850,500))
]

from event_names import game_over
add_listener(game_over, lambda _: print("Game Over"))
game = Window("Tiny Football", (WINDOW_WIDTH, WINDOW_HEIGHT), game_objects)
