from manim import *


class Item:
	def __init__(self, type, value, weight):
		self.value = value
		self.weight = weight

		if type == "suitcase":
			self.item = Item.make_suitcase()
		elif type == "camera":
			self.item = Item.make_camera()
		elif type == "pen":
			self.item = Item.make_pen()
		elif type == "sneakers":
			self.item = Item.make_sneakers()
		elif type == "toothbrush":
			self.item = Item.make_toothbrush()
		elif type == "headphones":
			self.item = Item.make_headphones()
		elif type == "dot":
			self.item = Item.make_dot()


	def make_suitcase():
		return RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		)


	def make_camera():
		camera_body = RoundedRectangle(
			width=1.2, height=0.8,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		)
		lens = Circle(
			radius=0.2,
			color=BLACK,
			fill_opacity=0.5
		).move_to(camera_body.get_center() + RIGHT*0.25)
		camera = VGroup(camera_body, lens)

		return camera


	def make_pen():
		pen_body = Rectangle(
			width=1.5, height=0.25,
			color=BLUE,
			fill_opacity=0.5
		)
		nib = Triangle(
			color=WHITE,
			fill_opacity=0.5
		).scale(0.15)
		nib.rotate(5*PI/6, about_point=nib.get_center()).move_to(pen_body.get_right() + RIGHT*0.15)
		pen = VGroup(pen_body, nib)

		return pen


	def make_sneakers():
		shoe = RoundedRectangle(
			width=0.5, height=0.8,
			corner_radius=0.2,
			color=WHITE,
			fill_opacity=0.5
		)
		sneakers = VGroup(shoe, shoe.copy()).arrange(RIGHT)

		return sneakers


	def make_toothbrush():
		toothbrush_body = Rectangle(
			width=1.9, height=0.2,
			color=WHITE,
			fill_opacity=0.5
		)
		brushes = RoundedRectangle(
			width=0.4, height=0.25,
			corner_radius=0.1,
			color=RED,
			fill_opacity=0.5
		).move_to(toothbrush_body.get_top() + UP*0.125 + RIGHT*0.71)
		toothbrush = VGroup(toothbrush_body, brushes)

		return toothbrush


	def make_headphones():
		headphone = RoundedRectangle(
			width=0.4, height=0.7,
			corner_radius=0.2,
			color=GRAY_D,
			fill_opacity=0.5
		)
		band = Arc(
			radius=0.7, angle=PI,
			color=GRAY_D
		)
		headphones = VGroup(headphone.shift(LEFT*0.4 + DOWN*0.15), band, headphone.copy().shift(RIGHT*0.8))

		return headphones


	def make_dot():
		return Dot(radius=0.2)