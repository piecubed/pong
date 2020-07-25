import enum
from typing import Tuple

import pygame


class Coordinate:
	x: float
	y: float

	def __init__(self, x: float, y: float) -> None:
		# assert x >= 0
		# assert y >= 0

		self.x = x
		self.y = y

	def __tuple__(self) -> Tuple[float, float]:
		return (self.x, self.y)

	def __str__(self) -> str:
		return f'({self.x}, {self.y})'

	def __add__(self, other: 'Coordinate') -> 'Coordinate':
		return Coordinate(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: 'Coordinate') -> 'Coordinate':
		return Coordinate(self.x - other.x, self.y - other.y)

class Position4:
	"""
	Shape drawing tool.
	===================

	+ Calculates dimensions of a shape based on one coord and height/width.
	+ Can be converted to shapes.
	"""

	topLeft: Coordinate
	topRight: Coordinate
	bottomLeft: Coordinate
	bottomRight: Coordinate
	__height: float
	__width: float
	rect: pygame.Rect

	def __init__(self, *, topLeft: Coordinate, height: float, width: float):
		assert height >= 0
		assert width >= 0

		self.topLeft = topLeft
		self.topRight = topLeft + Coordinate(width, 0)
		self.bottomLeft = topLeft + Coordinate(0, height)
		self.bottomRight = topLeft + Coordinate(width, height)
		self.__height = height
		self.__width = width
		self.rect = pygame.Rect((self.topLeft.x, self.topLeft.y, self.__width, self.__height))
