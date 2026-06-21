from manim import *

class Table:
	def __init__(self, fill_opacity=0.8):
		self.table = self.make_table(fill_opacity)

	def make_table(self, fill_opacity):
		TABLE_WIDTH, TABLE_HEIGHT, LEG_HEIGHT = 3, 0.5, 1.5

		top = Rectangle(
			width=TABLE_WIDTH, height=TABLE_HEIGHT,
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=fill_opacity
		)

		leg_1 = Rectangle(
			width=TABLE_HEIGHT/2, height=LEG_HEIGHT,
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=fill_opacity
		)

		leg_2 = leg_1.copy()

		legs = VGroup(leg_1, leg_2).arrange(RIGHT, buff=1.75)

		return VGroup(top, legs).arrange(DOWN, buff=0)