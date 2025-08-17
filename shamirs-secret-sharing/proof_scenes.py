from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#010621"


class EquallyLikelyKeys(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		lemma = Text("A degree-(k-1) polynomial requires k points to uniquely define it.", font_size=18).move_to(UP*3)
		self.play(Write(lemma))
		self.wait(2)


		lemma_2 = Text("There is exactly one polynomial of degree ≤k-1 which interpolates a set of k distinct points.", font_size=18).move_to(UP*3)
		self.play(Transform(lemma, lemma_2))
		self.wait(2)


		# Draw a plane
		plane = Plane(([0, 6, 1], [0, 6, 1]), include_numbers=False)
		self.play(Create(plane.get_axes().shift(DOWN*0.5)))
		self.wait(2)


		# Add the k-1 shares
		points = [(1, 3), (3, 4), (4, 2), (6, 5)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]

		i = 0
		point_dots = VGroup()
		for point in points:
			point_dot = plane.add_point(point, colours[i], ORIGIN, WHITE, label_text="")
			point_dots.add(point_dot)
			self.play(Create(point_dot))
			i += 1

		self.wait(2)

		attacker_text = Text("Attacker has stolen these k-1 shares.", color=PINK, font_size=18)
		self.play(Write(attacker_text))
		self.wait(2)

		attacker_text_2 = Text("Guessing a secret key takes\nthem up to k points total.", color=PINK, font_size=18).move_to(LEFT*3.5 + DOWN*3)


		# Attacker guesses the secret key
		for i in range(0, 7):
			secret_key = (0, i)
			sk_dot = plane.add_point(secret_key, RED, ORIGIN, WHITE, label_text="")
			self.play(Create(sk_dot))
			if i == 0:
				self.play(Write(attacker_text_2))
		
			polynomial_curve = plane.draw_polynomial_as_dots([0, 6], [0, 6], lambda x: (Polynomial.lagrange_interpolation(x, points + [secret_key])%7), WHITE)
			self.play(Create(polynomial_curve))
			self.wait(2)

			self.play(FadeOut(sk_dot), FadeOut(polynomial_curve))
		self.wait(2)


		# Attacker guesses next share and secret key
		self.play(FadeOut(point_dots[2]))
		points.pop(2)
		self.wait(2)


		for i in range(0, 7):
			next_share = (4, i)
			ns_dot = plane.add_point(next_share, TEAL, ORIGIN, WHITE, label_text="")
			self.play(Create(ns_dot))

			for j in range(0, 7):
				secret_key = (0, j)
				sk_dot = plane.add_point(secret_key, RED, ORIGIN, WHITE, label_text="")
				self.play(Create(sk_dot), run_time=0.01)
		
				polynomial_curve = plane.draw_polynomial_as_dots([0, 6], [0, 6], lambda x: (Polynomial.lagrange_interpolation(x, points + [secret_key] + [next_share])%7), WHITE, step=0.01)
				self.play(Create(polynomial_curve), run_time=0.01)
				self.wait(2)

				self.play(FadeOut(sk_dot), FadeOut(polynomial_curve), run_time=0.01)
			self.play(FadeOut(ns_dot))

		self.wait(2)



class UniquenessProof(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		lemma = Text("There is exactly one polynomial of degree ≤k-1 which interpolates a set of k distinct points.", font_size=18).move_to(UP*3)
		self.add(lemma)


		# Draw a plane
		plane = Plane(([0, 6, 1], [0, 7, 1]), include_numbers=False)
		self.add(plane.get_axes().scale(0.7).shift(DOWN*1.5))
		

		# Add the k-1 shares
		points = [(1, random.randint(0, 6)), (2, random.randint(0, 6)), (3, random.randint(0, 6)), (4, random.randint(0, 6)), (5, random.randint(0, 6)), (6, random.randint(0, 6))]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]

		i = 0
		point_dots = VGroup()
		for point in points:
			point_dot = plane.add_point(point, colours[i], ORIGIN, WHITE, label_text="")
			point_dots.add(point_dot)
			self.add(point_dot)
			i += 1


		k_points = Text("k points", font_size=20, color=LIGHT_PINK).move_to(DOWN*1 + RIGHT*6)
		self.wait(2)
		self.play(Write(k_points))
		self.wait(2)


		# Show Lagrange Formula
		lagrange = MathTex("P(x) = \\sum_{i=1}^{k} y_{i} \\prod_{1 \\leq j \\leq k, j \\neq i} \\frac{x - x_{j}}{x_{i} - x_{j}}", color=BLACK)
		rect = BackgroundRectangle(lagrange, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		self.play(FadeIn(rect), Write(lagrange))
		self.wait(2)
		self.play(FadeOut(rect), FadeOut(lagrange))


		# Illustrate px, qx and rx=px-qx
		px = plane.draw_polynomial_as_dots([0.8, 6], [0, 7], lambda x: (Polynomial.lagrange_interpolation(x, points)%7), WHITE)
		px_label = MathTex("p(x) \\equiv a_{k-1} x^{k-1} + a_{k-2} x^{k-2} + ... + a_1 x + a_0 \\pmod{p}", font_size=24).move_to(UP*2.5 + LEFT*4)
		self.play(Create(px), Write(px_label))
		self.bring_to_front(point_dots)
		self.wait(2)


		qx = plane.draw_polynomial_as_dots([0.8, 6], [0, 7], lambda x: (Polynomial.lagrange_interpolation(x, points + [(0, 4)])%7), GRAY)
		qx_label = MathTex("q(x) \\equiv b_{k-1} x^{k-1} + b_{k-2} x^{k-2} + ... + b_1 x + b_0 \\pmod{p}", color=GRAY, font_size=24).move_to(UP*2.5 + RIGHT*4)
		self.play(Write(qx_label))
		self.wait(1)
		self.play(Create(qx))
		self.bring_to_front(point_dots)
		self.wait(2)


		def subtract_polynomials(px, qx):
			if (px-qx)%7 < 0:
				return 7-((px-qx)%7)

			return (px-qx)%7


		rx = plane.draw_polynomial_as_dots([0.8, 6], [0, 7], lambda x: subtract_polynomials(Polynomial.lagrange_interpolation(x, points), Polynomial.lagrange_interpolation(x, points + [(0, 4)])), MAROON)
		rx_label = MathTex("r(x) = p(x) - q(x)", color=MAROON, font_size=24).move_to(UP*2)
		self.play(Write(rx_label))
		self.wait(1)
		self.play(Create(rx))
		self.bring_to_front(point_dots)
		self.wait(2)

		# Write r(x) fully
		rx_label_2 = MathTex("r(x) = p(x) - q(x) \\equiv (a_{k-1} - b_{k-1}) x^{k-1} + (a_{k-2} - b_{k-2}) x^{k-2} + ... + (a_1 - b_1) x + (a_0 - b_0) \\pmod{p}", color=MAROON, font_size=24).move_to(UP*2)
		self.play(Transform(rx_label, rx_label_2))
		self.wait(2)

		# Create the roots
		i = 1
		for point in point_dots:
			zero = point.copy()
			zero.set_color(RED)
			self.play(zero.animate.move_to(plane.axes.coords_to_point(i, 0)))

			i += 1
		k_plus_one = Text("k roots", font_size=20, color=MAROON).move_to(DOWN*2 + RIGHT*6)
		self.play(Write(k_plus_one))
		self.wait(2)

		# Transform r(x) into the zero polynomial
		zp = Polynomial(plane.get_axes(), lambda x: 0)
		zero = zp.draw_polynomial([0.8, 6], "", ORIGIN, MAROON)
		self.play(Transform(rx, zero))

		rx_label_3 = MathTex("r(x) = p(x) - q(x) = 0", color=MAROON, font_size=24).move_to(UP*2)
		self.play(Transform(rx_label, rx_label_3))
		self.wait(2)


		px_equal_qx = MathTex("p(x) - q(x) = 0", font_size=24).next_to(rx_label_3, DOWN)
		self.play(Write(px_equal_qx))
		self.wait(1)

		px_equal_qx_2 = MathTex("p(x) = q(x)", font_size=24).next_to(rx_label_3, DOWN)
		self.play(Transform(px_equal_qx, px_equal_qx_2))
		self.wait(2)

