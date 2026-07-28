from manim import *


class CodeBlock:
	def __init__(self, lines, font_size=16, t2c={}, pos=ORIGIN, stroke_colour=GRAY, fill_colour=BLACK, corner_radius=0.1, arrow_colour=TEAL):
		self.lines = lines
		self.code_block = self.make_code_block(font_size, t2c, pos, stroke_colour, fill_colour, corner_radius)
		self.arrow = Triangle(fill_color=arrow_colour, fill_opacity=1, stroke_width=0).scale(0.15).rotate(270*DEGREES).next_to(self.line_group[0], LEFT)

	def make_code_block(self, font_size, t2c, pos, stroke_colour, fill_colour, corner_radius):
		self.line_group = VGroup(*[Text(line, font_size=font_size, t2c=t2c) for line in self.lines])
		self.line_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)

		background = SurroundingRectangle(
			self.line_group,
			stroke_color=stroke_colour, 
			fill_color=fill_colour,
			fill_opacity=1,
			corner_radius=corner_radius,
			buff=0.25
		)
		return VGroup(background, self.line_group).move_to(pos)

	def move_arrow_to_line(self, line_num):
		return self.arrow.animate.next_to(self.line_group[line_num], LEFT)