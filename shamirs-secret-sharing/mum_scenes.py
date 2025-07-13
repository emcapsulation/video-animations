from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#011112"


class AnyFourPutTogetherParts(Scene):
	
	def construct(self):
		Text.set_default(font="Monospace")


		# Draw in each member of the family and key parts
		y_pos = DOWN*0.37
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family_group = family.get_family_group()

		dots = VGroup()
		for i in range(0, len(family_group)):
			dot = Dot(color=family.colours[i], radius=0.2).move_to(family_group[i].get_center()+DOWN*1.1)
			dots.add(dot)			

		self.add(family_group, dots)


		combine_parts_anim, grey_out_anim = [], []
		random_members = random.sample([0, 1, 2, 3, 4, 5], 4)

		random_dots = VGroup()
		for i in range(0, len(family_group)):
			if i in random_members:
				random_dots.add(dots[i])
				combine_parts_anim.append(dots[i].animate.move_to(UP))
			else:
				grey_out_anim.append(family_group[i].animate.set_color(GRAY_A))
				grey_out_anim.append(dots[i].animate.set_color(GRAY_A))

		self.play(*grey_out_anim)
		self.play(*combine_parts_anim)

		key = Key(YELLOW).get_key().move_to(UP).scale(0.3)
		self.play(ReplacementTransform(random_dots, key))
		self.play(FadeOut(key))