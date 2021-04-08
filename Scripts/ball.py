import pygame

from core.Physics import *


from game_object import GameObject
from utils import add_tuple

from box_collider import BoxCollider
from character import Mover

from playground import Rectangle

def collide_with(self, other : BoxCollider):
	if(self.pos[0] + self.size[0] < other.pos[0] or other.pos[0] + other.size[0] < self.pos[0]):
		return False
	if(self.pos[1] + self.size[1] < other.pos[1] or other.pos[1] + other.size[1] < self.pos[1]):
		return False
	return True

class Ball(GameObject):
	def __init__(self, size: int, pos: (0, 0), color = (255, 255, 255), show_collider = False, borders = list[Rectangle]):
		self.__size = size
		self.__pos = (pos[0] - size // 2, pos[1] - size // 2)
		self.__color = color
		self.__box_collider = BoxCollider((size * 2, size * 2), (self.__pos[0] - size, self.__pos[1] - size), show_collider)
		self.__mover = Mover(10, self.__pos)
		self.__speed = Vector(000, 000)
		self.borders = borders
		self.__goal = (0,0)
		# print("num of borders: " +str(len(borders)))
	def stop(self):
		self.__speed = Vector(0,0)
	def kicked(self, speed:Vector):
		self.__speed = speed
	def position(self):
		return self.__pos
	def box_collider(self):
		return self.__box_collider
	def set_position(self, pos):
		self.__pos = pos

	def update(self, delta):	
		goal_bound = (	self.borders[2].position()[0] + self.borders[2].size()[0], 
						self.borders[3].position()[0], 
						self.borders[2].position()[1] + self.borders[2].size()[1], 
						self.borders[4].position()[1])
		print(str(self.__goal))
		if (self.__pos[0] < goal_bound[0] or self.__pos[0] > goal_bound[1]) and (self.__pos[1] < goal_bound[3] and self.__pos[1] > goal_bound[2]):
			print("goal")
			if(self.__pos[0] < goal_bound[0]):
				self.__goal =(self.__goal[0], self.__goal[1]+1)
			else: 
				self.__goal = (self.__goal[0]+1, self.__goal[1]) 
			self.__speed = Vector(0,0)
			self.__pos = ((goal_bound[1]- goal_bound[0])/2,self.__pos[1])
		if(self.__speed.x != 0 or self.__speed.y != 0):
			for border in self.borders:
				if(collide_with(self.__box_collider,border.box_collider)):
					# print("ball: " + str(self.__box_collider.pos) + "\n size: "+ str(self.__box_collider.size))
					# print("border: " + str(border.position()) + "\n size: " + str(border.size()))
					# print("ingoing Speed: "+ str(self.__speed))
					self.__speed = reflect(self.__speed, Vector(border.perp_vector[0], border.perp_vector[1]))
					# print("outgoing speed: " + str(self.__speed))
					break
			self.__pos = (self.__pos[0] + self.__speed.x /delta , self.__pos[1] + self.__speed.y / delta)
			speed = magntude(self.__speed)
			x = self.__speed.x * (speed - 9.81*FRICTION_CO*(1/delta))/speed
			y = self.__speed.y * (speed - 9.81*FRICTION_CO*(1/delta))/speed
			self.__speed = Vector(x, y)
			if(x < 1 and x > -1):
				# print("x = 0")
				self.__speed = Vector(0, y)
			if(y < 1 and y > -1):
				self.__speed = Vector(x, 0)

		# else:
		# 	self.__mover.update(delta)	
		# 	self.__pos = self.__mover.pos
		self.__box_collider.set_pos(add_tuple(self.__pos, (-self.__size, -self.__size)))

	def goal_score(self):
		return self.__goal

	def handle_input(self, event):
		self.__mover.handle_input(event)

	def render(self, window):
		pygame.draw.circle(window, self.__color, self.__pos, self.__size)
		self.__box_collider.render(window)

	def size(self):
		return self.__size