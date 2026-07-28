from manim import *

class HintBox:
	def __init__(self, text, colour, y_pos=0):
		self.text = text
		self.box = self.make_box(text, colour, y_pos)

	def make_box(self, text, colour, y_pos):
		rect = Rectangle(
			width=14.5, height=1.5, 
			fill_color=colour, fill_opacity=0.05, 
			stroke_color=colour, stroke_width=0.5
		).to_edge(UP, buff=0).shift(DOWN*y_pos)
		return VGroup(rect, text.move_to(rect.get_center()))

	def init_lbl(self):
		return [FadeIn(self.box[0]), AddTextLetterByLetter(self.box[1])]

	def change_text(self, new_text):
		return Transform(self.text, new_text.move_to(self.box.get_center()))