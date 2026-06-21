from manim import *

from constants import DEFAULT_BACKGROUND, MONOSPACE_FONT

config.background_color = DEFAULT_BACKGROUND


class DrawAndGlowLetter(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		self.play(Write(Text("Thank you for watching!").shift(UP*2)))

		letter_e = Text("e", font_size=200, color=TEAL)
		self.play(Write(letter_e))

		letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
		glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
		self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
		self.play(FadeOut(letter_e_stroke, glow_effect))

		self.wait(3)