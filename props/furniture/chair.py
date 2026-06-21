from manim import *

class Chair:
	def __init__(self, fill_opacity=0.8, flipped=False):
		self.chair = self.make_chair(fill_opacity, flipped)

	def make_chair(self, fill_opacity, flipped):
		CHAIR_COLOUR = GRAY_D

		CHAIR_WIDTH, CHAIR_HEIGHT = 0.25, 2
		back = Rectangle(
			width=CHAIR_WIDTH, height=CHAIR_HEIGHT,
			stroke_color=CHAIR_COLOUR,
			fill_color=CHAIR_COLOUR,
			fill_opacity=fill_opacity
		)

		SEAT_WIDTH = 1.25
		seat = Rectangle(
			width=SEAT_WIDTH, height=CHAIR_WIDTH,
			stroke_color=CHAIR_COLOUR,
			fill_color=CHAIR_COLOUR,
			fill_opacity=fill_opacity
		)

		chair = VGroup(back, seat).arrange(DOWN, buff=0)
		back_shift = LEFT if not flipped else RIGHT
		back.shift(back_shift*(SEAT_WIDTH/2 - CHAIR_WIDTH/2))
		
		return chair