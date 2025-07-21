from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#021a1c"


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



class SimultaneousEquations(Scene):
	
	def construct(self):
		Text.set_default(font="Monospace")


		# Draw in mum and speech bubble
		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).get_human().scale(0.4).move_to(RIGHT*5+UP*2.5)
		self.play(Create(mum))

		speech_bubble = SpeechBubble([TEAL, BLUE], 9, 1.5).get_speech_bubble().move_to(LEFT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("We are missing a pretty important step.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		# Write four points and plug them in
		point_text = Text("(1, 4), (2, 0), (4, 1), (6, 5)", 
			font_size=24, 
			t2c={"(1, 4)": ORANGE, "(2, 0)": GOLD, "(4, 1)": TEAL, "(6, 5)": PURPLE}).move_to(UP)
		self.play(Write(point_text))
		self.wait(2)

		general = MathTex("y = ax^{3} + bx^{2} + cx + d").next_to(point_text, DOWN)
		self.play(Write(general))		

		# Solve simultaneously
		sub_eq = MathTex("4", "=", "a", "\\cdot", "1", "^{3}", "+", "b", "\\cdot", "1", "^{2}", "+", "c", "\\cdot", "1", "+", "d", "\\quad", "(1)", font_size=24)
		sub_eq.set_color_by_tex("4", ORANGE)
		sub_eq.set_color_by_tex("1", ORANGE)
		sub_eq.next_to(general, DOWN, buff=0.5)
		self.play(Write(sub_eq))

		sub_eq_2 = MathTex("0", "=", "a", "\\cdot", "2", "^{3}", "+", "b", "\\cdot", "2", "^{2}", "+", "c", "\\cdot", "2", "+", "d", "\\quad", "(2)", font_size=24)
		sub_eq_2.set_color_by_tex("0", GOLD)
		sub_eq_2.set_color_by_tex("2", GOLD)
		sub_eq_2.next_to(sub_eq, DOWN, buff=0.5)
		self.play(Write(sub_eq_2))

		sub_eq_3 = MathTex("1", "=", "a", "\\cdot", "4", "^{3}", "+", "b", "\\cdot", "4", "^{2}", "+", "c", "\\cdot", "4", "+", "d", "\\quad", "(3)", font_size=24)
		sub_eq_3.set_color_by_tex("1", TEAL)
		sub_eq_3.set_color_by_tex("4", TEAL)
		sub_eq_3.set_color_by_tex("(3)", TEAL)
		sub_eq_3.next_to(sub_eq_2, DOWN, buff=0.5)
		self.play(Write(sub_eq_3))

		sub_eq_4 = MathTex("5", "=", "a", "\\cdot", "6", "^{3}", "+", "b", "\\cdot", "6", "^{2}", "+", "c", "\\cdot", "6", "+", "d", "\\quad", "(4)", font_size=24)
		sub_eq_4.set_color_by_tex("5", PURPLE)
		sub_eq_4.set_color_by_tex("6", PURPLE)
		sub_eq_4.set_color_by_tex("(4)", PURPLE)
		sub_eq_4.next_to(sub_eq_3, DOWN, buff=0.5)
		self.play(Write(sub_eq_4))


		simplify_eq = MathTex("4", "=", "a", "+", "b", "+", "c", "+", "d", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(sub_eq, simplify_eq))

		simplify_eq_2 = MathTex("0", "=", "8a", "+", "4b", "+", "2c", "+", "d", "\\quad", "(2)", font_size=24).move_to(sub_eq_2.get_center())
		self.play(TransformMatchingTex(sub_eq_2, simplify_eq_2))

		simplify_eq_3 = MathTex("1", "=", "64a", "+", "16b", "+", "4c", "+", "d", "\\quad", "(3)", font_size=24).move_to(sub_eq_3.get_center())
		self.play(TransformMatchingTex(sub_eq_3, simplify_eq_3))

		simplify_eq_4 = MathTex("5", "=", "216a", "+", "36b", "+", "6c", "+", "d", "\\quad", "(4)", font_size=24).move_to(sub_eq_4.get_center())
		self.play(TransformMatchingTex(sub_eq_4, simplify_eq_4))


		simplify_eq_21 = MathTex("-32", "=", "-4b", "-", "6c", "-", "7d", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_2, simplify_eq_21))

		simplify_eq_31 = MathTex("-255", "=", "-48b", "-", "60c", "-", "63d", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_3, simplify_eq_31))

		simplify_eq_41 = MathTex("-859", "=", "-180b", "-", "210c", "-", "215d", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_4, simplify_eq_41))


		simplify_eq_32 = MathTex("129", "=", "12c", "+", "21d", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_31, simplify_eq_32))

		simplify_eq_42 = MathTex("581", "=", "60c", "+", "100d", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_41, simplify_eq_42))

		simplify_eq_43 = MathTex("-64", "=", "-5d", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_42, simplify_eq_43))

		simplify_eq_44 = MathTex("d", "=", "\\frac{64}{5}", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_43, simplify_eq_44))


		simplify_eq_33 = MathTex("- \\frac{699}{5}", "=", "12c", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_32, simplify_eq_33))

		simplify_eq_34 = MathTex("c", "=", "- \\frac{233}{20}", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_33, simplify_eq_34))


		simplify_eq_22 = MathTex("\\frac{288}{5}", "=", "-4b", "-", "6c", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_21, simplify_eq_22))

		simplify_eq_23 = MathTex("- \\frac{123}{10}", "=", "-4b", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_22, simplify_eq_23))

		simplify_eq_24 = MathTex("b", "=", "\\frac{123}{40}", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_23, simplify_eq_24))


		simplify_eq_11 = MathTex("- \\frac{44}{5}", "=", "a", "+", "b", "+", "c", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq, simplify_eq_11))

		simplify_eq_12 = MathTex("\\frac{57}{20}", "=", "a", "+", "b", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_11, simplify_eq_12))

		simplify_eq_13 = MathTex("- \\frac{9}{40}", "=", "a", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_12, simplify_eq_13))

		simplify_eq_14 = MathTex("a", "=", "- \\frac{9}{40}", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_13, simplify_eq_14))


		# Take modulos
		simplify_eq_15 = MathTex("a", "\\equiv", "-9", "\\cdot", "3", "\\pmod{7}", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_14, simplify_eq_15))

		simplify_eq_16 = MathTex("a", "\\equiv", "-27", "\\pmod{7}", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_15, simplify_eq_16))

		simplify_eq_17 = MathTex("a", "\\equiv", "1", "\\pmod{7}", "\\quad", "(1)", font_size=24).move_to(sub_eq.get_center())
		self.play(TransformMatchingTex(simplify_eq_16, simplify_eq_17))


		simplify_eq_25 = MathTex("b", "\\equiv", "123", "\\cdot", "3", "\\pmod{7}", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_24, simplify_eq_25))

		simplify_eq_26 = MathTex("b", "\\equiv", "369", "\\pmod{7}", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_25, simplify_eq_26))

		simplify_eq_27 = MathTex("b", "\\equiv", "5", "\\pmod{7}", "\\quad", "(2)", font_size=24).move_to(simplify_eq_2.get_center())
		self.play(TransformMatchingTex(simplify_eq_26, simplify_eq_27))


		simplify_eq_35 = MathTex("c", "\\equiv", "-233", "\\cdot", "6", "\\pmod{7}", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_34, simplify_eq_35))

		simplify_eq_36 = MathTex("c", "\\equiv", "-1398", "\\pmod{7}", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_35, simplify_eq_36))

		simplify_eq_37 = MathTex("c", "\\equiv", "2", "\\pmod{7}", "\\quad", "(3)", font_size=24).move_to(simplify_eq_3.get_center())
		self.play(TransformMatchingTex(simplify_eq_36, simplify_eq_37))


		simplify_eq_45 = MathTex("d", "\\equiv", "64", "\\cdot", "3", "\\pmod{7}", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_44, simplify_eq_45))

		simplify_eq_46 = MathTex("d", "\\equiv", "192", "\\pmod{7}", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_45, simplify_eq_46))

		simplify_eq_47 = MathTex("d", "\\equiv", "3", "\\pmod{7}", "\\quad", "(4)", font_size=24).move_to(simplify_eq_4.get_center())
		self.play(TransformMatchingTex(simplify_eq_46, simplify_eq_47))


		self.play(*[FadeOut(mob)for mob in self.mobjects])