class Duration:
	milliseconds: int
	
	def __init__(self, seconds: int = 0, milliseconds: int = 0) -> None:
		self.milliseconds = milliseconds + (seconds * 1000)