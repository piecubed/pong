from __future__ import annotations

import threading
import time

import pygame
import pygame.surface as surface

import pong_game.utils.theme as theme
from pong_game.utils.position import Coordinate, Position4


class Main:
	thread: threading.Thread
	gameDisplay: surface.Surface

	def init(self) -> None:
		from pong_game.app.ball import Ball

		self.gameDisplay = pygame.display.set_mode((800,600))
		self.gameDisplay.fill(theme.black)
		self.ball = Ball()
		self.ball.init(self)
		self.loop()
	
	def loop(self) -> None:
		pygame.draw.rect(
			surface=self.gameDisplay, 
			color=theme.red, 
			rect=Position4(
				topLeft=Coordinate(0, 0), 
				width=100, 
				height=50
			),
		)
		clock = pygame.time.Clock()
		while True:

			clock.tick(60)
			pygame.display.flip()
			

