from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#faf5e8"


class Recap(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce_with_background().shift(RIGHT*2)
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce_with_background().shift(RIGHT*2)

		key = Key(LIGHT_BROWN).get_key().scale(0.6).move_to(LEFT*2)

		self.play(Create(secret_sauce_plaintext))
		self.play(Create(key))


		# Key encrypts the plaintext
		self.play(key.animate.move_to(secret_sauce_encrypted.get_center()))
		self.play(key.animate.move_to(LEFT*2), Transform(secret_sauce_plaintext, secret_sauce_encrypted))
		self.wait(2)

		positions = [LEFT*5+UP*3, LEFT*5, LEFT*5+DOWN*3, RIGHT*5+UP*3, RIGHT*5, RIGHT*5+DOWN*3]
		family = Family(0.8, 0.4, 1, positions)
		family.set_label_colour(BLACK)
		family_group = family.get_family_group()
		self.play(Create(family_group))


		# A key gets divvied out to everyone
		small_key = Key(LIGHT_BROWN).get_key().scale(0.2).move_to(key.get_center())
		small_keys = VGroup(small_key, small_key.copy(), small_key.copy(), small_key.copy(), small_key.copy(), small_key.copy())

		key_go_anim = []
		for i in range(len(small_keys)):
			key_go_anim.append(small_keys[i].animate.move_to(family_group[i].get_center()))
		self.play(*key_go_anim)
		self.wait(2)


		# Competitor steals one
		competitor = Human(MAROON_D, 0.8).get_human().move_to(RIGHT*8 + UP*2).scale(0.3)
		self.play(competitor.animate.move_to(family_group[4].get_right()))
		self.play(competitor.animate.shift(RIGHT*3 + UP*2), small_keys[4].animate.shift(RIGHT*3 + UP*2))
		self.wait(2)

		red_x = Text("X", color=RED, font_size=72)
		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))
		self.play(FadeOut(small_keys))


		# Six fragments get split
		fragments = VGroup()
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(family_group)):
			fragments.add(Dot(radius=0.2, color=colours[i]).move_to(LEFT*3+RIGHT*i/3))
		self.play(Transform(key, fragments))


		fragments_copy = fragments.copy()
		left_or_right = [LEFT, RIGHT]
		for i in range(0, len(family_group)):
			self.play(fragments_copy[i].animate.move_to(family_group[i].get_center() + left_or_right[i//3 == 0]))
		self.wait(2)


		# Someone loses their part
		self.play(fragments_copy[3].animate.shift(UP*2 + RIGHT*3))

		make_key_again = []
		for i in range(0, len(fragments_copy)):
			if i != 3:
				make_key_again.append(fragments_copy[i].animate.move_to(DOWN+LEFT*3+RIGHT*i/3))
		self.play(*make_key_again)
		self.wait(2)

		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))



class Recap2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title_text = Text("Problem Recap", color=BLACK).shift(UP*3)
		self.play(Write(title_text))

		text = Text("""
Each family member gets some kind\n
of piece of the key. But not the\n
whole key - just a piece which is\n
useless on its own.\n\n
The original key should be recoverable\n
if ANY four family members bring their\n
parts together.\n\n
But, no subset of family members less\n
than size four can reconstruct the key,\n
or even learn any information.
""", 
			font_size=18, color=BLACK).move_to(DOWN*0.6+LEFT*4)
		self.play(Write(text), run_time=20)
		self.wait(2)


		positions = [UP*2, RIGHT*2.5+UP*2, RIGHT*5+UP*2, DOWN*3, RIGHT*2.5+DOWN*3, RIGHT*5+DOWN*3]
		family = Family(0.8, 0.2, 1, positions)
		family.set_label_colour(BLACK)
		family_group = family.get_family_group()
		
		key = Key(LIGHT_BROWN).get_key().scale(0.5).move_to(RIGHT*2.5)
		self.play(Create(family_group), Create(key))
		self.wait(2)


		fragments = VGroup()
		colours = [ORANGE, GOLD, GREEN, TEAL]
		for i in range(0, len(colours)):
			fragments.add(Dot(radius=0.2, color=colours[i]).move_to(RIGHT*2+RIGHT*i/3))
		self.play(ReplacementTransform(key, fragments))
		fragments.add(fragments[0].copy(), fragments[1].copy())
		self.wait(2)


		fragments_copy = fragments.copy()
		up_or_down = [UP, DOWN]
		for i in range(0, len(fragments_copy)):
			self.play(fragments_copy[i].animate.move_to(family_group[i].get_center() + up_or_down[i//3 == 0]))
		self.wait(2)


		self.play(Flash(fragments_copy[0], color=ORANGE), Flash(fragments_copy[4], color=ORANGE))
		self.play(Flash(fragments_copy[1], color=GOLD), Flash(fragments_copy[5], color=GOLD))
		self.wait(2)


		self.play(fragments_copy[0].animate.move_to(DOWN+RIGHT*2+RIGHT*0/3))
		self.play(fragments_copy[1].animate.move_to(DOWN+RIGHT*2+RIGHT*1/3))
		self.play(fragments_copy[3].animate.move_to(DOWN+RIGHT*2+RIGHT*3/3))
		self.play(fragments_copy[5].animate.move_to(DOWN+RIGHT*2+RIGHT*1/3))
		self.wait(2)


		red_x = Text("X", color=RED, font_size=72)
		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))
		self.wait(2)


		key = Key(LIGHT_BROWN).get_key().scale(0.5).move_to(RIGHT*2.5 + DOWN*0.5)
		self.play(FadeIn(key), FadeOut(fragments), FadeOut(fragments_copy))
		self.wait(5)
