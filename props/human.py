from manim import *

class Human:
	def __init__(self, colour, fill_opacity=0.8):
		self.colour = colour
		self.fill_opacity = fill_opacity
		self.human = self.make_human()


	def get_human(self):
		return self.human

	def get_body(self):
		return self.human[0]

	def get_label(self):
		return self.human[1]


	def make_human(self):
		head = Circle(color=self.colour, fill_opacity=self.fill_opacity, radius=1)
		body = Arc(color=self.colour, fill_opacity=self.fill_opacity, radius=1.5, angle=PI)
		human = VGroup(head, body).arrange(DOWN)

		return VGroup(human)


	def add_label(self, label, label_colour=WHITE):
		label = Text(label, font_size=30, color=label_colour).next_to(self.human, UP)
		self.human.add(label)

		return self