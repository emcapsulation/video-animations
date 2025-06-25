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



def make_secret_sauce(include_background=True):
	secret_sauce = VGroup()

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

	if include_background:
		secret_sauce.add(circle)

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

	secret_sauce.add(paper, title, lines)
	return secret_sauce


def make_burger():
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

	burger = VGroup(bun, lettuce, tomato, meat, bun.copy()).arrange(DOWN, buff=0)
	return burger



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

		burger = make_burger()
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


		secret_sauce = make_secret_sauce()
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



config.background_color = "#090f1a"

def make_speech_bubble(colour, position, width, height):
	speech_bubble = RoundedRectangle(
		width=width, height=height, 
		fill_color=colour, stroke_color=colour,
		corner_radius=0.2, fill_opacity=0.1).move_to(position)

	return speech_bubble


def make_key(position, scale):
	annulus = Annulus(inner_radius=0.5, outer_radius=1, color=YELLOW)

	stick = RoundedRectangle(
		width=2.5, height=0.5,
		corner_radius=[0.05, 0.05, 0.05, 0.05],
		stroke_color=YELLOW,
		fill_color=YELLOW,
		fill_opacity=1
	)

	little_stick = RoundedRectangle(
		width=0.25, height=1,
		corner_radius=[0.05, 0.05, 0.05, 0.05],
		stroke_color=YELLOW,
		fill_color=YELLOW,
		fill_opacity=1
	)

	little_sticks = VGroup(little_stick, little_stick.copy()).arrange(RIGHT)

	key = VGroup(
		annulus,
		stick.move_to(annulus.get_center() + RIGHT*1.8),
		little_sticks.move_to(stick.get_right() + LEFT*0.5+DOWN*0.4)
	).scale(scale).move_to(position)

	return key


def make_secret_sauce_text():
	secret_sauce = VGroup()

	paper = RoundedRectangle(
		width=3, height=4,
		corner_radius=0.2,
		color=LOGO_WHITE,
		fill_opacity=0.85
	)

	title = Text(
		"Secret Sauce",
		color=BLACK,
		font_size=22
	).shift(UP*1.1)

	text_1 = Text("2 tbsp mayonnaise", font_size=16, color=BLACK)
	text_2 = Text("2 tbsp ketchup", font_size=16, color=BLACK)
	text_3 = Text("1 tbsp mustard", font_size=16, color=BLACK)
	text_4 = Text("1 tsp paprika", font_size=16, color=BLACK)
	text_5 = Text("1 clove garlic", font_size=16, color=BLACK)
	lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

	secret_sauce.add(paper, title, lines)
	return secret_sauce


def make_secret_sauce_encrypted():
	secret_sauce = VGroup()

	paper = RoundedRectangle(
		width=3, height=4,
		corner_radius=0.2,
		color=LOGO_WHITE,
		fill_opacity=0.85
	)

	title = Text(
		"qL7#xP$v@Kf2!W",
		color=BLACK,
		font_size=22
	).shift(UP*1.1)

	text_1 = Text("f9@Lz#Wq8v!2Xp$N", font_size=16, color=BLACK)
	text_2 = Text("B#v5$eYp!tn8Wz@J", font_size=16, color=BLACK)
	text_3 = Text("xM7&rA^Fz3@b!gPL", font_size=16, color=BLACK)
	text_4 = Text("Z!uT@p#qE9*WsLd^", font_size=16, color=BLACK)
	text_5 = Text("r%NyB!q2$GKz*vM@", font_size=16, color=BLACK)
	lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

	secret_sauce.add(paper, title, lines)
	return secret_sauce


class BroYapping(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bro = make_hooman_with_label(BLUE, "Brother", 0.4, LEFT*5+UP*2.5)
		self.play(Create(bro))

		speech_bubble = make_speech_bubble([TEAL, BLUE], RIGHT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("We should encrypt the recipe.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))

		secret_sauce = make_secret_sauce_text()
		secret_sauce.move_to(LEFT*4 + DOWN*0.5).scale(0.6)
		self.play(Create(secret_sauce))

		key = make_key(LEFT*4 + DOWN*3, 0.25)
		self.play(Create(key))

		encrypt = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		encrypt_text = Text("Encryption Scheme", font_size=24).move_to(encrypt.get_center())

		encrypto = VGroup(encrypt, encrypt_text).shift(DOWN + RIGHT*0.5)
		self.play(Create(encrypto))

		self.play(
			secret_sauce.animate.move_to(encrypto.get_left()),
			key.animate.move_to(encrypto.get_left())
		)

		garbled = make_secret_sauce_encrypted()
		garbled.move_to(encrypto.get_right()).scale(0.6)

		self.play(
			FadeOut(secret_sauce),
			FadeOut(key),
			garbled.animate.move_to(RIGHT*5 + DOWN)
		)

		self.wait(2)

		self.play(
			FadeOut(encrypto),
			garbled.animate.move_to(ORIGIN+DOWN).scale(1.5)
		)

		comp_1 = make_hooman(MAROON_D).move_to(RIGHT*4).scale(0.6)
		comp_2 = make_hooman(RED_D).move_to(LEFT*4 + DOWN*2).scale(0.6)

		self.play(Create(comp_1), Create(comp_2))

		q_mark_1 = Text("?", color=MAROON_D).move_to(comp_1.get_center())
		q_mark_2 = Text("?", color=RED_D).move_to(comp_2.get_center())

		self.play(Transform(comp_1, q_mark_1), Transform(comp_2, q_mark_2))

		self.wait(2)


config.background_color = "#0d0904"

class UncYapLord(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		garbled = make_secret_sauce_encrypted()
		garbled.move_to(ORIGIN + DOWN).scale(0.6*1.5)
		self.add(garbled)

		unc = make_hooman_with_label(GOLD, "Uncle", 0.4, RIGHT*5+UP*2.5)
		self.play(Create(unc))

		speech_bubble = make_speech_bubble([YELLOW, GOLD], LEFT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Then how are WE supposed to read it?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))

		self.wait(2)

		burger = make_burger().move_to(RIGHT*3 + DOWN)
		q_mark = Text("?", color=GOLD).move_to(burger.get_center())

		self.play(garbled.animate.shift(LEFT*3), Create(burger))
		self.play(Transform(burger, q_mark))
		self.wait(2)

		self.play(FadeOut(unc), FadeOut(speech_bubble), FadeOut(q_mark), FadeOut(speech1), FadeOut(burger), 
			garbled.animate.move_to(ORIGIN).scale(0.6))



config.background_color = "#000000"

class EachKeepACopy(Scene):
	def garblegarble(self, key_group, i, garbled):
		self.play(
			key_group[i].animate.move_to(garbled.get_center())
		)

		self.play(
			key_group[i].animate.move_to(UP*2.15*math.sin(i*2*PI/6)+RIGHT*2.15*math.cos(i*2*PI/6)),
			Transform(garbled, make_secret_sauce_text().scale(0.6*1.5*0.6))
		)

		self.wait(2)

		self.play(
			key_group[i].animate.move_to(garbled.get_center())
		)

		self.play(
			key_group[i].animate.move_to(UP*2.15*math.sin(i*2*PI/6)+RIGHT*2.15*math.cos(i*2*PI/6)),
			Transform(garbled, make_secret_sauce_encrypted().scale(0.6*1.5*0.6))
		)

		self.wait(2)


	def construct(self):
		Text.set_default(font="Monospace")

		garbled = make_secret_sauce_encrypted()
		garbled.move_to(ORIGIN).scale(0.6*1.5*0.6)
		self.add(garbled)

		you = make_hooman_with_label(PURPLE, "You", 0.3, RIGHT*5+DOWN*0.37)
		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.3, LEFT*5+DOWN*0.37)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.3, LEFT*3+DOWN*0.37)
		dad = make_hooman_with_label(GREEN, "Dad", 0.3, LEFT*1+DOWN*0.37)
		mum = make_hooman_with_label(TEAL, "Mum", 0.3, RIGHT*1+DOWN*0.37)
		brother = make_hooman_with_label(BLUE, "Brother", 0.3, RIGHT*3+DOWN*0.37)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)


		i = 0
		while i < 6:
			up = 3*math.sin(i*2*PI/6)
			right = 3*math.cos(i*2*PI/6)

			fam_bam[i].move_to(UP*up+RIGHT*right)
			i += 1

		self.play(Create(fam_bam))
		self.wait(2)


		key_group = VGroup()
		i = 0
		while i < 6:
			up = 2.15*math.sin(i*2*PI/6)
			right = 2.15*math.cos(i*2*PI/6)

			key = make_key(UP*up+RIGHT*right, 0.15)
			self.play(Create(key))
			key_group.add(key)

			i += 1

		self.wait(2)

		self.garblegarble(key_group, 1, garbled)
		self.garblegarble(key_group, 3, garbled)


		def spinny_boi(mob, alpha):
			mob.restore()
			mob.become(mob.move_to(interpolate(mob.get_center(), LEFT*5 + UP*5, alpha)).rotate(interpolate(0, 2*PI, alpha)))

		key_group[2].save_state()
		self.play(UpdateFromAlphaFunc(key_group[2], spinny_boi))

		self.play(
			key_group[5].animate.shift(DOWN + RIGHT*2)
		)

		competitor = make_hooman(MAROON_D).move_to(RIGHT*8).scale(0.3)
		self.play(
			competitor.animate.move_to(key_group[5].get_center() + RIGHT)
		)
		self.play(
			competitor.animate.shift(RIGHT*8),
			key_group[5].animate.shift(RIGHT*8)
		)

		self.wait(2)


		self.play(
			key_group[4].animate.shift(LEFT*8 + DOWN),
			fam_bam[4].animate.shift(LEFT*8 + DOWN)
		)

		self.wait(4)