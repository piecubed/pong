import pygame
from pong_game.app.main_screen import Main

def init() -> None:
	pygame.init()
	Main().init()