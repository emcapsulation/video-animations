from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#15131c"


class StraightLineOnePointAlgebra(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax + b").move_to(UP*2)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the line to pass through (1, 2)", font_size=28, t2c={"(1, 2)": RED}).next_to(general, DOWN)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "+", "b")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN)
		self.play(Write(sub_eq))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "=", "2").next_to(sub_eq, DOWN)
		self.play(TransformMatchingTex(sub_eq.copy(), simplified))
		self.wait(2)

		underline = Underline(simplified, color=MAROON)
		explain = Text("1 equation, 2 unknowns", font_size=20, color=MAROON).next_to(simplified, RIGHT*1.5)
		self.play(Create(underline), FadeIn(explain))
		self.wait(2)

		conclusion = Text("Infinitely many (a, b) pairs satisfy this.", font_size=28).next_to(simplified, DOWN, buff=0.5).shift(DOWN)
		self.play(Write(conclusion))
		self.wait(2)

		not_unique = Text("One point alone is not enough to define a line.", font_size=30, weight=BOLD).next_to(conclusion, DOWN, buff=0.5)
		self.play(FadeIn(not_unique))

		conc = VGroup(conclusion, not_unique)
		self.play(Circumscribe(conc, color=MAROON))
		self.wait(2)



class StraightLineTwoPointsAlgebra(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax + b").move_to(UP*3.5)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the line to pass through (1, 2) and (2, 6)", font_size=24, 
			t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).next_to(general, DOWN)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "+", "b", "\\quad", "(1)")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN).shift(LEFT*3)
		self.play(Write(sub_eq))
		self.wait(2)

		sub_eq_2 = MathTex("6", "=", "a", "\\cdot", "2", "+", "b", "\\quad", "(2)")
		sub_eq_2.set_color_by_tex("2", ORANGE)
		sub_eq_2.set_color_by_tex("6", ORANGE)
		sub_eq_2.next_to(point_text, DOWN).shift(RIGHT*3)
		self.play(Write(sub_eq_2))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "=", "2", "\\quad", "(1)").next_to(sub_eq, DOWN)
		simplified_2 = MathTex("2a", "+", "b", "=", "6", "\\quad", "(2)").next_to(sub_eq_2, DOWN)
		self.play(
			TransformMatchingTex(sub_eq.copy(), simplified),
			TransformMatchingTex(sub_eq_2.copy(), simplified_2)
		)
		self.wait(2)

		solve = Text("Subtract (2) - (1)", font_size=24, 
			t2c={"(1)": RED, "(2)": ORANGE})
		self.play(Write(solve))
		self.wait(2)

		big_boi = MathTex("2a", "-", "a", "+", "b", "-", "b", "=", "6", "-", "2").next_to(solve, DOWN)
		self.play(Write(big_boi))
		self.wait(2)

		big_boi_simp = MathTex("a", "=", "4").next_to(solve, DOWN)
		self.play(Transform(big_boi, big_boi_simp))
		self.wait(2)

		solve_2 = Text("Substitute a = 4 into (1)", font_size=24, 
			t2c={"(1)": RED}).next_to(big_boi_simp, DOWN).shift(DOWN*0.5)
		self.play(Write(solve_2))
		self.wait(2)

		again = MathTex("4", "+", "b", "=", "2").next_to(solve_2, DOWN)
		self.play(Write(again))
		self.wait(2)

		again_simp = MathTex("b", "=", "-2").next_to(solve_2, DOWN)
		self.play(Transform(again, again_simp))
		self.wait(2)

		final_guy = MathTex("y = 4x - 2").next_to(again_simp, DOWN).shift(DOWN*0.5)
		self.play(Write(final_guy))
		self.play(Circumscribe(final_guy, color=MAROON))
		self.wait(2)

		conclusion = Text("A degree-1 polynomial requires 2 points to uniquely define it.", font_size=20, color=BLACK)
		rect = BackgroundRectangle(conclusion, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		self.play(FadeIn(rect), Write(conclusion))
		self.wait(2)



class ParabolaTwoPointsAlgebra(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax^{2} + bx + c").move_to(UP*3)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the curve to pass through (1, 2) and (2, 6)", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).next_to(general, DOWN, buff=1)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "^{2}", "+", "b", "\\cdot", "1", "+", "c", "\\quad", "(1)")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN).shift(LEFT*3)
		self.play(Write(sub_eq))
		self.wait(2)

		sub_eq_2 = MathTex("6", "=", "a", "\\cdot", "2", "^{2}", "+", "b", "\\cdot", "2", "+", "c", "\\quad", "(2)")
		sub_eq_2.set_color_by_tex("2", ORANGE)
		sub_eq_2.set_color_by_tex("6", ORANGE)
		sub_eq_2.next_to(point_text, DOWN).shift(RIGHT*3)
		self.play(Write(sub_eq_2))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "+", "c", "=", "2", "\\quad", "(1)").next_to(sub_eq, DOWN)
		simplified_2 = MathTex("4a", "+", "2b", "+", "c", "=", "6", "\\quad", "(2)").next_to(sub_eq_2, DOWN)
		self.play(
			TransformMatchingTex(sub_eq.copy(), simplified),
			TransformMatchingTex(sub_eq_2.copy(), simplified_2)
		)
		self.wait(2)

		underline = Underline(simplified, color=MAROON)
		underline_2 = Underline(simplified_2, color=MAROON)

		explain = Text("2 equations, 3 unknowns", font_size=20, color=MAROON).move_to(DOWN*0.5)
		self.play(Create(underline), Create(underline_2), FadeIn(explain))
		self.wait(2)

		conclusion = Text("Infinitely many solutions.", font_size=28).next_to(explain, DOWN, buff=0.5).shift(DOWN)
		self.play(Write(conclusion))
		self.wait(2)



class UseIntegersAlgebra(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax^{3} + bx^{2} + cx + d").move_to(UP*3)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the curve to pass through (1, 43), (2, 24) and (3, 13)", 
			font_size=24, t2c={"(1, 43)": ORANGE, "(2, 24)": GOLD, "(3, 13)": GREEN}).next_to(general, DOWN, buff=1)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("43", "=", "a", "\\cdot", "1", "^{3}", "+", "b", "\\cdot", "1", "^{2}", "+", "c", "\\cdot", "1", "+", "d", "\\quad", "(1)", font_size=36)
		sub_eq.set_color_by_tex("43", ORANGE)
		sub_eq.set_color_by_tex("1", ORANGE)
		sub_eq.next_to(point_text, DOWN)
		self.play(Write(sub_eq))

		sub_eq_2 = MathTex("24", "=", "a", "\\cdot", "2", "^{3}", "+", "b", "\\cdot", "2", "^{2}", "+", "c", "\\cdot", "2", "+", "d", "\\quad", "(2)", font_size=36)
		sub_eq_2.set_color_by_tex("24", GOLD)
		sub_eq_2.set_color_by_tex("2", GOLD)
		sub_eq_2.next_to(sub_eq, DOWN)
		self.play(Write(sub_eq_2))

		sub_eq_3 = MathTex("13", "=", "a", "\\cdot", "3", "^{3}", "+", "b", "\\cdot", "3", "^{2}", "+", "c", "\\cdot", "3", "+", "d", "\\quad", "(3)", font_size=36)
		sub_eq_3.set_color_by_tex("13", GREEN)
		sub_eq_3.set_color_by_tex("3", GREEN)
		sub_eq_3.next_to(sub_eq_2, DOWN)
		self.play(Write(sub_eq_3))
		self.wait(2)

		simplified = MathTex("43", "=", "a", "+", "b", "+", "c", "+", "d", "\\quad", "(1)", font_size=36).next_to(point_text, DOWN)
		simplified_2 = MathTex("24", "=", "8", "a", "+", "4", "b", "+", "2", "c", "+", "d", "\\quad", "(2)", font_size=36).next_to(sub_eq, DOWN)
		simplified_3 = MathTex("13", "=", "27", "a", "+", "9", "b", "+", "3", "c", "+", "d", "\\quad", "(3)", font_size=36).next_to(sub_eq_2, DOWN)

		self.play(TransformMatchingTex(sub_eq, simplified))
		self.play(TransformMatchingTex(sub_eq_2, simplified_2))
		self.play(TransformMatchingTex(sub_eq_3, simplified_3))
		self.wait(2)


		solve = Text("(1) - (2) + 1/3 * (3)", font_size=24, 
			t2c={"(1)": ORANGE, "(2)": GOLD, "(3)": GREEN}).next_to(sub_eq_3, DOWN, buff=1)
		self.play(Write(solve))
		self.wait(2)

		long_eq = MathTex("a - 8a + 9a + b - 4b + 3b + c - 2c + c + d - d + \\frac{1}{3} d = 43 - 24 + \\frac{13}{3}", font_size=36).next_to(solve, DOWN)
		self.play(Write(long_eq))
		self.wait(2)

		long_eq_simplified = MathTex("2a + \\frac{1}{3} d", "=", "\\frac{70}{3}", font_size=36).next_to(solve, DOWN)
		self.play(Transform(long_eq, long_eq_simplified))
		self.wait(2)

		long_eq_simplified_2 = MathTex("6a + d", "=", "70", font_size=36).next_to(solve, DOWN)
		self.play(Transform(long_eq, long_eq_simplified_2))
		self.wait(2)

		long_eq_simplified_3 = MathTex("d", "=", "70 - 6a", font_size=36).next_to(solve, DOWN)
		self.play(Transform(long_eq, long_eq_simplified_3))
		self.wait(2)


		simple_equation = MathTex("d", "=", "70", "-", "6", "\\cdot", "a").next_to(solve, DOWN)
		self.play(simple_equation.animate.shift(DOWN))
		self.wait(2)


		for a in range(-10, 10):
			simple_equation_2 = MathTex("d", "=", "70", "-", "6", "\\cdot", str(a), "=", str(70-6*a)).next_to(solve, DOWN).shift(DOWN)
			simple_equation_2[6].set_color(RED)
			self.play(Transform(simple_equation, simple_equation_2))

		self.wait(2)
