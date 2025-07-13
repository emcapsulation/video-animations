from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#120903"


class UseIntegers(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Write polynomial and integer coefficients and shares
		polynomial_text = MathTex("P(x) = a_{k-1} x^{k-1} + a_{k-2} x^{k-2} + ... + a_{1} x^{1} + a_{0}")
		self.play(Write(polynomial_text))

		n_points = MathTex("\\forall (x_{i}, y_{i}) \\in \\{(x_{1}, y_{1}), (x_{2}, y_{2}), ..., (x_{n}, y_{n})\\}, P(x_{i}) = y_{i}").move_to(DOWN*2)
		self.play(Write(n_points))
		self.wait(2)


		integer_coefficients = MathTex("{a_{k-1}, a_{k-2}, ..., a_{1}, a_{0}} \\in \\mathbb{Z}", font_size=30, color=GREEN).next_to(polynomial_text, DOWN)
		integer_shares = MathTex("{x_{1}, x_{2}, ..., x_{n}} \\in \\mathbb{Z}", font_size=30, color=GREEN).next_to(n_points, DOWN)

		self.play(Write(integer_coefficients))
		self.wait(1)
		self.play(Write(integer_shares))
		self.wait(1)


		green_check = Text("☑", color=GREEN, font_size=108).move_to(UP*2)
		self.play(SpinInFromNothing(green_check))
		self.wait(2)

		self.play(FadeOut(green_check))


		# Draw in grandpa and speech bubble
		grandpa = Human(ORANGE, 0.8).add_label("Grandpa", WHITE).get_human().scale(0.4).move_to(RIGHT*5+UP*2.5)
		self.play(Create(grandpa))

		speech_bubble = SpeechBubble([ORANGE, GOLD], 9, 1.5).get_speech_bubble().move_to(LEFT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Each possible value of the key should be equally likely.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)

		speech2 = Text("Could some information about the secret key be leaked?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)

		self.play(
			FadeOut(polynomial_text), 
			FadeOut(n_points), 
			FadeOut(integer_coefficients), 
			FadeOut(integer_shares)
		)


		# Draw in axes, polynomial and y intercept
		plane = Plane(([-1, 7, 1], [-50, 170, 20]), xy_length=[12, 6])
		plane.get_axes_and_labels().scale(0.75).shift(DOWN)
		self.play(Create(plane.get_axes()), Write(plane.get_axis_labels()))
		self.wait(2)

		polynomial = Polynomial(plane.get_axes(), lambda x: x*x*x - 2*x*x - 20*x + 64)
		
		curve, curve_label = polynomial.draw_polynomial(
			[-1, 7], 
			"P(x) = x^{3} - 2x^{2} - 20x + 64", 
			UP + RIGHT, WHITE, label_font_size=24
		)
		self.play(Write(curve_label))
		self.play(Create(curve))
		self.wait(2)

		yint_and_label = plane.add_point((0, 64), RED, plane.get_axes().coords_to_point(0, 64) + LEFT, RED)
		self.play(Create(yint_and_label[0]), Write(yint_and_label[1]))
		self.wait(2)

		self.play(
			FadeOut(polynomial.get_polynomial_and_label()), 
			FadeOut(yint_and_label)
		)

		plane.points = VGroup()


		# Three points
		fam_points = [(1, 43), (2, 24), (3, 13)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]

		i = 0
		for point in fam_points:
			point_and_label = plane.add_point(point, colours[i], plane.get_axes().coords_to_point(*point) + (RIGHT+UP)*0.5, colours[i])
			self.play(Create(point_and_label[0]), Write(point_and_label[1]))

			i += 1
		self.wait(2)


		# Show the infinite set of polynomials
		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a+31)/11)*x*x*x - (2*(3*a+71)/11)*x*x + a*x + (-6*a+111)/11 + 43, (-170, 140))
		
		line = always_redraw(lambda: polynomial_set.get_line([-0.5, 7]))
		self.add(line)
		self.bring_to_front(plane.get_points())


		# Label the secret key (y-intercept)
		yint_and_label = always_redraw(lambda: polynomial_set.get_y_int(plane))
		self.add(yint_and_label)


		def equation_text(a):
			return f"P(x) = {((a+31)/11):.2f}x^{3} + {-1*(2*(3*a+71)/11):.2f}x^{2} + {a:.2f}x + {(-6*a+111)/11 + 43:.2f}"

		equation = always_redraw(lambda: polynomial_set.get_equation(equation_text, UP+RIGHT))
		self.add(equation)

		polynomial_set.animate_a_tracker(self, 6)	
		self.wait(2)

		self.remove(line, equation)
		plane.points = VGroup(plane.points[0], plane.points[1], plane.points[2])
		self.remove(yint_and_label)


		# Show the reduced set of polynomials
		polynomial_set_2 = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a+31)/11)*x*x*x - (2*(3*a+71)/11)*x*x + a*x + (-6*a+111)/11 + 43, (-50, 50))
		
		def get_line_colour_integer():
			a = polynomial_set_2.a_tracker.get_value()

			colour = GRAY
			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and ((-6*a+111)/11 + 43).is_integer():
				colour = polynomial_set_2.get_line_colour(a)

			return colour

		line = always_redraw(lambda: polynomial_set_2.get_line([-0.5, 7], colour=get_line_colour_integer()))
		self.add(line)
		self.bring_to_front(plane.get_points())


		# Label the secret key (y-intercept)
		yint_and_label = always_redraw(lambda: polynomial_set_2.get_y_int(plane, colour=get_line_colour_integer()))
		self.add(yint_and_label)


		def equation_text(a):
			return f"P(x) = {((a+31)/11):.2f}x^{3} + {-1*(2*(3*a+71)/11):.2f}x^{2} + {a:.2f}x + {(-6*a+111)/11 + 43:.2f}"

		equation = always_redraw(lambda: polynomial_set_2.get_equation(equation_text, UP+RIGHT, colour=get_line_colour_integer()))
		self.add(equation)

		
		# Pause when integer coefficients are hit
		polynomial_set_2.a_tracker.set_value(polynomial_set_2.a_start)

		step, pause_time, frame_time = 1, 0.5, 0.02
		a = polynomial_set_2.a_start
		while a <= polynomial_set_2.a_end:
			self.play(polynomial_set_2.a_tracker.animate.set_value(a), run_time=frame_time, rate_func=linear)

			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and ((-6*a+111)/11 + 43).is_integer():
				self.wait(pause_time)

			a += step

		self.wait(2)