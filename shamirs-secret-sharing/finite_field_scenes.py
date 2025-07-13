from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#3273a8"


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
