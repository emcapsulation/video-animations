from manim import *

class Lock:
	def __init__(self, colour):
		self.colour = colour
		self.lock = self.make_lock()


	def get_lock(self):
		return self.lock


	def make_lock(self):
		annulus = Annulus(inner_radius=0.5, outer_radius=1, color=self.colour)

		back = RoundedRectangle(
			width=2.25, height=2,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=self.colour,
			fill_color=self.colour,
			fill_opacity=1
		)

		keyhole_1 = Dot(
			radius=0.25,
			color=BLACK
		)

		keyhole_2 = Rectangle(
			width=0.2, height=0.25,
			color=BLACK, fill_color=BLACK,
			fill_opacity=1
		).move_to(keyhole_1.get_center()+DOWN*0.25)

		keyhole = VGroup(keyhole_1, keyhole_2)

		return VGroup(annulus, back.move_to(annulus.get_center()+DOWN), keyhole.move_to(back.get_center())).scale(0.3)
