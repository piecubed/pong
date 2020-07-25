from __future__ import annotations

import math
import random
import threading
import time

import pygame.display
import pygame.draw

import pong_game.utils.theme as theme
from pong_game.app.main_screen import Main
from pong_game.utils.duration import Duration
from pong_game.utils.position import Coordinate, Position4


class Bouncer:
	__angle: float
	__magnitude: float

	__x: float
	__y: float

	wallAngle: float = 0

	@property
	def angle(self) -> float:
		return self.__angle

	
	@angle.setter
	def angle(self, angle: float) -> None:
		self.x = math.cos(math.radians(angle)) * self.__magnitude
		self.y = math.sin(math.radians(angle)) * self.__magnitude
		self.__angle = angle
		
	@property
	def x(self) -> float:
		return self.__x

	
	@x.setter
	def x(self, x: float) -> None:
		self.__magnitude = math.sqrt(x**2 + self.__y**2)
		self.__angle = math.tanh(self.__y/x)
		self.__x = x

	@property
	def y(self) -> float:
		return self.__y

	
	@y.setter
	def y(self, y: float) -> None:
		self.__magnitude = math.sqrt(self.__x**2 + y**2)
		self.__angle = math.tanh(y/self.__x)
		self.__y = y

	@property
	def magnitude(self) -> float:
		return self.__magnitude


	@magnitude.setter
	def magnitude(self, magnitude: float) -> None:
		self.x = math.cos(math.radians(self.__angle)) * magnitude
		self.y = math.sin(math.radians(self.__angle)) * magnitude
		self.__magnitude = magnitude

	def setCartesian(self, x: float, y: float) -> None:	
		self.__magnitude = math.sqrt(x**2 + y**2)
		self.__angle = math.tanh(y/x)
		self.__y = y
		self.__x = x
	
	def setPolar(self, magnitude: float, angle: float) -> None:
		self.x = math.cos(math.radians(angle)) * magnitude
		self.y = math.sin(math.radians(angle)) * magnitude
		self.__magnitude = magnitude
		self.__angle = angle

	def bounce(self,) -> None:
		angle = self.wallAngle + math.degrees(math.atan2(-math.sin(math.radians(self.__angle - self.wallAngle)), math.cos(math.radians(self.__angle - self.wallAngle))))
		magnitude = math.cos(math.radians(angle))/800 
		self.wallAngle = 0
		if math.sin(math.radians(angle)) * magnitude >= 600:
			self.wallAngle = 90
			magnitude = math.sin(math.radians(self.__angle))/600
		print(angle)
		self.setPolar(magnitude, angle)

class Ball:
	thread: threading.Thread
	main: Main
	gameDisplay: pygame.Surface
	bouncer = Bouncer()

	def init(self, main: Main) -> None:
		self.main = main
		self.gameDisplay = self.main.gameDisplay
		self.circleRect = pygame.draw.circle(self.gameDisplay, radius=10, center=(400,300), color=theme.green)
		thread = threading.Thread(target=self.loop, name='BallMainLoop')
		self.bouncer.setCartesian(400,300)
		thread.start()
	
	def moveTo(self, targetCoord: Coordinate, duration: Duration) -> None:
		startCoord = Coordinate(self.circleRect.centerx, self.circleRect.centery)
		currentCoord = Coordinate(startCoord.x, startCoord.y)

		diff = targetCoord - currentCoord
		pixelsPer10MillisecondY = (diff.y/duration.milliseconds)*10
		pixelsPer10MillisecondX = (diff.x/duration.milliseconds)*10
		
		for _ in range(duration.milliseconds//10):
			time.sleep(0.01)
			currentCoord += Coordinate(pixelsPer10MillisecondX, pixelsPer10MillisecondY)
			# if currentCoord.y <= 0 or currentCoord.y >= 600:
			# 	break
			pygame.draw.rect(self.gameDisplay, color=theme.black, rect=self.circleRect)
			self.circleRect = pygame.draw.circle(self.gameDisplay, radius=10, center=(currentCoord.x, currentCoord.y), color=theme.green)
		targetVector = pygame.math.Vector2(currentCoord.x, startCoord.y)
		targetVector.cross(pygame.math.Vector2(startCoord.x, currentCoord.y))


	def loop(self) -> None:
		time.sleep(4)
		side = True
		self.bouncer.angle = 90
		self.bouncer.bounce()
		print(self.bouncer.y)

		while True:
			self.moveTo(Coordinate(0 if side else 800, self.bouncer.y), Duration(milliseconds=1500))
			self.bouncer.bounce()

