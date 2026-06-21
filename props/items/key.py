from manim import *

class Key:
	def __init__(self, colour):
		self.colour = colour
		self.key = self.make_key()


	def get_key(self):
		return self.key


	def make_key(self):
		annulus = Annulus(inner_radius=0.5, outer_radius=1, color=self.colour)

		stick = RoundedRectangle(
			width=2.5, height=0.5,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=self.colour,
			fill_color=self.colour,
			fill_opacity=1
		)

		little_stick = RoundedRectangle(
			width=0.25, height=1,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=self.colour,
			fill_color=self.colour,
			fill_opacity=1
		)

		little_sticks = VGroup(little_stick, little_stick.copy()).arrange(RIGHT)

		key = VGroup(
			annulus,
			stick.move_to(annulus.get_center() + RIGHT*1.8),
			little_sticks.move_to(stick.get_right() + LEFT*0.5+DOWN*0.4)
		)

		return key