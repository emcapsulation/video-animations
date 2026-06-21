from manim import *

class Usb:
	def __init__(self):
		self.usb = self.make_usb()


	def make_usb(self):
		body = RoundedRectangle(
			width=0.8, height=0.3,
			corner_radius=[0.05, 0.05, 0, 0],
			stroke_color=RED,
			fill_color=RED,
			fill_opacity=1
		)

		head = RoundedRectangle(
			width=0.2, height=0.2,
			corner_radius=[0, 0, 0.05, 0.05],
			stroke_color=GRAY,
			fill_color=GRAY,
			fill_opacity=1
		)

		return VGroup(body, head).arrange(RIGHT, buff=0)