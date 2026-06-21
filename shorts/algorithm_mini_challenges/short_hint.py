from manim import *

class ShortHint:
	def __init__(self, scene, text, font_size=24):
		self.scene = scene
		self.background_rectangle = self.get_background_rectangle()
		self.hint = self.init_hint(text, font_size=font_size)

	def init_hint(self, text, font_size=24):
		hint_text = Text(text, font_size=font_size)
		hint = VGroup(self.background_rectangle, hint_text.move_to(self.background_rectangle.get_center()))
		return hint

	def get_background_rectangle(self):
		return Rectangle(width=10, height=2, fill_color=WHITE, fill_opacity=0.2, stroke_width=0).move_to(UP*7)

	def create_hint(self):
		self.scene.play(Create(self.hint))

	def change_hint(self, new_text, font_size=24):
		hint_text_2 = Text(new_text, font_size=font_size)
		hint_2 = VGroup(self.background_rectangle, hint_text_2.move_to(self.background_rectangle.get_center()))
		self.scene.play(Transform(self.hint, hint_2))


