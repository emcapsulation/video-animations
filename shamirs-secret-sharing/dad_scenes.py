from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#070d05"


class SplitKeyIdea(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in dad and speech bubble
		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(dad))

		speech_bubble = SpeechBubble([GREEN_B, GREEN], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("What if we split the key into six pieces?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))


		# Split the key
		key_text = Text("super_secret_key_1")
		self.play(Write(key_text))
		self.wait(2)

		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		key_text_copy = key_text.copy()
		for i in range(0, len(key_text_copy.get_text()), 3):
			key_text_copy[i:i+3].set_color(colours[i//3])


		# Draw in each member of the family
		y_pos = DOWN*3
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.4, 0.8, positions)
		family_group = family.get_family_group()

		self.play(
			Transform(key_text, key_text_copy),
			Create(family_group)
		)


		# Move the part of the key above the family member
		part_of_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			part_of_key_anim.append(
				key_text[i:i+3].animate.move_to(family_group[i//3].get_center()+UP*1.2).scale(0.5)
			)

		self.play(*part_of_key_anim)
		self.wait(2)


		# Competitor cannot decrypt the recipe
		competitor = Human(MAROON_D, 0.8).get_human().scale(0.2).move_to(LEFT*4)
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().scale(0.7)
		self.play(
			Create(secret_sauce_encrypted),
			Create(competitor)
		)

		self.play(key_text[0:0+3].animate.move_to(competitor.get_right()))

		competitor_and_key = VGroup(competitor, key_text[0:0+3])
		self.play(
			competitor_and_key.animate.move_to(secret_sauce_encrypted.get_left())
		)

		self.play(Wiggle(secret_sauce_encrypted), competitor_and_key.animate.move_to(LEFT*4))
		self.wait(2)

		self.play(competitor.animate.shift(LEFT*8))


		# Combine the key parts to get the full key back
		combine_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			combine_key_anim.append(
				key_text[i:i+3].animate.move_to(LEFT*5).shift(RIGHT*i/5)
			)

		self.play(*combine_key_anim)
		self.wait(2)


		# Decrypt the recipe
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().scale(0.7)
		self.play(
			key_text.animate.move_to(secret_sauce_encrypted.get_left())
		)
		self.play(key_text.animate.move_to(LEFT*4),
			Transform(secret_sauce_encrypted, secret_sauce_plaintext)
		)
		self.wait(2)


		# Give the key parts back
		part_of_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			part_of_key_anim.append(
				key_text[i:i+3].animate.move_to(family_group[i//3].get_center()+UP*1.2)
			)

		self.play(*part_of_key_anim)
		self.wait(2)