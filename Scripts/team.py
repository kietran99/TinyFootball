import pygame
from character import Mover

from core.box_collider import *

from game_object import GameObject
from utils import add_tuple

from core.Physics import Vector,magntude
from ball import Ball,collide_with


control_left_team = [
	pygame.K_w, #Move up	0
	pygame.K_s, #Move down	1	
	pygame.K_a, #Move left	2	
	pygame.K_d, #Move right	3
	pygame.K_i, #dir up		4
	pygame.K_k, #dir down	5
	pygame.K_j, #dir left	6
	pygame.K_l, #dir right	7
	pygame.K_q, #select 	8
	pygame.K_e, #deselect	9
	pygame.K_SPACE, #kick	10
	pygame.K_r #end turn
]

control_right_team = [
	pygame.K_UP,
	pygame.K_DOWN,
	pygame.K_LEFT,
	pygame.K_RIGHT,
	pygame.K_KP5,
	pygame.K_KP2,
	pygame.K_KP1,
	pygame.K_KP3,
	pygame.K_KP4,
	pygame.K_KP6,
	pygame.K_KP_ENTER,
	pygame.K_KP9
]


class Players(GameObject):
	def __init__(self,size ,speed:int,pos : (0,0),keycode, show_collider = False):
		self.__size = size
		self.__position = (pos[0] - size // 2, pos[1] - size // 2)
		self.__speed = speed
		self.__facing_dir = Vector(0, 1)
		self.__box_collider = BoxCollider((size * 2, size * 2), (self.__position[0] - size, self.__position[1] - size), show_collider)
		self.__selected = False
		self.ball = None
		self.holding_ball = False
		self.kicked = False
		self.__keycode = keycode
		self.__mover = Mover(speed, pos,self.__keycode)
	def box_collider(self):
		return self.__box_collider
		
	def update(self,delta):
		if self.__selected:
			print("Facing direction:" + str(self.__facing_dir))
			self.__mover.update(delta)	
			self.__position = self.__mover.pos
			self.__box_collider.set_pos(add_tuple(self.__position, (-self.__size, -self.__size)))
			if(self.ball != None):
				ball_pos = (self.__position[0]+self.__facing_dir.x * (self.__size + self.ball.size()+5), self.__position[1] + self.__facing_dir.y * (self.__size + self.ball.size() + 5) )
				self.ball.set_position(ball_pos) 
	
	def handle_input(self,event):
		self.__mover.handle_input(event)
		if event.type == pygame.KEYDOWN and self.__selected:
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[self.__keycode[10]] and self.holding_ball:
				self.kickBall()
				self.kicked = True
			if pressed_keys[self.__keycode[5]]:
				if pressed_keys[self.__keycode[6]]:
					self.__facing_dir = Vector(-1,1)
				elif pressed_keys[self.__keycode[7]]:
					self.__facing_dir = Vector(1,1)
				else: 
					self.__facing_dir = Vector(0,1)
			elif pressed_keys[self.__keycode[4]]:
				if pressed_keys[self.__keycode[6]]:
					self.__facing_dir = Vector(-1,-1)
				elif pressed_keys[self.__keycode[7]]:
					self.__facing_dir = Vector(1,-1)
				else: 
					self.__facing_dir = Vector(0,-1)
			elif pressed_keys[self.__keycode[6]]:
				if pressed_keys[self.__keycode[4]]:
					self.__facing_dir = Vector(-1,-1)
				elif pressed_keys[self.__keycode[5]]:
					self.__facing_dir = Vector(-1,1)
				else: 
					self.__facing_dir = Vector(-1,0)
			elif pressed_keys[self.__keycode[7]]:
				if pressed_keys[self.__keycode[4]]:
					self.__facing_dir = Vector(1,-1)
				elif pressed_keys[self.__keycode[5]]:
					self.__facing_dir = Vector(1,1)
				else: 
					self.__facing_dir = Vector(1,0)

	def render(self,window, in_turn):
		if in_turn:
			if self.__selected:
				pygame.draw.circle(window, (255,0,0), self.__position, self.__size)
			else: pygame.draw.circle(window, (0,0,255), self.__position, self.__size)
		else: pygame.draw.circle(window, (255,255,255), self.__position, self.__size)
		self.__box_collider.render(window)


	def getBall(self,ball : Ball):
		self.ball = ball
		self.ball.stop()
		
	
	def selectPlayer(self):
		self.__selected = True
	def deselect(self):
		self.__selected = False
	def set_position(self,new_pos):
		self.__position = new_pos
	def get_position(self):
		return self.__position
        
    

	def kickBall(self):
		if(self.ball != None):
			self.ball.kicked(Vector(500 * self.__facing_dir.x, 500 * self.__facing_dir.y))
			self.ball = None


class TeamOfPlayers(GameObject):
	def __init__(self,ball : Ball,leftTeam = False):
		self.__leftTeam  = leftTeam
		if(leftTeam):
			self.__keycode = control_left_team
		else:
			self.__keycode = control_right_team	
		if not leftTeam:
			self.__players = [
				Players(64,50,(1000, 500),self.__keycode),
				Players(64,50, (900,200),self.__keycode),
				Players(64,50, (1100, 450),self.__keycode)
			]
		else:
			self.__players = [
				Players(64,50,(400, 500),self.__keycode),
				Players(64,50, (300,200),self.__keycode),
				Players(64,50, (200, 450),self.__keycode)
			]
		self.active_Player = -1
		self.__selector  = 0
		self.__score = 0
		self.__ball = ball
		self.__selector_sprite = None
		self.__has_turn = False
		self.__has_ball = False
		self.__can_walk = (	self.__ball.borders[2].position()[0] + self.__ball.borders[2].size()[0], 
							self.__ball.borders[3].position()[0], 
							self.__ball.borders[0].position()[1] + self.__ball.borders[0].size()[1], 
							self.__ball.borders[1].position()[1])

	def auto_end_turn(self):
		if self.__selector < 0:
			return False
		return self.__players[self.__selector].kicked
	def done_auto_end_turn(self):
		if self.__selector >=0:
			self.__players[self.__selector].kicked
	def gain_turn(self):
		self.__has_turn = True
	def end_turn(self):
		self.__has_turn = False
	def has_ball(self):
		return self.__has_ball
	def lose_ball(self):
		self.__has_ball = False
	def force_kick(self):
		for player in self.__players:
			if player.holding_ball:
				player.kickBall()
				player.kicked = True

	def update(self,delta):
		# if self.__has_turn
		for player in self.__players:
			player.update(delta)
			pos = player.get_position()
			if pos[0] < self.__can_walk[0] :
				player.set_position((self.__can_walk[0],pos[1]))
			if pos[0] > self.__can_walk[1]:
				player.set_position((self.__can_walk[1],pos[1]))
			if pos[1] < self.__can_walk[2] :
				player.set_position((pos[0],self.__can_walk[2]))
			if pos[1]  > self.__can_walk[3]:
				player.set_position((pos[0],self.__can_walk[3]))
		# if not self.__has_ball:
		# 	for player in self.__players:
		# 		if collide_with(self.__ball.box_collider() , player.box_collider()):
		# 			self.__has_ball = True
		# 			player.getBall(self.__ball)
		# 			if self.__has_turn:
		# 				player.kickBall()
		# 			else:
		# 				player.holding_ball = True
		# 			break
		# if self.__has_ball:
		# 	for player in self.__players:
		# 		if collide_with(self.__ball.box_collider() , player.box_collider()):
		# 			player.kickBall()

		if self.__has_turn:
			if self.__has_ball:
				for player in self.__players:
					if(collide_with(self.__ball.box_collider(), player.box_collider())):
						player.getBall(self.__ball)
						if not player.holding_ball:
							player.kickBall()
							
			else:
				for player in self.__players:
					if(collide_with(self.__ball.box_collider(), player.box_collider())):
						self.__has_ball = True
						player.holding_ball = True
						player.getBall(self.__ball)
						break

		else:
			for player in self.__players:
				if(collide_with(self.__ball.box_collider(), player.box_collider())):
					self.__has_ball = True
					player.holding_ball = True
					player.getBall(self.__ball)
					break

		# else:
		# 	for player in self.__players:
		# 		if collide_with(ball.box_collider() , player.box_collider()):
		if not self.__has_turn:
			self.active_Player = -1
			for player in self.__players:
				player.deselect()
		# goal = self.__ball.goal()
		# if goal[0]:
		# 	if(goal[1] and self.__leftTeam):
		# 		self.__score +=1
		# 		self.__ball.de_goal()
		
	def render(self,window):
		for player in self.__players :
			player.render(window,self.__has_turn)

	def handle_input(self,event):
		for player in self.__players:
			player.handle_input(event,)
		if event.type == pygame.KEYDOWN:
			pressed_keys = pygame.key.get_pressed()
			if self.active_Player == -1:
				if pressed_keys[self.__keycode[3]]:
					self.__selector += 1
					if self.__selector >= len(self.__players):
						self.__selector = 0
			if pressed_keys[self.__keycode[8]]:
				self.active_Player = self.__selector
				self.__players[self.__selector].selectPlayer()
			if pressed_keys[self.__keycode[9]]:
				self.active_Player = -1
				self.__players[self.__selector].deselect()