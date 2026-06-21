import random

from manim import *

class BurgerStore:
	def __init__(self):
		self.burger_store = self.make_burger_store()


	def get_burger_store(self):
		return self.burger_store

	def get_wall(self):
		return self.burger_store[0]

	def get_poster(self):
		return self.burger_store[1]

	def get_counter(self):
		return self.burger_store[2]


	def make_wall(self):
		up_min, up_max = -10, 10
		left_min, left_max = -14, 14
		brick_width, brick_height = 1, 0.5

		wall = VGroup()

		cur_up = up_min
		while cur_up <= up_max:

			cur_left = left_min
			left_offset = random.uniform(-0.8, 0.8)

			while cur_left <= left_max:
				brick = Rectangle(
					width=brick_width, height=brick_height,
					stroke_color="DARK_BROWN",
					fill_color="DARK_BROWN",
					fill_opacity=0.5
				).move_to(UP*cur_up + LEFT*(cur_left+left_offset))

				wall.add(brick)
				cur_left += brick_width+0.2

			cur_up += brick_height+0.2

		return wall


	@staticmethod
	def make_burger():
		burger_width = 2.75

		bun = RoundedRectangle(
			width=burger_width, height=0.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=1
		)

		lettuce = RoundedRectangle(
			width=burger_width, height=0.2,
			corner_radius=[0.1, 0.1, 0.1, 0.1],
			stroke_color=GREEN,
			fill_color=GREEN,
			fill_opacity=1
		)

		tomato = Rectangle(
			width=burger_width-0.25, height=0.2,
			stroke_color=RED,
			fill_color=RED,
			fill_opacity=1
		)

		meat = RoundedRectangle(
			width=burger_width-0.05, height=0.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color=DARK_BROWN,
			fill_color=DARK_BROWN,
			fill_opacity=1
		)

		burger = VGroup(bun, lettuce, tomato, meat, bun.copy()).arrange(DOWN, buff=0)
		return burger


	def make_poster(self):
		poster = RoundedRectangle(
			width=13, height=4,
			stroke_color=GRAY_C,
			fill_color=BLACK,
			fill_opacity=0.9
		).shift(UP*1.5)

		burger = BurgerStore.make_burger()
		burger.scale(0.5).move_to(UP*2.5+LEFT*4)

		writing = RoundedRectangle(
			width=12, height=0.15,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=GRAY_B,
			fill_color=GRAY_B,
			fill_opacity=1
		)
		text = VGroup(writing, writing.copy(), writing.copy(), writing.copy()).arrange(DOWN, buff=0.5).scale(0.5).next_to(burger, RIGHT, buff=2)

		full_poster = VGroup(poster, burger, text)
		return full_poster


	def make_counter(self):
		bottom = Rectangle(
			width=13.5, height=3,
			stroke_color="GRAY_C",
			fill_color="GRAY_C",
			fill_opacity=1
		)

		top = RoundedRectangle(
			width=14, height=0.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_D",
			fill_color="GRAY_D",
			fill_opacity=1
		).move_to(bottom.get_top())		

		counter = VGroup(bottom, top).shift(DOWN*3)
		return counter


	def make_burger_store(self):
		wall = self.make_wall()
		poster = self.make_poster()
		counter = self.make_counter()

		burger_store = VGroup(wall, poster, counter)
		return burger_store