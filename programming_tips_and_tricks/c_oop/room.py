from manim import *

from constants import *


FILL_OPACITY = 0.8


class Room:
	def __init__(self):
		self.room = self.make_room()


	def get_room(self):
		return self.room

	def get_roof(self):
		return self.room[1]


	def make_skirting_board(self):
		return Rectangle(width=20, height=0.5, fill_color=BLUE_E, fill_opacity=FILL_OPACITY, stroke_color=BLUE_E)


	def make_roof(self):
		return Rectangle(width=20, height=1, fill_color=BLUE, fill_opacity=0.2, stroke_color=BLUE)


	def make_door(self):
		DOOR_WIDTH, DOOR_HEIGHT = 2, 4

		door = Rectangle(
			width=DOOR_WIDTH, height=DOOR_HEIGHT,
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=1
		)

		# Panels
		panel_1 = Rectangle(
			width=0.7*DOOR_WIDTH, height=0.4*DOOR_HEIGHT,
			stroke_color=DARK_BROWN,
			fill_color=DARK_BROWN,
			fill_opacity=FILL_OPACITY
		)

		panel_2 = Rectangle(
			width=0.7*DOOR_WIDTH, height=0.3*DOOR_HEIGHT,
			stroke_color=DARK_BROWN,
			fill_color=DARK_BROWN,
			fill_opacity=FILL_OPACITY
		)

		panels = VGroup(panel_1, panel_2).arrange(DOWN, buff=0.4).move_to(door.get_center())


		# Handle
		handle = Circle(
			radius=0.2, 
			color=GRAY_D, 
			stroke_color=GRAY_D, 
			fill_opacity=FILL_OPACITY
		).move_to(door.get_center() + RIGHT*0.8*(DOOR_WIDTH/2) + DOWN*0.2)


		return VGroup(door, panels, handle)


	def make_plant(self):
		plant = Ellipse(width=0.5, height=4, color=GREEN, fill_opacity=FILL_OPACITY)
		plant_2 = Ellipse(width=0.5, height=1, color=GREEN, fill_opacity=FILL_OPACITY).rotate(-PI/3).move_to(plant.get_center()+RIGHT*0.3+UP)
		pot = Sector(radius=2, start_angle=0, angle=-PI, color=DARK_BROWN, fill_opacity=1)
		full_plant = VGroup(VGroup(plant, plant_2), pot).arrange(DOWN, buff=0)
		full_plant[0].shift(RIGHT*0.2)
		return full_plant


	def make_table(self):
		TABLE_WIDTH, TABLE_HEIGHT, LEG_HEIGHT = 5, 0.5, 1.5

		top = Rectangle(
			width=TABLE_WIDTH, height=TABLE_HEIGHT,
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=FILL_OPACITY
		)

		leg_1 = Rectangle(
			width=TABLE_HEIGHT, height=LEG_HEIGHT,
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=FILL_OPACITY
		)

		leg_2 = leg_1.copy()

		legs = VGroup(leg_1, leg_2).arrange(RIGHT, buff=2)

		return VGroup(top, legs).arrange(DOWN, buff=0)


	def make_chair(self, flipped=False):
		CHAIR_COLOUR = GRAY_D

		CHAIR_WIDTH, CHAIR_HEIGHT = 0.25, 2
		back = Rectangle(
			width=CHAIR_WIDTH, height=CHAIR_HEIGHT,
			stroke_color=CHAIR_COLOUR,
			fill_color=CHAIR_COLOUR,
			fill_opacity=FILL_OPACITY
		)

		SEAT_WIDTH = 1.25
		seat = Rectangle(
			width=SEAT_WIDTH, height=CHAIR_WIDTH,
			stroke_color=CHAIR_COLOUR,
			fill_color=CHAIR_COLOUR,
			fill_opacity=FILL_OPACITY
		)

		chair = VGroup(back, seat).arrange(DOWN, buff=0)
		back_shift = LEFT if not flipped else RIGHT
		back.shift(back_shift*(SEAT_WIDTH/2 - CHAIR_WIDTH/2))
		return chair


	def make_window(self):
		WINDOW_WIDTH, WINDOW_HEIGHT = 4.5, 2.5
		window = Rectangle(
			width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
			stroke_color=DARK_BROWN,
			stroke_width=20,
			fill_color=BLUE,
			fill_opacity=FILL_OPACITY
		)

		sun = Circle(
			radius=0.3,
			stroke_color=YELLOW,
			fill_color=YELLOW,
			fill_opacity=FILL_OPACITY
		).move_to(window.get_center() + UP*(0.4*WINDOW_HEIGHT/2) + RIGHT*(0.6*WINDOW_WIDTH/2))

		return VGroup(window, sun)


	def make_room(self):
		sb = self.make_skirting_board().move_to(DOWN*4)
		roof = self.make_roof().move_to(UP*3.5)
		door = self.make_door().scale(1.2).move_to(DOWN*1.8 + LEFT*5)
		plant = self.make_plant().move_to(DOWN*1.6 + LEFT*3.25)
		table = self.make_table().move_to(DOWN*3 + RIGHT*2)
		chair_one = self.make_chair().move_to(DOWN*2.35 + LEFT*2)
		chair_two = self.make_chair(flipped=True).move_to(DOWN*2.35 + RIGHT*6)
		window = self.make_window().move_to(RIGHT*3 + UP)

		return VGroup(sb, roof, door, plant, table, chair_one, chair_two, window)
