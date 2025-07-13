from manim import *
from entities import *

import random
import math


class Plane:
	def __init__(self, xy_range, xy_length=None, include_numbers=True, include_axes_labels=True):
		self.xy_range = xy_range
		self.xy_length = xy_length
		self.include_numbers = include_numbers
		self.include_axes_labels = include_axes_labels

		self.axes = Axes(
			x_range=self.xy_range[0],
			y_range=self.xy_range[1],
			tips=False,
			axis_config={"include_numbers": self.include_numbers, "font_size": 18},
		)

		if self.xy_length != None:
			self.axes = Axes(
				x_range=self.xy_range[0],
				y_range=self.xy_range[1],
				x_length=self.xy_length[0],
				y_length=self.xy_length[1],
				tips=False,
				axis_config={"include_numbers": self.include_numbers, "font_size": 18},
			)

		self.axis_labels = None
		if self.include_axes_labels:
			self.axis_labels = self.axes.get_axis_labels(x_label="x", y_label="y")

		self.points = VGroup()


	def set_xy_length(self, xy_length):
		self.axes.x_length = xy_length[0]
		self.axes.y_length = xy_length[1]

	def set_colour(self, colour):
		self.axes.set_color(colour)


	def get_axes(self):
		return self.axes

	def get_axis_labels(self):
		return self.axis_labels

	def get_axes_and_labels(self):
		return VGroup(self.axes, self.axis_labels)

	def get_points(self):
		return self.points


	def add_point(self, coordinates, colour, label_position, label_colour, label_text=None, label_font_size=24):
		point = Dot(self.axes.coords_to_point(*coordinates), color=colour)

		if label_text == None:
			label_text = str(coordinates)
		point_label = MathTex(label_text, font_size=label_font_size, color=label_colour).move_to(label_position)

		point_and_label = VGroup(point, point_label)
		self.points.add(point_and_label)

		return point_and_label



class PolynomialSet:
	def __init__(self, axes, parametric, a_start_end):
		self.axes = axes
		self.parametric = parametric

		self.a_start = a_start_end[0]
		self.a_end = a_start_end[1]
		self.a_tracker = ValueTracker(self.a_start)

		self.polynomials = VGroup()


	def get_polynomials(self):
		return self.polynomials

	def get_a_tracker(self):
		return self.a_tracker


	def get_line_colour(self, a):
		if self.a_start == None or self.a_end == None:
			print("Define the start and end of the parameter")

		a_range, gradient_steps = self.a_end - self.a_start, 100

		return color_gradient(
			[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], 
			gradient_steps
		)[int((a - self.a_start)/a_range * (gradient_steps-1))]


	def draw_polynomial(self, a, x_range, label_text, label_position, colour=None):
		if colour is None:
			colour = self.get_line_colour(a)

		curve = self.axes.plot(self.parametric(a), x_range=x_range, color=colour)
		curve_label = MathTex(label_text, font_size=24, color=colour).move_to(label_position)

		curve_group = VGroup(curve, curve_label)
		self.polynomials.add(curve_group)

		return curve_group


	def get_line(self, x_range, colour=None):
		a = self.a_tracker.get_value()

		if colour is None:
			colour = self.get_line_colour(a)

		if x_range == None:
			x_range = self.axes.x_range
		else:
			if callable(x_range):
				x_range = x_range(a)

		return self.axes.plot(
			self.parametric(a),
			x_range=x_range,
			color=colour,
			stroke_width=4
		)


	def get_equation(self, equation_text, equation_position, colour=None):
		a = self.a_tracker.get_value()

		if colour is None:
			colour = self.get_line_colour(a)

		equation = MathTex(
		    equation_text(a),
		    color=colour,
		    font_size=24
		)
		equation.move_to(equation_position)

		return equation


	def get_y_int(self, plane, colour=None):
		a = self.a_tracker.get_value()

		if colour is None:
			colour = RED

		yint_and_label = plane.add_point(
			(0, self.parametric(a)(0)), colour, 
			plane.get_axes().coords_to_point(0, self.parametric(a)(0)) + LEFT*1.5, colour,
			label_text=f"(0, {self.parametric(a)(0):.2f})"
		)

		return yint_and_label


	def animate_a_tracker(self, scene, run_time):
		scene.play(self.a_tracker.animate.set_value(self.a_end), run_time=run_time, rate_func=linear)



class Polynomial:
	def __init__(self, axes, equation):
		self.axes = axes
		self.equation = equation

		self.polynomial = VGroup()
		self.polynomial_label = VGroup()
		self.polynomial_and_label = VGroup()


	def get_y_value(self, x):
		return self.equation(x)

	def get_polynomial(self):
		return self.polynomial

	def get_label(self):
		return self.polynomial_label

	def get_polynomial_and_label(self):
		return self.polynomial_and_label


	def draw_polynomial(self, x_range, label_text, label_position, colour, label_font_size=24):
		curve = self.axes.plot(self.equation, x_range=x_range, color=colour)
		curve_label = MathTex(label_text, font_size=label_font_size, color=colour).move_to(label_position)
		curve_group = VGroup(curve, curve_label)

		self.polynomial = curve
		self.polynomial_label = curve_label
		self.polynomial_and_label = curve_group

		return curve_group