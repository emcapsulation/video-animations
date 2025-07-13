from manim import *
from polynomials import *

import random
import math



class Human:
	def __init__(self, colour, fill_opacity):
		self.colour = colour
		self.fill_opacity = fill_opacity
		self.human = self.make_human()


	def get_human(self):
		return self.human

	def get_body(self):
		return self.human[0]

	def get_label(self):
		return self.human[1]


	def make_human(self):
		head = Circle(color=self.colour, fill_opacity=self.fill_opacity, radius=1)
		body = Arc(color=self.colour, fill_opacity=self.fill_opacity, radius=1.5, angle=PI)
		human = VGroup(head, body).arrange(DOWN)

		return VGroup(human)


	def add_label(self, label, label_colour):
		label = Text(label, font_size=30, color=label_colour).next_to(self.human, UP)
		self.human.add(label)

		return self



class Family:
	def __init__(self, fill_opacity, human_size, group_size, positions):
		self.fill_opacity = fill_opacity
		self.human_size = human_size
		self.group_size = group_size
		self.positions = positions

		self.label_colour = WHITE
		self.labels = ["Grandpa", "Uncle", "Dad", "Mum", "Brother", "You"]
		self.colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]

		# VGroup of the manim objects
		self.family_group = None

		# List of the actual classes
		self.family_list = None


	def get_family_list(self):
		if self.family_list == None:
			self.family_list = self.make_family_list()
		return self.family_list

	def get_family_group(self):
		if self.family_group == None:
			self.family_group = self.make_family_group()
		return self.family_group

	def get_family_list_member(self, label):
		return self.family_list[self.labels.index(label)]

	def get_family_group_member(self, label):
		return self.family_group[self.labels.index(label)]


	def set_labels(self, labels):
		self.labels = labels

	def set_colours(self, colours):
		self.colours = colours

	def set_label_colour(self, label_colour):
		self.label_colour = label_colour


	def make_family_list(self):
		family_list = []

		for i in range(0, len(self.labels)):
			family_member = Human(self.colours[i], self.fill_opacity).add_label(self.labels[i], self.label_colour)
			family_member.get_human().scale(self.human_size).move_to(self.positions[i])
			family_list.append(family_member)

		return family_list

	def make_family_group(self):
		family_group = VGroup()

		for i in range(0, len(self.labels)):
			family_member = Human(self.colours[i], self.fill_opacity).add_label(self.labels[i], self.label_colour)
			family_member.get_human().scale(self.human_size).move_to(self.positions[i])
			family_group.add(family_member.get_human())

		family_group.scale(self.group_size)
		return family_group



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



class SecretSauce:
	def __init__(self, type):
		self.type = type
		self.secret_sauce = self.make_secret_sauce()
		self.secret_sauce_with_background = self.make_secret_sauce_with_background()


	def get_secret_sauce(self):
		return self.secret_sauce

	def get_secret_sauce_with_background(self):
		return self.secret_sauce_with_background

	def get_paper(self):
		return self.secret_sauce[0]

	def get_title(self):
		return self.secret_sauce[1]

	def get_lines(self):
		return self.secret_sauce[2]

	def get_background(self):
		return self.secret_sauce_with_background[0]


	def make_secret_sauce(self):
		secret_sauce = VGroup()		

		paper = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=LOGO_WHITE,
			fill_opacity=0.85
		)


		title = None
		if self.type == "shapes" or self.type == "text":
			title = Text(
				"Secret Sauce",
				color=BLACK,
				font_size=22
			).shift(UP*1.1)

		elif self.type == "encrypted":
			title = Text(
				"qL7#xP$v@Kf2!W",
				color=BLACK,
				font_size=22
			).shift(UP*1.1)


		lines = None
		if self.type == "shapes":
			writing = RoundedRectangle(
				width=3.6, height=0.15,
				corner_radius=[0.05, 0.05, 0.05, 0.05],
				stroke_color=BLACK,
				fill_color=BLACK,
				fill_opacity=1
			)
			lines = VGroup(
				writing, 
				writing.copy(), 
				writing.copy(), 
				writing.copy(), 
				writing.copy(), 
				writing.copy()
			).arrange(DOWN, buff=0.5).scale(0.5).shift(DOWN*0.5)

		elif self.type == "text":
			text_1 = Text("2 tbsp mayonnaise", font_size=16, color=BLACK)
			text_2 = Text("2 tbsp ketchup", font_size=16, color=BLACK)
			text_3 = Text("1 tbsp mustard", font_size=16, color=BLACK)
			text_4 = Text("1 tsp paprika", font_size=16, color=BLACK)
			text_5 = Text("1 clove garlic", font_size=16, color=BLACK)
			lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

		elif self.type == "encrypted":
			text_1 = Text("f9@Lz#Wq8v!2Xp$N", font_size=16, color=BLACK)
			text_2 = Text("B#v5$eYp!tn8Wz@J", font_size=16, color=BLACK)
			text_3 = Text("xM7&rA^Fz3@b!gPL", font_size=16, color=BLACK)
			text_4 = Text("Z!uT@p#qE9*WsLd^", font_size=16, color=BLACK)
			text_5 = Text("r%NyB!q2$GKz*vM@", font_size=16, color=BLACK)
			lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

		secret_sauce.add(paper, title, lines)
		return secret_sauce


	def make_secret_sauce_with_background(self):
		circle = Circle(
			radius=3,
			color=GOLD_A,
			fill_opacity=0.85
		)

		secret_sauce_with_background = VGroup(circle, self.secret_sauce)
		return secret_sauce_with_background



class SpeechBubble:
	def __init__(self, colour, width, height):
		self.speech_bubble = RoundedRectangle(
			width=width, height=height, 
			fill_color=colour, stroke_color=colour,
			corner_radius=0.2, fill_opacity=0.1
		)


	def get_speech_bubble(self):
		return self.speech_bubble



class Key:
	def __init__(self, colour):
		self.colour = colour
		self.key = self.make_key()


	def get_key(self):
		return self.key


	def make_key(self):
		annulus = Annulus(inner_radius=0.5, outer_radius=1, color=self.colour)

		stick = RoundedRectangle(
			width=2.5, height=0.5,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=self.colour,
			fill_color=self.colour,
			fill_opacity=1
		)

		little_stick = RoundedRectangle(
			width=0.25, height=1,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=self.colour,
			fill_color=self.colour,
			fill_opacity=1
		)

		little_sticks = VGroup(little_stick, little_stick.copy()).arrange(RIGHT)

		key = VGroup(
			annulus,
			stick.move_to(annulus.get_center() + RIGHT*1.8),
			little_sticks.move_to(stick.get_right() + LEFT*0.5+DOWN*0.4)
		)

		return key
