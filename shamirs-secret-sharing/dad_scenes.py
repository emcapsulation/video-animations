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



class LagrangeGetSecret(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in dad and speech bubble
		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(dad))

		speech_bubble = SpeechBubble([GREEN_B, GREEN], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("We plug in x = 0 to recover the key.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))


		points = [(1, 4), (2, 0), (4, 1), (6, 5)]
		colours = [ORANGE, GOLD, TEAL, PURPLE]


		polynomial_terms = VGroup()
		font_size, end = 24, 4


		def create_full_term(i, plug_in=False):
			box_num = 2*i + 1
			
			text = "\\frac{"
			for j in range(0, end):
				if j != i:
					if plug_in == False:
						text += f"(x-{points[j][0]})"
					else:
						text += f"({plug_in}-{points[j][0]})"
			text += "}{"
			for j in range(0, end):
				if j != i:
					text += f"({points[i][0]}-{points[j][0]})"
			text += "}"

			text += f"\\cdot {points[i][1]}"

			if len(polynomial_terms) > box_num:
				this_term = MathTex(text, font_size=font_size, color=colours[i]).move_to(polynomial_terms[box_num].get_center())
				self.play(Transform(polynomial_terms[box_num], this_term))
			else:
				this_term = MathTex(text, font_size=font_size, color=colours[i])
				polynomial_terms.add(this_term)

			self.wait(2)


		# Draw the polynomial
		px = MathTex("P(x) = ", font_size=font_size)
		polynomial_terms.add(px)

		for i in range(0, 4):
			create_full_term(i, plug_in=False)

			if i != 3:
				plus = MathTex("+", font_size=font_size)
				polynomial_terms.add(plus)

		polynomial_terms.arrange(RIGHT)

		for i in range(0, len(polynomial_terms)):
			self.play(Write(polynomial_terms[i]))


		# Plug in 0
		p0 = MathTex("P(0) = ", font_size=font_size).move_to(polynomial_terms[0].get_center())
		self.play(Transform(polynomial_terms[0], p0))

		for i in range(0, 4):
			box_num = 2*i + 1

			plug_in = 0
			create_full_term(i, plug_in=str(plug_in))

			numerator, denominator = 1, 1

			text = "\\frac{"
			for j in range(0, end):
				if j != i:
					numerator *= (plug_in-points[j][0])			
					text += f"({plug_in-points[j][0]})"
			text += "}{"
			for j in range(0, end):
				if j != i:
					denominator *= (points[i][0]-points[j][0])
					text += f"({points[i][0]-points[j][0]})"
			text += "}"

			text += f"\\cdot {points[i][1]}"

			this_term = MathTex(text, font_size=font_size, color=colours[i]).move_to(polynomial_terms[box_num].get_center())
			self.play(Transform(polynomial_terms[box_num], this_term))
			self.play(polynomial_terms.animate.arrange(RIGHT))


			text = "\\frac{%d}{%d}" % (numerator, denominator)
			text += f"\\cdot {points[i][1]}"

			this_term = MathTex(text, font_size=36, color=colours[i]).move_to(polynomial_terms[box_num].get_center())
			self.play(Transform(polynomial_terms[box_num], this_term))
			self.play(polynomial_terms.animate.arrange(RIGHT))


			this_term = MathTex("\\frac{%d}{%d}" % (numerator*points[i][1], denominator), font_size=36, color=colours[i]).move_to(polynomial_terms[box_num].get_center())
			self.play(Transform(polynomial_terms[box_num], this_term))
			self.play(polynomial_terms.animate.arrange(RIGHT))


		polynomial_ans = MathTex("P(0) = \\frac{64}{5}", font_size=36)
		self.play(Transform(polynomial_terms, polynomial_ans))
		self.wait(2)
			
		speech2 = Text("But our secret key is 3?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)