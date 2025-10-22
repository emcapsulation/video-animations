from manim import *

from bit_manipulation import BinaryNumber, BitwiseTable, BitwiseSubtraction, fade_out_scene

config.background_color = "#140010"



class SameSign(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[LIGHT_PINK, PINK], stroke_color=[LIGHT_PINK, PINK],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #8: Check if two numbers have the same sign.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)