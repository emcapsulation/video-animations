from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#5574c2"


class FiniteField(Scene):

	def get_number_line(self, scale_tracker):
			scale = scale_tracker.get_value()
			x_min, x_max = -5 * scale, 5 * scale

			line = NumberLine(
				x_range=[int(x_min), int(x_max), int(scale)],
				length=10,
				include_numbers=True,
				include_tip=False,
				stroke_width=2,
			)

			return line


	def bounce_path(self, number_line, x1, x2):
		p1 = number_line.n2p(x1)
		p2 = number_line.n2p(x2)

		angle = PI
		if x1 < x2:
			angle=-PI

		return ArcBetweenPoints(p1, p2, angle=angle)		


	def bounce_path_ring(self, target_numbers, directions, x1, x2, angle):
		p1 = target_numbers[x1].get_center() + directions[x1]
		p2 = target_numbers[x2].get_center() + directions[x2]

		return ArcBetweenPoints(start=p1, end=p2, angle=angle)	


	def wrap_numbers_around_ring(self, start, end, centre, radius):
		wrap_numbers = VGroup()

		for num in range(start, end+1, 1):
			mod_seven = num%7

			up = math.sin(mod_seven*2*PI/7)
			right = math.cos(mod_seven*2*PI/7)
			direction = UP*up + RIGHT*right

			colour = WHITE
			if num//7 == 1:
				colour = GRAY_A
			elif num//7 == 2:
				colour = GRAY_B
			elif num//7 == 3:
				colour = GRAY_C

			tick_centre = centre + radius*direction
			number = Text(str(num), font_size=24, color=colour).move_to(tick_centre + 0.4*(num//7 + 1)*direction)
			wrap_numbers.add(number)

		return wrap_numbers


	def construct(self):
		Text.set_default(font="Monospace")


		colour_gradient = (TEAL, BLUE, PURPLE)


		# Show the number line zooming out
		scale_tracker = ValueTracker(1)
		number_line = always_redraw(lambda: self.get_number_line(scale_tracker))
		self.add(number_line)
		self.wait(1)

		self.play(
			scale_tracker.animate.set_value(100),
			run_time=10,
			rate_func=rate_functions.ease_in_out_cubic
		)
		self.wait(2)


		# Replace with 0-6
		nl_six = NumberLine(
			x_range=[0, 6, 1],
			length=10,
			include_numbers=True,
			include_tip=False,
			stroke_width=2,
		)
		self.play(ReplacementTransform(number_line, nl_six))
		self.wait(2)


		# Addition
		arithmetic = Text("4 + 3", color=WHITE).move_to(UP*2)
		self.play(Write(arithmetic))
		self.wait(2)

		ball = Dot(color=TEAL, radius=0.2).move_to(nl_six.n2p(4) + UP*0.2)
		self.add(ball)		

		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, 4, 5)))
		self.wait(0.5)
		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, 5, 6)))
		self.wait(1)

		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, 6, 9)))
		self.remove(ball)
		self.wait(0.25)

		ball = Dot(color=TEAL, radius=0.2).move_to(nl_six.n2p(0) + LEFT*3 + UP*3)
		self.add(ball)
		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, -3, 0)))
		self.wait(1)

		arithmetic_2 = Text("4 + 3 = 0", color=WHITE).move_to(UP*2)
		self.play(Transform(arithmetic, arithmetic_2))
		self.wait(2)


		# Subtraction
		arithmetic_3 = Text("0 - 1", color=WHITE).move_to(UP*2)
		self.play(Transform(arithmetic, arithmetic_3))
		self.wait(2)

		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, 0, -3)))
		self.remove(ball)
		self.wait(0.25)

		ball = Dot(color=TEAL, radius=0.2).move_to(nl_six.n2p(0) + RIGHT*3 + UP*3)
		self.add(ball)
		self.play(MoveAlongPath(ball, self.bounce_path(nl_six, 9, 6)))
		self.wait(1)

		arithmetic_4 = Text("0 - 1 = 6", color=WHITE).move_to(UP*2)
		self.play(Transform(arithmetic, arithmetic_4))
		self.wait(2)


		self.play(FadeOut(arithmetic))


		# Morph into a ring
		ticks, numbers = VGroup(), VGroup()
		numbers = VGroup()
		for mob in nl_six.get_family():
			if isinstance(mob, Line):
				ticks.add(mob)
			if isinstance(mob, DecimalNumber):
				numbers.add(mob)


		centre, radius, total = ORIGIN+DOWN*0.5, 2, 7
		angle_step = (2*PI)/total

		target_ticks, target_numbers = VGroup(), VGroup()
		directions = []
		for i in range(total):
			up = math.sin(i*2*PI/total)
			right = math.cos(i*2*PI/total)
			direction = UP*up + RIGHT*right
			directions.append(direction)

			tick_centre = centre + radius*direction
			tick = Line(
				tick_centre,
				tick_centre + 0.2*direction
			)

			number = Text(str(i), font_size=24).move_to(tick_centre + 0.4*direction)
			target_ticks.add(tick)
			target_numbers.add(number)


		ring = Circle(radius=radius, stroke_color=WHITE).move_to(centre)

		transform_ticks_anim, transform_numbers_anim = [], []
		for i in range(0, 7):
			transform_ticks_anim.append(Transform(ticks[i], target_ticks[i]))
			transform_numbers_anim.append(Transform(numbers[i], target_numbers[i]))

		self.play(
			*transform_ticks_anim,
			*transform_numbers_anim,
			Create(ring),
			ball.animate.move_to(target_numbers[0].get_center() + RIGHT),
			run_time=2
		)
		
		self.wait(2)


		# Subtraction around the ring
		subtraction = Text("0 - 1 = 6", font_size=24, gradient=colour_gradient).move_to(centre)
		self.play(Write(subtraction))

		self.play(MoveAlongPath(ball, self.bounce_path_ring(target_numbers, directions, 0, 6, -PI)))
		self.wait(1)

		self.play(FadeOut(subtraction))


		# Addition around the ring
		addition = Text("6 + 2 = 1", font_size=24, gradient=colour_gradient).move_to(centre)
		self.play(Write(addition))

		self.play(MoveAlongPath(ball, self.bounce_path_ring(target_numbers, directions, 6, 0, PI)))
		self.play(MoveAlongPath(ball, self.bounce_path_ring(target_numbers, directions, 0, 1, PI)))
		self.wait(1)

		self.play(FadeOut(addition), FadeOut(ball))
		self.wait(2)


		# Arithmetic introduction
		twelve = Text("12", font_size=24).move_to(RIGHT*4 + DOWN*2)
		self.play(Write(twelve))
		self.wait(2)


		title = Text("Modular Arithmetic", color=WHITE).move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		twelve_mod_seven = Text("12 mod 7 = 5", font_size=24, gradient=colour_gradient).move_to(centre)
		self.play(Write(twelve_mod_seven))
		self.wait(2)


		# Wrap the numbers around the ring
		wrap_numbers = self.wrap_numbers_around_ring(7, 12, centre, radius)
		for num in wrap_numbers:
			self.play(Write(num))			

		congruence = MathTex("12 \\equiv 5 \\pmod{7}", font_size=36, color=colour_gradient).move_to(centre)
		self.play(FadeOut(twelve), Transform(twelve_mod_seven, congruence))
		self.wait(2)


		wrap_numbers_2 = self.wrap_numbers_around_ring(13, 27, centre, radius)
		for num in wrap_numbers_2:
			self.play(Write(num))

		congruence = MathTex("6 \\times 4 = 24 \\equiv 3 \\pmod{7}", font_size=30, color=colour_gradient).move_to(centre)
		self.play(Transform(twelve_mod_seven, congruence))
		self.wait(2)


		# Introduce the finite field
		finite_field = MathTex("\\mathbb{F}_7", color=colour_gradient).move_to(centre)
		self.play(FadeOut(wrap_numbers), FadeOut(wrap_numbers_2))
		self.play(Transform(twelve_mod_seven, finite_field))
		self.wait(2)

		add = Text("+", color=TEAL).move_to(UP*2 + LEFT*4 + DOWN*0.5)
		self.play(Write(add))
		self.wait(1)

		mult = Text("x", color=BLUE).move_to(UP*2 + RIGHT*4 + DOWN*0.5)
		self.play(Write(mult))
		self.wait(1)

		sub = Text("-", color=PURPLE).move_to(DOWN*2 + LEFT*4 + DOWN*0.5)
		self.play(Write(sub))
		self.wait(1)

		div = Text("÷", color=LIGHT_PINK).move_to(DOWN*2 + RIGHT*4 + DOWN*0.5)
		self.play(Write(div))
		self.wait(1)



class FiniteFieldReasons(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		
		# Everything is an integer
		speech_bubble = SpeechBubble([LIGHT_PINK, PURPLE, BLUE, TEAL], 8, 1).get_speech_bubble().move_to(UP*3)
		self.play(Create(speech_bubble))

		speech1 = Text("Everything is an integer.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		plane = Plane(([0, 10], [0, 10]), xy_length=[9, 5])
		plane.get_axes().shift(DOWN*0.5)
		self.play(Create(plane.get_axes()))


		# Plot integer points
		colours = color_gradient([TEAL, BLUE, PURPLE, LIGHT_PINK], 11)
		for x in range(0, 11):
			point = (x, (5*x*x + 2*x + 9) % 11)
			plotted_point = plane.add_point(point, colours[x], ORIGIN, colours[x], label_text="")
			self.play(Create(plotted_point))
		self.wait(2)


		green_check = Text("☑", font_size=100, color=GREEN)
		self.play(SpinInFromNothing(green_check))
		self.wait(2)

		self.play(
			FadeOut(green_check),
			FadeOut(plane.get_axes()),
			FadeOut(plane.get_points())
		)


		# Everything is in the range 0 to p-1
		speech2 = Text("Everything is in the range 0 to p-1.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)


		plane = Plane(([0, 6, 1], [0, 1000, 100]), xy_length=[9, 5], include_numbers=False)
		plane.get_axes().shift(DOWN*0.5)
		self.play(Create(plane.get_axes()))


		big_polynomial = Polynomial(plane.get_axes(), lambda x: x**10 + 5)
		curve, curve_label = big_polynomial.draw_polynomial([0, 2.5], "P(x) = x^{100} + 5", UP, WHITE)
		self.play(Write(curve_label))
		self.wait(2)
		self.play(Create(curve), run_time=6)


		self.remove(
			big_polynomial.get_polynomial(),
			big_polynomial.get_label(),
			plane.get_axes(), 
			speech1,
			speech_bubble
		)

		sad_face = Text(":(", font_size=64)
		self.add(sad_face)		
		self.wait(2)


		# Information theoretic security
		speech_bubble = SpeechBubble([LIGHT_PINK, PURPLE, BLUE, TEAL], 8, 1).get_speech_bubble().move_to(UP*3)
		self.remove(sad_face)
		self.play(Create(speech_bubble))

		speech1 = Text("Guarantees information theoretic security.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		# Show the plane and shares
		plane = Plane(([0, 10], [0, 10]), xy_length=[9, 5])
		plane.get_axes().shift(DOWN*0.5)
		self.play(Create(plane.get_axes()))


		competitor = Human(MAROON_D, 0.8).get_human().scale(0.3).move_to(RIGHT*4)
		self.play(Create(competitor))


		# Plot integer points
		for x in range(1, 11, 3):
			point = (x, (5*x*x + 2*x + 9) % 11)
			plotted_point = plane.add_point(point, colours[x], ORIGIN, colours[x], label_text="")
			self.play(Create(plotted_point))
		self.wait(2)


		# Show all y intercepts being equally likely
		this_point = None
		for y in range(0, 11):
			if this_point is not None:
				self.play(FadeOut(this_point))

			this_point = plane.add_point((0, y), colours[0], ORIGIN, colours[0], label_text="")
			self.play(FadeIn(this_point))
			self.play(Indicate(this_point))


		question_mark = Text("?", color=MAROON_D).move_to(RIGHT*4)
		self.play(Transform(competitor, question_mark))
		self.wait(2)



class ModularDivision(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		fz = 64
		dividing = MathTex("6", "\\div", "3", "=", "2", font_size=fz)
		self.play(Write(dividing))
		self.wait(2)

		multiplying = MathTex("6", "\\times", "\\frac{1}{3}", "=", "2", font_size=fz)
		self.play(TransformMatchingTex(dividing, multiplying))
		self.wait(2)

		self.play(FadeOut(multiplying))


		dividing = MathTex("64", "\\div", "5", font_size=fz)
		self.play(Write(dividing))
		self.wait(2)

		multiplying = MathTex("64", "\\times", "\\frac{1}{5}", font_size=fz)
		self.play(TransformMatchingTex(dividing, multiplying))
		self.wait(2)

		reciprocal = MathTex("5", "\\times", "\\frac{1}{5}", font_size=fz)
		self.play(TransformMatchingTex(multiplying, reciprocal))
		self.wait(2)

		reciprocal_2 = MathTex("5", "\\times", "\\frac{1}{5}", "=", "1", font_size=fz)
		self.play(TransformMatchingTex(reciprocal, reciprocal_2))
		self.wait(2)

		self.play(FadeOut(reciprocal_2))


		dividing = MathTex("a", "\\div", "b", "\\pmod{m}", font_size=fz)
		self.play(Write(dividing))
		self.wait(2)

		multiplying = MathTex("a", "\\times", "b^{-1}", "\\pmod{m}", font_size=fz)
		self.play(TransformMatchingTex(dividing, multiplying))
		self.wait(2)

		inverse = MathTex("b", "\\times", "b^{-1}", "\\equiv 1", "\\pmod{m}", font_size=fz)
		self.play(TransformMatchingTex(multiplying, inverse))
		self.wait(2)

		self.play(FadeOut(inverse))
		


		def solve_fraction(numerator, denominator):
			dividing = MathTex("\\frac{%d}{%d}" % (numerator, denominator), "\\pmod{7}", font_size=fz)
			self.play(Write(dividing))
			self.wait(2)

			multiplying = MathTex("\\frac{%d}{%d}" % (numerator, denominator), "\\equiv", f"{numerator}", "\\times", "{%d}^{-1}" % (denominator), "\\pmod{7}", font_size=fz)
			self.play(TransformMatchingTex(dividing, multiplying))
			self.wait(2)

			self.play(multiplying.animate.shift(UP*3))


			inverse_group = VGroup()
			pos = 0
			res, cur = 0, 1
			while res != 1:
				res = (denominator*cur)%7
				colour = RED if res != 1 else GREEN

				inverse = MathTex(f"{denominator} \\cdot {cur} = {denominator*cur} \\equiv {res} \\pmod{7}", color=colour).move_to(DOWN*pos)
				self.play(Write(inverse))
				self.wait(1)

				inverse_group.add(inverse)
				pos += 1
				cur += 1
			self.wait(2)
			cur -= 1


			mult_copy = multiplying.copy()
			self.play(mult_copy.animate.shift(DOWN))

			answer = MathTex("\\equiv", f"{numerator}", "\\times", f"{cur}", "\\pmod{7}", font_size=fz).move_to(mult_copy.get_center() + RIGHT*1.5)
			self.play(TransformMatchingTex(mult_copy, answer))
			self.wait(2)

			answer_2 = MathTex("\\equiv", f"{numerator}", "\\times", f"{cur}", f"= {numerator*cur}", f"\\equiv {(numerator*cur)%7}", "\\pmod{7}", font_size=fz).move_to(mult_copy.get_center() + RIGHT*1.5)
			self.play(TransformMatchingTex(answer, answer_2))
			self.wait(2)


			self.play(FadeOut(inverse_group), 
				*[FadeOut(mob) for mob in self.mobjects])
			self.wait(2)

		solve_fraction(3, 2)
		solve_fraction(64, 5)



		finite_field = MathTex("\\mathbb{F}_p", font_size=64)
		self.play(Write(finite_field))

		finite_field_2 = MathTex("\\mathbb{F}_7", font_size=64)
		self.play(Transform(finite_field, finite_field_2))

		self.play(finite_field.animate.shift(UP*2))
		self.wait(2)


		table = [
			["a ", 0, 1, 2, 3, 4, 5, 6],
			["a^{-1}", "X", 1, 4, 5, 2, 3, 6]
		]

		table_group = VGroup()
		for i in range(0, len(table)):
			row = VGroup()

			for j in range(0, len(table[i])):
				cell = Text(str(table[i][j]))
				if j == 0:
					cell = MathTex(table[i][j], color=LIGHT_PINK, font_size=64)				
				row.add(cell)

			row.arrange(RIGHT, buff=1)
			table_group.add(row)

		table_group.arrange(DOWN, buff=1)
		table_group[1].shift(LEFT*0.4)

		for i in range(0, len(table_group)):
			for j in range(0, len(table_group[i])):
				self.play(Write(table_group[i][j]))
		self.wait(2)

