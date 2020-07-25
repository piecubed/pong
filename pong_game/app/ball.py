from __future__ import annotations

import threading
import time

import pygame.display
import pygame.draw
from pong_game.app.main_screen import Main
import pong_game.utils.theme as theme
from pong_game.utils.position import Position4, Coordinate
from pong_game.utils.duration import Duration
import math
import random

class Ball:
	thread: threading.Thread
	main: Main
	gameDisplay: pygame.Surface
	
	def init(self, main: Main) -> None:
		self.main = main
		self.gameDisplay = self.main.gameDisplay
		self.circleRect = pygame.draw.circle(self.gameDisplay, radius=10, center=(400,300), color=theme.green)
		thread = threading.Thread(target=self.loop, name='BallMainLoop')
		thread.start()
	
	def moveTo(self, targetCoord: Coordinate, duration: Duration) -> float:
		currentCoord = Coordinate(self.circleRect.centerx, self.circleRect.centery)
		diff = targetCoord-currentCoord
		pixelsPer10MillisecondY = (diff.y/duration.milliseconds)*10
		pixelsPer10MillisecondX = (diff.x/duration.milliseconds)*10
		print(duration.milliseconds)
		for _ in range(duration.milliseconds//10):
			time.sleep(0.01)
			currentCoord += Coordinate(pixelsPer10MillisecondX, pixelsPer10MillisecondY)
			pygame.draw.rect(self.gameDisplay, color=theme.black, rect=self.circleRect)
			self.circleRect = pygame.draw.circle(self.gameDisplay, radius=10, center=(currentCoord.x, currentCoord.y), color=theme.green)
			
		return 0
			
	def loop(self) -> None:
		side = True

		while True:
			self.moveTo(Coordinate(0 if side else 800, random.randint(0, 600)), Duration(milliseconds=1500))
			side = not side