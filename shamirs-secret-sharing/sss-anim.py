from manim import *
import random
import math


def make_hooman(colour, fill_opacity=0.8):
	head = Circle(color=colour, fill_opacity=fill_opacity, radius=1)
	body = Arc(color=colour, fill_opacity=fill_opacity, radius=1.5, angle=PI)
	hooman = VGroup(head, body).arrange(DOWN)

	return hooman



def make_hooman_with_label(colour, label, scale, position):
	hooman = make_hooman(colour)
	label = Text(label, font_size=30).next_to(hooman, UP)
	hooman_and_label = VGroup(hooman, label).move_to(position).scale(scale)

	return hooman_and_label



class CheeseBurger(Scene):
	def make_wall(self):
		wall = VGroup()

		up = -10

		while up <= 10:
			left = -14
			add = random.uniform(-0.8, 0.8)

			while left <= 14:
				brick = Rectangle(
					width=1, height=0.5,
					stroke_color="DARK_BROWN",
					fill_color="DARK_BROWN",
					fill_opacity=0.5
				).move_to(UP*up + LEFT*(left+add))

				wall.add(brick)
				left += 1.2

			up += 0.7

		return wall


	def make_poster(self):	
		poster = RoundedRectangle(
			width=13, height=4,
			stroke_color=GRAY_C,
			fill_color=BLACK,
			fill_opacity=0.9
		).shift(UP*1.5)

		bun = RoundedRectangle(
			width=2.75, height=0.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color=LIGHT_BROWN,
			fill_color=LIGHT_BROWN,
			fill_opacity=1
		)

		lettuce = RoundedRectangle(
			width=2.75, height=0.2,
			corner_radius=[0.1, 0.1, 0.1, 0.1],
			stroke_color=GREEN,
			fill_color=GREEN,
			fill_opacity=1
		)

		tomato = Rectangle(
			width=2.5, height=0.2,
			stroke_color=RED,
			fill_color=RED,
			fill_opacity=1
		)

		meat = RoundedRectangle(
			width=2.7, height=0.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color=DARK_BROWN,
			fill_color=DARK_BROWN,
			fill_opacity=1
		)

		burger = VGroup(bun, lettuce, tomato, meat, bun.copy()).arrange(DOWN, buff=0).scale(0.5).move_to(UP*2.5+LEFT*4)

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


	def make_secret_sauce(self):
		circle = Circle(
			radius=3,
			color=GOLD_A,
			fill_opacity=0.85
		)

		paper = RoundedRectangle(
			width=2.85, height=4,
			color=LOGO_WHITE,
			fill_opacity=0.85
		)

		title = Text(
			"Secret Sauce",
			color=BLACK,
			font_size=22
		).shift(UP*1.1)

		writing = RoundedRectangle(
			width=3.5, height=0.15,
			corner_radius=[0.05, 0.05, 0.05, 0.05],
			stroke_color=BLACK,
			fill_color=BLACK,
			fill_opacity=1
		)
		lines = VGroup(writing, writing.copy(), writing.copy(), writing.copy(), writing.copy(), writing.copy()).arrange(DOWN, buff=0.5).scale(0.5).shift(DOWN*0.5)

		secret_sauce = VGroup(circle, paper, title, lines)
		return secret_sauce


	def make_competitor(self, colour, position):
		guy = make_hooman(colour, fill_opacity=1)
		guy.move_to(position).scale(0.6)
		return guy


	def construct(self):
		Text.set_default(font="Monospace")

		wall = self.make_wall()
		self.add(wall)

		poster = self.make_poster()
		self.add(poster)

		counter = self.make_counter()
		self.add(counter)

		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5+DOWN*0.37)
		self.play(Create(you[0]), Write(you[1]))

		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5+DOWN*0.37)
		self.play(Create(grandpa[0]), Write(grandpa[1]))

		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*3+DOWN*0.37)
		self.play(Create(uncle[0]), Write(uncle[1]))

		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*1+DOWN*0.37)
		self.play(Create(dad[0]), Write(dad[1]))

		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*1+DOWN*0.37)
		self.play(Create(mum[0]), Write(mum[1]))

		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*3+DOWN*0.37)
		self.play(Create(brother[0]), Write(brother[1]))

		fam_bam = [grandpa, uncle, dad, mum, brother, you]

		self.wait(2)


		secret_sauce = self.make_secret_sauce()
		self.play(Create(secret_sauce[0]))
		self.play(Create(secret_sauce[1]))
		self.play(Write(secret_sauce[2]), Create(secret_sauce[3]))
		self.wait(2)


		competitor_1 = self.make_competitor(MAROON_D, LEFT*3)
		competitor_2 = self.make_competitor(RED_D, RIGHT*3)

		self.play(Create(competitor_1), 
			Create(competitor_2))

		arc_2 = Arc(radius=3, start_angle=0, angle=PI)
		arc_1 = Arc(radius=3, start_angle=PI, angle=PI)

		self.play(MoveAlongPath(competitor_1, arc_1), 
			MoveAlongPath(competitor_2, arc_2),
			run_time=10,
			rate_func=linear)

		self.play(competitor_1.animate.shift(RIGHT*10), 
			secret_sauce[1].animate.shift(RIGHT*10), 
			secret_sauce[2].animate.shift(RIGHT*10),
			secret_sauce[3].animate.shift(RIGHT*10))

		self.play(FadeOut(secret_sauce[0]),
			competitor_2.animate.shift(LEFT*8))

		self.wait(2)		

		self.play(FadeOut(counter))
		self.play(poster.animate.shift(UP*8), FadeOut(wall))

		self.wait(2)


		go_to_assigned_seat = []
		i = 0
		while i < 6:
			up = 2.5*math.sin(i*2*PI/6)
			right = 2.5*math.cos(i*2*PI/6)

			go_to_assigned_seat.append(fam_bam[i].animate.move_to(UP*up+RIGHT*right+DOWN*0.5))
			i += 1

		self.play(*go_to_assigned_seat)

		text = Text("How can we protect the recipe from falling into the wrong hands?",
			font_size=20).shift(UP*3)

		move_around_table = [Write(text)]
		i = 0
		while i < 6:
			arc = Arc(radius=2.5, start_angle=i*2*PI/6, angle=PI/2).shift(DOWN*0.5)
			move_around_table.append(MoveAlongPath(fam_bam[i], arc))
			i += 1

		self.play(*move_around_table, 
			run_time=5,
			rate_func=linear)

		self.wait(2)



