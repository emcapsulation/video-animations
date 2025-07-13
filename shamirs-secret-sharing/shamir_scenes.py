from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#120410"


class Shamir(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in Shamir and speech bubble
		shamir = Human(LIGHT_PINK, 0.8).add_label("Shamir", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(shamir))

		speech_bubble = SpeechBubble([PINK, LIGHT_PINK], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("This is Shamir's Secret Sharing.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		# Descriptions
		text_1 = Text("Splits any secret into n parts called shares.", font_size=20).move_to(UP)
		self.play(Write(text_1))
		self.wait(2)

		text_2 = Text("You select a threshold, k.", font_size=20).move_to(UP*0.5)
		self.play(Write(text_2))
		self.wait(2)


		# k shares description
		top_rect = SpeechBubble(GREEN, 10, 1.5).get_speech_bubble().move_to(DOWN)
		top_text = Text("≥ k shares reconstructs the secret.", font_size=20).move_to(top_rect.get_center())
		top = VGroup(top_rect, top_text)
		self.play(Create(top_rect), Write(top_text))
		self.wait(2)

		bot_rect = SpeechBubble(RED, 10, 1.5).get_speech_bubble().move_to(DOWN*3)
		bot_text = Text("< k shares are completely useless.", font_size=20).move_to(bot_rect.get_center())
		bot = VGroup(bot_rect, bot_text)
		self.play(Create(bot_rect), Write(bot_text))
		self.wait(2)


		# Slide both rectangles to the side
		self.play(
			top_rect.animate.set_width(7),
			bot_rect.animate.set_width(7)
		)
		self.play(
			top.animate.shift(LEFT*3),
			bot.animate.shift(LEFT*3)
		)
		self.wait(2)

		
		positions = [RIGHT*2+DOWN, RIGHT*4+DOWN, RIGHT*6+DOWN, RIGHT*2+DOWN*2, RIGHT*4+DOWN*2, RIGHT*6+DOWN*2]
		family = Family(0.8, 0.2, 1, positions)
		family_group = family.get_family_group()
		self.play(Create(family_group))

		n_is_6 = Text("n = 6", font_size=28).move_to(RIGHT*3 + DOWN*3)
		self.play(Write(n_is_6))
		self.wait(2)


		self.play(
			family.get_family_group_member("Uncle").animate.set_color(GRAY),
			family.get_family_group_member("Mum").animate.set_color(GRAY)
		)
		self.play(
			family.get_family_group_member("Uncle").animate.set_color(GOLD),
			family.get_family_group_member("Mum").animate.set_color(TEAL)
		)
		self.play(
			family.get_family_group_member("Grandpa").animate.set_color(GRAY),
			family.get_family_group_member("You").animate.set_color(GRAY)
		)
		self.play(
			family.get_family_group_member("Grandpa").animate.set_color(ORANGE),
			family.get_family_group_member("You").animate.set_color(PURPLE)
		)
		self.play(
			family.get_family_group_member("Dad").animate.set_color(GRAY),
			family.get_family_group_member("Mum").animate.set_color(GRAY)
		)


		k_is_4 = Text("k = 4", font_size=28).move_to(RIGHT*5 + DOWN*3)
		self.play(Write(k_is_4))
		self.wait(2)
