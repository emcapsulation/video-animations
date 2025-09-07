from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#ffffff"


class ShamirExplained(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Shamir's Secret Sharing", gradient=(ORANGE, GREEN, PURPLE)).move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		# Reiterate the premise of Shamir's Secret Sharing
		n_shares = SpeechBubble([GREEN, ORANGE], 3.5, 1).get_speech_bubble().move_to(UP*2 + LEFT*4)
		n_shares_text = Text("Split a secret\ninto n shares.", color=BLACK, font_size=20).move_to(n_shares.get_center())
		self.play(FadeIn(n_shares), Write(n_shares_text))

		k_shares = SpeechBubble([PURPLE, GREEN, ORANGE], 3.5, 1).get_speech_bubble().move_to(UP*2)
		k_shares_text = Text("≥ k shares can\nrecover the secret.", color=BLACK, font_size=20).move_to(k_shares.get_center())
		self.play(FadeIn(k_shares), Write(k_shares_text))

		less_k_shares = SpeechBubble([PURPLE, GREEN], 3.5, 1).get_speech_bubble().move_to(UP*2 + RIGHT*4)
		less_k_shares_text = Text("< k shares are\ncompletely useless.", color=BLACK, font_size=20).move_to(less_k_shares.get_center())
		self.play(FadeIn(less_k_shares), Write(less_k_shares_text))
		self.wait(2)

		self.play(
			FadeOut(n_shares), FadeOut(n_shares_text), 
			FadeOut(k_shares), FadeOut(k_shares_text), 
			FadeOut(less_k_shares), FadeOut(less_k_shares_text)
		)


		# The main fact
		poly_fact = Text("A degree-d polynomial is uniquely determined by d+1 distinct points.", color=BLACK, weight=BOLD, font_size=20).move_to(UP*2)
		self.play(Write(poly_fact))
		self.wait(2)

		line = Line(start=UP*1.5+LEFT*0.8, end=DOWN*4+LEFT*0.8)
		line.set_color_by_gradient(ORANGE, GREEN, PURPLE)
		self.play(Create(line))


		# Step 1: Choose a degree k-1 polynomial
		select_polynomial = Text("Choose a degree k-1 polynomial.", color=BLACK, font_size=16).move_to(LEFT*4 + UP)
		self.play(Write(select_polynomial))

		polynomial_text = MathTex("P(x) = a_{k-1} x^{k-1} + a_{k-2} x^{k-2} + ... + a_{1} x^{1} + a_{0}", color=BLACK, font_size=24).next_to(select_polynomial, DOWN)
		self.play(Write(polynomial_text))
		self.wait(2)


		plane = Plane(([-2, 6, 1], [-10, 20, 5]), xy_length=[7, 5], include_numbers=False, include_axes_labels=False)
		plane.set_colour(BLACK)
		plane.get_axes().to_corner(DOWN + RIGHT, buff=0.5)
		self.play(Create(plane.get_axes()))

		polynomial = Polynomial(plane.get_axes(), lambda x: 0.5 * x**3 - 3 * x**2 + 2 * x + 5)
		
		curve, curve_label = polynomial.draw_polynomial([-1.7, 6], "", ORIGIN, BLACK)
		self.play(Create(curve), run_time=2)
		self.wait(2)


		# Step 2: Find secret key
		secret_key = Text("Secret key (S) is the y-intercept.", color=BLACK, font_size=16).next_to(polynomial_text, DOWN, buff=0.5)
		self.play(Write(secret_key))

		secret_key_2 = MathTex("S = P(0) = a_{0}", color=BLACK, font_size=24).next_to(secret_key, DOWN)
		self.play(Write(secret_key_2))
		self.wait(2)

		colours = color_gradient([ORANGE, GREEN, PURPLE], 7)
		x0, y0 = 0, polynomial.get_y_value(0)
		sk_point_and_label = plane.add_point((x0, y0), colours[0], plane.get_axes().coords_to_point(x0, y0) + (UP + LEFT)*0.5, colours[0], label_text="Secret Key", label_font_size=16)
		self.play(Create(sk_point_and_label[0]), Write(sk_point_and_label[1]))
		self.wait(2)


		# Step 3: Select n points
		n_shares = Text("Select n distinct points.", color=BLACK, font_size=16).next_to(secret_key_2, DOWN, buff=0.5)
		self.play(Write(n_shares))

		n_points = MathTex("\\forall (x_{i}, y_{i}) \\in \\{(x_{1}, y_{1}), (x_{2}, y_{2}), ..., (x_{n}, y_{n})\\}, P(x_{i}) = y_{i}", color=BLACK, font_size=24).next_to(n_shares, DOWN)
		self.play(Write(n_points))
		self.wait(2)


		dots, labels = VGroup(), VGroup()
		for i in range(1, 7):
			x, y = i, polynomial.get_y_value(i)
			point_and_label = plane.add_point((x, y), colours[i], plane.get_axes().coords_to_point(x, y) + (LEFT + DOWN)*0.5, colours[i], label_text=f"(x_{i}, y_{i})", label_font_size=20)

			dots.add(point_and_label[0])
			labels.add(point_and_label[1])

			self.play(Create(point_and_label[0]), Write(point_and_label[1]))			
		self.wait(2)


		# Step 4: Recover the key
		recover = Text("S is recoverable if ≥k points are known.", color=BLACK, font_size=16).next_to(n_points, DOWN, buff=0.5)
		self.play(Write(recover))
		self.wait(2)

		self.play(
			FadeOut(polynomial.get_polynomial()), FadeOut(plane.get_points())
		)


		subsets = [[0, 3, 4, 5], [1, 2, 3, 4], [0, 1, 3, 5]]
		for subset in subsets:
			self.play(
				*[FadeIn(dots[i]) for i in subset], 
				*[FadeIn(labels[i]) for i in subset]
			)

			self.play(Create(polynomial.get_polynomial()))
			self.play(FadeIn(sk_point_and_label))

			self.play(
				FadeOut(polynomial.get_polynomial()), 
				*[FadeOut(dots[i]) for i in subset], *[FadeOut(labels[i]) for i in subset], 
				FadeOut(sk_point_and_label)
			)



class FamilyPolynomial(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in each member of the family and the SSS parameters
		y_pos = DOWN*3.5
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.25, 1, positions)
		family.set_label_colour(BLACK)
		family_group = family.get_family_group()

		self.play(Create(family_group))
		self.wait(2)


		n_text = Text("n = 6", color=ORANGE).move_to(UP)
		self.play(Write(n_text))
		self.wait(2)

		k_text = Text("k = 4", color=GREEN).next_to(n_text, DOWN)
		self.play(Write(k_text))
		self.wait(2)

		self.play(FadeOut(n_text), FadeOut(k_text))


		# Draw in axes and polynomial
		plane = Plane(([-1, 7, 1], [-50, 170, 10]))
		plane.set_colour(BLACK)
		plane.get_axes().move_to(UP*0.75)
		self.play(Create(plane.get_axes()), Write(plane.get_axis_labels()))

		polynomial = Polynomial(plane.get_axes(), lambda x: x*x*x - 2*x*x - 20*x + 64)
		
		curve, curve_label = polynomial.draw_polynomial([-1, 7], "P(x) = x^{3} - 2x^{2} - 20x + 64", UP*3, BLACK, label_font_size=36)
		self.play(Write(curve_label))
		self.play(Create(curve))
		self.wait(2)


		# Calculate the secret key
		y_int_maths = MathTex("P(0) = 0^{3} - 2 \\cdot 0^{2} - 20 \\cdot 0 + 64", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Write(y_int_maths))
		self.wait(2)

		y_int_maths_2 = MathTex("S = 64", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Transform(y_int_maths, y_int_maths_2))

		yint_and_label = plane.add_point((0, 64), RED, plane.get_axes().coords_to_point(0, 64) + LEFT*1.5, RED)
		self.play(Create(yint_and_label[0]), Write(yint_and_label[1]), FadeOut(y_int_maths))
		self.wait(2)


		# Give the points to each person
		fam_points = [(1, 43), (2, 24), (3, 13), (4, 16), (5, 39), (6, 88)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		point_group, label_group = VGroup(), VGroup()

		i = 0
		for point in fam_points:
			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN

			point_and_label = plane.add_point(point, colours[i], plane.get_axes().coords_to_point(*point) + pos*0.5, colours[i])

			point_group.add(point_and_label[0])
			label_group.add(point_and_label[1])
			self.play(Create(point_and_label[0]), Write(point_and_label[1]))

			i += 1
		self.wait(2)


		# Move the points to the family members
		move_point_anim = []
		for i in range(0, len(label_group)):
			move_point_anim.append(label_group[i].animate.next_to(family_group[i], UP))
		self.play(*move_point_anim)
		self.wait(2)

		self.play(
			FadeOut(point_group),
			FadeOut(yint_and_label),
			FadeOut(polynomial.get_polynomial_and_label())
		)


		# Randomly sample 4 points and draw the polynomial through it
		fam_indexes = [0, 1, 2, 3, 4, 5]
		for count in range(0, 3):
			index_sample = random.sample(fam_indexes, 4)

			point_subset, label_subset = VGroup(), VGroup()
			for i in index_sample:
				pos = RIGHT+UP
				if i >= 4:
					pos = RIGHT+DOWN

				self.play(Create(point_group[i]), label_group[i].animate.next_to(point_group[i], pos, buff=0.2))

				point_subset.add(point_group[i])
				label_subset.add(label_group[i])
			self.wait(2)

			self.play(Create(polynomial.get_polynomial()))
			self.bring_to_front(point_subset)
			self.play(Write(polynomial.get_label()))
			self.wait(2)


			self.play(Create(yint_and_label[0]))
			self.play(Write(yint_and_label[1]))
			self.wait(2)


			self.play(
				FadeOut(point_subset),
				FadeOut(yint_and_label),
				FadeOut(polynomial.get_polynomial_and_label()),
				*[label_group[i].animate.next_to(family_group[i], UP) for i in range(0, len(family_group))]
			)
			self.wait(2)


		# Put three points on the plane
		index_sample = [0, 3, 4]
		point_subset, label_subset = VGroup(), VGroup()
		for i in index_sample:
			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN

			self.play(Create(point_group[i]), label_group[i].animate.next_to(point_group[i], pos, buff=0.2))

			point_subset.add(point_group[i])
			label_subset.add(label_group[i])
		self.wait(2)


		# Smoothly draw all the cubic options through the three points
		polynomial_set = PolynomialSet(plane.get_axes(), lambda a: lambda x: ((a+49)/29)*x*x*x - (2*(5*a+129)/29)*x*x + a*x + (-20*a+209)/29 + 43, (-170, 140))
		
		line = always_redraw(lambda: polynomial_set.get_line([-0.5, 7]))
		self.add(line)
		self.bring_to_front(point_subset, label_subset)


		# Label the secret key (y-intercept)
		yint_and_label = always_redraw(lambda: polynomial_set.get_y_int(plane))
		self.add(yint_and_label)


		def equation_text(a):
			return f"P(x) = {((a+49)/29):.2f}x^{3} + {-1*(2*(5*a+129)/29):.2f}x^{2} + {a:.2f}x + {(-20*a+209)/29 + 43:.2f}"

		equation = always_redraw(lambda: polynomial_set.get_equation(equation_text, UP*3))
		self.add(equation)

		polynomial_set.animate_a_tracker(self, 6)	
		self.wait(2)



class ModuloPolynomial(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in each member of the family and the SSS parameters
		y_pos = DOWN*3.5
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.25, 1, positions)
		family.set_label_colour(BLACK)
		family_group = family.get_family_group()

		self.play(Create(family_group))
		self.wait(2)


		n_text = Text("n = 6", color=ORANGE).move_to(UP)
		self.play(Write(n_text))
		self.wait(2)

		k_text = Text("k = 4", color=GREEN).next_to(n_text, DOWN)
		self.play(Write(k_text))
		self.wait(2)

		p_text = Text("p = 7", color=PURPLE).next_to(n_text, UP)
		self.play(Write(p_text))
		self.wait(2)

		self.play(FadeOut(n_text), FadeOut(k_text), FadeOut(p_text))


		# Draw in axes and polynomial
		plane = Plane(([-1, 7, 1], [-40, 230, 10]))
		plane.set_colour(BLACK)
		plane.get_axes().move_to(UP*0.75)
		self.play(Create(plane.get_axes()), Write(plane.get_axis_labels()))

		polynomial = Polynomial(plane.get_axes(), lambda x: 8*x*x*x - 65*x*x + 135*x + 10)
		
		curve, curve_label = polynomial.draw_polynomial([-1, 7], "P(x) = 8x^{3} - 65x^{2} + 135x + 10", UP*3, BLACK, label_font_size=36)
		self.play(Write(curve_label))
		self.play(Create(curve))
		self.wait(2)


		# Calculate the secret key
		y_int_maths = MathTex("P(0) = 8 \\cdot 0^{3} - 65 \\cdot 0^{2} + 135 \\cdot 0 + 10", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Write(y_int_maths))
		self.wait(2)

		y_int_maths_2 = MathTex("S = 10", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Transform(y_int_maths, y_int_maths_2))

		yint_and_label = plane.add_point((0, 10), RED, plane.get_axes().coords_to_point(0, 10) + LEFT*1.5, RED)
		self.play(Create(yint_and_label[0]), Write(yint_and_label[1]), FadeOut(y_int_maths))
		self.wait(2)


		# Create 6 points
		fam_points = [(1, 88), (2, 84), (3, 46), (4, 22), (5, 60), (6, 208)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		point_group, label_group = VGroup(), VGroup()

		i = 0
		for point in fam_points:
			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN

			point_and_label = plane.add_point(point, colours[i], plane.get_axes().coords_to_point(*point) + pos*0.5, colours[i])

			point_group.add(point_and_label[0])
			label_group.add(point_and_label[1])
			self.play(Create(point_and_label[0]), Write(point_and_label[1]))

			i += 1
		self.wait(2)


		# Calculate the new graph mod 7
		new_label = MathTex("P(x) = 8x^{3} - 65x^{2} + 135x + 10 \\pmod{7}", font_size=36, color=BLACK).move_to(UP*3)
		self.play(Transform(curve_label, new_label))
		self.wait(2)


		new_label_2 = MathTex("P(x) = x^{3} + 5x^{2} + 2x + 3 \\pmod{7}", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Write(new_label_2))
		self.wait(2)


		polynomial_2 = Polynomial(plane.get_axes(), lambda x: x*x*x + 5*x*x + 2*x + 3)

		curve_2, curve_label_2 = polynomial_2.draw_polynomial([-1, 7], "P(x) = x^{3} + 5x^{2} + 2x + 3 \\pmod{7}", UP*3, BLACK, label_font_size=36)
		self.play(
			Transform(curve, curve_2), 
			Transform(curve_label, curve_label_2), 
			FadeOut(new_label_2),
			FadeOut(plane.get_points())
		)
		self.wait(2)


		# Morph the new graph into the mod 7 version
		plane_2 = Plane(([-1, 7, 1], [0, 10, 1]))
		plane_2.set_colour(BLACK)
		plane_2.get_axes().move_to(UP*0.75)


		# Morph it into the mod 7 version
		polynomial_3 = Polynomial(plane.get_axes(), lambda x: x*x*x + 5*x*x + 2*x + 3)
		curve_3, curve_label_3 = polynomial_3.draw_polynomial([-1, 7], "", UP*3, BLACK, label_font_size=36)
		polynomial_3.morph_polynomial(self, lambda x: (x*x*x + 5*x*x + 2*x + 3) % 7, [0, 6, 0.001], BLACK)


		# Change the scale
		polynomial_4 = plane_2.draw_polynomial_as_dots([0, 6], [0, 6], lambda x: (x*x*x + 5*x*x + 2*x + 3) % 7, BLACK)
		self.play(
			FadeOut(curve),
			Transform(plane.get_axes(), plane_2.get_axes()),
			FadeOut(polynomial_3.get_polynomial()),
			FadeIn(polynomial_4),
			run_time=2
		)
		self.wait(2)


		# Fade in the dots
		for i in range(0, 7):
			plane_2.add_point((i, (i*i*i + 5*i*i + 2*i + 3) % 7), BLACK, ORIGIN, WHITE, label_text="", radius=0.04)
		self.play(FadeIn(plane_2.get_points()))
		self.play(polynomial_4.animate.set_color(GRAY_A))
		self.wait(2)


		yint_and_label = plane_2.add_point((0, 3), RED, plane_2.get_axes().coords_to_point(0, 3) + LEFT*1.5, RED)
		self.play(Create(yint_and_label[0]), Write(yint_and_label[1]))
		self.wait(2)


		# Calculate share 1
		share_1_maths = MathTex("P(1) = 1^{3} + 5 \\cdot 1^{2} + 2 \\cdot 1 + 3", " = 11", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(Write(share_1_maths))
		self.wait(2)

		share_1_maths_mod = MathTex("P(1) = 1^{3} + 5 \\cdot 1^{2} + 2 \\cdot 1 + 3", "\\equiv 4 \\pmod{7}", font_size=24, color=BLACK).next_to(curve_label, DOWN)
		self.play(TransformMatchingTex(share_1_maths, share_1_maths_mod))
		self.wait(2)

		point_group, label_group = VGroup(), VGroup()
		point_and_label = plane_2.add_point((1, 4), ORANGE, plane_2.get_axes().coords_to_point(*(1, 4)) + (RIGHT+UP)*0.5, ORANGE)
		
		point_group.add(point_and_label[0])
		label_group.add(point_and_label[1])
		self.play(Create(point_and_label[0]), Write(point_and_label[1]))	
		self.play(FadeOut(share_1_maths_mod))	
		self.wait(2)


		# Create remaining 5 points
		fam_points = [(2, 0), (3, 4), (4, 1), (5, 4), (6, 5)]
		colours = [GOLD, GREEN, TEAL, BLUE, PURPLE]		

		i = 0
		for point in fam_points:
			pos = RIGHT+UP
			point_and_label = plane_2.add_point(point, colours[i], plane_2.get_axes().coords_to_point(*point) + pos*0.5, colours[i])

			point_group.add(point_and_label[0])
			label_group.add(point_and_label[1])
			self.play(Create(point_and_label[0]), Write(point_and_label[1]))

			i += 1
		self.wait(2)


		# Move the points to the family members
		move_point_anim = []
		for i in range(0, len(label_group)):
			move_point_anim.append(label_group[i].animate.next_to(family_group[i], UP))
		self.play(*move_point_anim)
		self.wait(2)



class RandomText(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		random = Text("You would now randomly select k-1 coefficients from your finite field", font_size=20, color=BLACK)
		self.play(Write(random))
		random_2 = Text("{ Integers in the range [0, p-1] }", font_size=20, color=BLACK).next_to(random, DOWN)
		self.play(Write(random_2))
		self.wait(5)


class RandomText2(Scene):

	def construct(self):
		Text.set_default(font="Monospace")
		
		random = Text("In this example, let's use 3 as the secret key", font_size=20, color=BLACK)
		self.play(Write(random))
		self.wait(5)