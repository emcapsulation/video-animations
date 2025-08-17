from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#000000"


class StraightLineOnePoint(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw a plane and a single point
		plane = Plane(([-1, 10, 1], [-4, 8, 1]))
		plane.get_axes_and_labels().move_to(DOWN*0.75)

		point_and_label = plane.add_point((1, 2), RED, plane.get_axes().coords_to_point(1, 2) + RIGHT*0.5, WHITE)

		self.play(Create(plane.get_axes()), Write(plane.get_axis_labels()))
		self.wait(2)
		self.play(Create(point_and_label[0]), Write(point_and_label[1]))		
		self.wait(2)

		question = Text("How many straight lines can we draw through (1, 2)?", font_size=24, t2c={"(1, 2)": RED}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point_and_label[0], color=RED))
		self.wait(2)


		# Draw a few lines through it
		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: a*x + 2 - a, (-15, 15))
		
		y_x_1, y_x_1_label = polynomial_set.draw_polynomial(1, [-1, 7], "y = x + 1", polynomial_set.axes.coords_to_point(3, 4) + RIGHT*1.5)
		self.play(Create(y_x_1), Write(y_x_1_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		y_3x_m1, y_3x_m1_label = polynomial_set.draw_polynomial(3, [-1, 3], "y = 3x - 1", polynomial_set.axes.coords_to_point(2, 5) + RIGHT*1.25)
		self.play(Create(y_3x_m1), Write(y_3x_m1_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		y_m2x_4, y_m2x_4_label = polynomial_set.draw_polynomial(-2, [-1, 4], "y = -2x + 4", polynomial_set.axes.coords_to_point(3, -2) + RIGHT*1.5)
		self.play(Create(y_m2x_4), Write(y_m2x_4_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		self.play(FadeOut(polynomial_set.get_polynomials()))
		self.wait(2)


		# Draw a smooth set of lines through it
		question_2 = MathTex("\\infty").move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)


		def calculate_x_range(a):
			x_min, x_max = plane.get_axes().x_range[0], plane.get_axes().x_range[1]

			x1 = x_min
			if a != 0:
				x1 = (-4+a-2)/a

			x2 = x_max
			if a != 0:
				x2 = (8+a-2)/a

			return [max(x_min, min(x1, x2)), min(x_max, max(x1, x2))]


		line = always_redraw(lambda: polynomial_set.get_line(calculate_x_range))
		self.add(line)
		self.bring_to_front(plane.get_points())


		def equation_text(a):
			return f"y = {a:.2f}x + {(2 - a):.2f}"

		equation = always_redraw(lambda: polynomial_set.get_equation(equation_text, UP*2 + RIGHT*4))
		self.add(equation)

		polynomial_set.animate_a_tracker(self, 6)	
		self.wait(2)



class StraightLineTwoPoints(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw a plane and two points
		plane = Plane(([-1, 10, 1], [-4, 8, 1]))
		plane.get_axes_and_labels().move_to(DOWN*0.75)

		point_and_label = plane.add_point((1, 2), RED, plane.get_axes().coords_to_point(1, 2) + RIGHT*0.5, WHITE)

		self.add(plane.get_axes_and_labels(), point_and_label)
		self.wait(2)

		point_and_label_2 = plane.add_point((2, 6), ORANGE, plane.get_axes().coords_to_point(2, 6) + RIGHT*0.5, WHITE)
		self.play(Create(point_and_label_2[0]), Write(point_and_label_2[1]))		
		self.wait(2)

		question = Text("How many straight lines can we draw through (1, 2) and (2, 6)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point_and_label[0], color=RED))
		self.play(Flash(point_and_label_2[0], color=ORANGE))
		self.wait(2)


		# Draw the line through it
		question_2 = Text("Only 1", font_size=24).move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)

		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: a*x + 2 - a, (-15, 15))
		
		y_4x_m2, y_4x_m2_label = polynomial_set.draw_polynomial(4, [-1, 2.5], "y = 4x - 2", polynomial_set.axes.coords_to_point(1.5, 4) + RIGHT*1.5)
		self.play(Create(y_4x_m2), Write(y_4x_m2_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)



class ParabolaTwoPoints(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw a plane and two points
		plane = Plane(([-1, 10, 1], [-4, 8, 1]))
		plane.get_axes_and_labels().move_to(DOWN*0.75)

		point_and_label = plane.add_point((1, 2), RED, plane.get_axes().coords_to_point(1, 2) + RIGHT*0.5, WHITE)
		point_and_label_2 = plane.add_point((2, 6), ORANGE, plane.get_axes().coords_to_point(2, 6) + RIGHT*0.5, WHITE)
		
		self.add(plane.get_axes_and_labels(), point_and_label, point_and_label_2)
		self.wait(2)


		question = Text("How many parabolas can we draw through (1, 2) and (2, 6)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point_and_label[0], color=RED))
		self.play(Flash(point_and_label_2[0], color=ORANGE))
		self.wait(2)


		# Draw a few parabolas through them
		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a-2)/2 + 2)*x*x - ((3*a-2)/2)*x + a, (-50, 60))
		
		curve_1, curve_1_label = polynomial_set.draw_polynomial(1, [-1, 2.3], "y = 1.5x^{2} - 0.5x + 1", polynomial_set.axes.coords_to_point(2.5, 7) + RIGHT*1.5)
		self.play(Create(curve_1), Write(curve_1_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		curve_2, curve_2_label = polynomial_set.draw_polynomial(10, [0.16, 2.18], "y = 6x^{2} - 14x + 10", polynomial_set.axes.coords_to_point(2, 5) + RIGHT*1.5)
		self.play(Create(curve_2), Write(curve_2_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		curve_3, curve_3_label = polynomial_set.draw_polynomial(-6, [0.2, 4.79], "y = -2x^{2} + 10x - 6", polynomial_set.axes.coords_to_point(4, 2) + RIGHT*1.5)
		self.play(Create(curve_3), Write(curve_3_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)

		self.play(FadeOut(polynomial_set.get_polynomials()))
		self.wait(2)


		# Draw a smooth set of parabolas through the points
		question_2 = MathTex("\\infty").move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)

		line = always_redraw(lambda: polynomial_set.get_line(None))
		self.add(line)
		self.bring_to_front(plane.get_points())


		def equation_text(a):
			return f"y = {((a-2)/2 + 2):.2f}x^{2} + {(-1*(3*a-2)/2):.2f}x + {a:.2f}"

		equation = always_redraw(lambda: polynomial_set.get_equation(equation_text, UP*2 + RIGHT*4))
		self.add(equation)

		polynomial_set.animate_a_tracker(self, 6)	
		self.wait(2)



class ParabolaThreePoints(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw a plane and two points
		plane = Plane(([-1, 10, 1], [-4, 8, 1]))
		plane.get_axes_and_labels().move_to(DOWN*0.75)

		point_and_label = plane.add_point((1, 2), RED, plane.get_axes().coords_to_point(1, 2) + RIGHT*0.5, WHITE)
		point_and_label_2 = plane.add_point((2, 6), ORANGE, plane.get_axes().coords_to_point(2, 6) + RIGHT*0.5, WHITE)
		
		self.add(plane.get_axes_and_labels(), point_and_label, point_and_label_2)
		self.wait(2)


		# Draw in the third point
		point_and_label_3 = plane.add_point((3, 4), GOLD, plane.get_axes().coords_to_point(3, 4) + RIGHT*0.5, WHITE)
		self.play(Create(point_and_label_3[0]), Write(point_and_label_3[1]))		
		self.wait(2)

		question = Text("How many parabolas can we draw through (1, 2), (2, 6) and (3, 4)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE, "(3, 4)": GOLD}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point_and_label[0], color=RED))
		self.play(Flash(point_and_label_2[0], color=ORANGE))
		self.play(Flash(point_and_label_3[0], color=GOLD))
		self.wait(2)


		# Draw the parabola through it
		question_2 = Text("Only 1", font_size=24).move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)

		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a-2)/2 + 2)*x*x - ((3*a-2)/2)*x + a, (-50, 60))
		
		curve, curve_label = polynomial_set.draw_polynomial(-8, [-1, 10], "y = -3x^{2} + 13x - 8", polynomial_set.axes.coords_to_point(3.5, 2) + RIGHT*1.5)
		self.play(Create(curve), Write(curve_label))
		self.bring_to_front(plane.get_points())	
		self.wait(2)


		# Introduce the fact that a degree d polynomial is uniquely defined by d+1 points
		deg2 = Text("A degree-2 polynomial is uniquely determined by 3 points.", 
			font_size=20, color=BLACK, t2c={"1": MAROON, "2": MAROON, "3": MAROON})
		rect = BackgroundRectangle(deg2, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		self.play(FadeIn(rect), Write(deg2))
		self.wait(2)

		deg1 = Text("A degree-1 polynomial is uniquely determined by 2 points.", 
			font_size=20, color=BLACK, t2c={"1": MAROON, "2": MAROON, "3": MAROON})
		self.play(Transform(deg2, deg1))
		self.wait(2)

		degd = Text("A degree-d polynomial is uniquely determined by d+1 points.", font_size=20, color=BLACK)
		self.play(Transform(deg2, degd))
		self.wait(2)



class CubicDemo(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw a plane and three points
		plane = Plane(([-1, 10, 1], [-4, 8, 1]))
		plane.get_axes_and_labels().move_to(DOWN*0.75)

		point_and_label = plane.add_point((1, 2), RED, plane.get_axes().coords_to_point(1, 2) + RIGHT*0.5, WHITE)
		point_and_label_2 = plane.add_point((2, 6), ORANGE, plane.get_axes().coords_to_point(2, 6) + RIGHT*0.5, WHITE)
		point_and_label_3 = plane.add_point((3, 4), GOLD, plane.get_axes().coords_to_point(3, 4) + RIGHT*0.5, WHITE)
		
		self.add(plane.get_axes_and_labels(), point_and_label, point_and_label_2, point_and_label_3)
		self.wait(2)


		# Draw the set of cubics
		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a-13)/11)*x*x*x - (3*(2*a-15)/11)*x*x + a*x - (6*a+32)/11 + 2, (-110, 170))
		
		line = always_redraw(lambda: polynomial_set.get_line(None))
		self.add(line)
		self.bring_to_front(plane.get_points())


		def equation_text(a):
			return f"y = {((a-13)/11):.2f}x^{3} + {-1*(3*(2*a-15)/11):.2f}x^{2} + {a:.2f}x + {-1*(6*a+32)/11 + 2:.2f}"

		equation = always_redraw(lambda: polynomial_set.get_equation(equation_text, UP*2 + RIGHT*4))
		self.add(equation)

		polynomial_set.animate_a_tracker(self, 6)	
		self.wait(2)


		# Add a fourth point which locks it in
		point_and_label_4 = plane.add_point((4, 2), GREEN, plane.get_axes().coords_to_point(4, 2) + RIGHT*0.5, WHITE)
		self.play(Create(point_and_label_4[0]), Write(point_and_label_4[1]))	
		self.play(Flash(point_and_label_4[0], color=GREEN))	
		self.wait(2)

		self.play(polynomial_set.a_tracker.animate.set_value(24), run_time=1, rate_func=linear)
		self.bring_to_front(plane.get_points())	
		self.wait(2)



class LagrangeFormula(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		lagrange = MathTex("P(x) = \\sum_{i=1}^{k} y_{i} \\prod_{1 \\leq j \\leq k, j \\neq i} \\frac{x - x_{j}}{x_{i} - x_{j}}")
		self.play(Write(lagrange))

		self.wait(5)



class Thumbnail(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Shamir's Secret Sharing").move_to(UP*3)
		title.set_color(WHITE)
		self.add(title)


		# Family at the bottom
		y_pos = DOWN*3.5
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.25, 1, positions)
		family.set_label_colour(BLACK)
		family_group = family.get_family_group()

		self.add(family_group)


		# Draw in axes and polynomial
		plane = Plane(([-1, 7, 1], [-20, 130, 10]), xy_length=(12, 4.5), include_numbers=False)
		plane.set_colour(WHITE)
		plane.get_axes()
		self.add(plane.get_axes())

		polynomial = Polynomial(plane.get_axes(), lambda x: x*x*x - 2*x*x - 20*x + 64)
		
		curve, curve_label = polynomial.draw_polynomial([-1, 7], "P(x) \\equiv a_{k-1}x^{k-1} + a_{k-2}x^{k-2} + ... + a_{1}x + a_0 \\pmod{p}", UP*2, WHITE, label_font_size=30)
		self.add(curve_label)
		self.add(curve)


		# Be a bit mysterious
		y_int_maths_2 = Text("Secret = ?", font_size=24, color=RED).next_to(curve_label, DOWN)
		self.add(y_int_maths_2)


		# Give the points to each person
		fam_points = [(1, 43), (2, 24), (3, 13), (4, 16), (5, 39), (6, 88)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		point_group, label_group = VGroup(), VGroup()

		i = 0
		for point in fam_points:
			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN

			point_and_label = plane.add_point(point, colours[i], family_group[i].get_center() + UP*0.75, colours[i], label_text=f"(x_{i}, y_{i})")

			point_group.add(point_and_label[0])
			label_group.add(point_and_label[1])			

			i += 1


		# Randomly sample 4 points and draw the polynomial through it
		fam_indexes = [0, 1, 2, 3, 4, 5]
		index_sample = random.sample([0, 1, 2, 4, 5], 4)

		point_subset, label_subset = VGroup(), VGroup()
		for i in range(0, len(fam_indexes)):
			if i in index_sample:
				pos = RIGHT+UP
				if i >= 4:
					pos = RIGHT+DOWN

				label_group[i].next_to(point_group[i], pos, buff=0.2)
				self.add(point_group[i])

				point_subset.add(point_group[i])
				label_subset.add(label_group[i])

		self.add(label_group)
		self.add(polynomial.get_polynomial())
		self.bring_to_front(point_subset)
		self.add(polynomial.get_label())

