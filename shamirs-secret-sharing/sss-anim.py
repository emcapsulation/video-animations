from manim import *
import random
import math


def make_hooman(colour, fill_opacity=0.8):
	head = Circle(color=colour, fill_opacity=fill_opacity, radius=1)
	body = Arc(color=colour, fill_opacity=fill_opacity, radius=1.5, angle=PI)
	hooman = VGroup(head, body).arrange(DOWN)

	return hooman



def make_hooman_with_label(colour, label, scale, position, label_colour=WHITE):
	hooman = make_hooman(colour)
	label = Text(label, font_size=30, color=label_colour).next_to(hooman, UP)
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


def make_key(position, scale, colour=YELLOW):
	annulus = Annulus(inner_radius=0.5, outer_radius=1, color=colour)

	stick = RoundedRectangle(
		width=2.5, height=0.5,
		corner_radius=[0.05, 0.05, 0.05, 0.05],
		stroke_color=colour,
		fill_color=colour,
		fill_opacity=1
	)

	little_stick = RoundedRectangle(
		width=0.25, height=1,
		corner_radius=[0.05, 0.05, 0.05, 0.05],
		stroke_color=colour,
		fill_color=colour,
		fill_opacity=1
	)

	little_sticks = VGroup(little_stick, little_stick.copy()).arrange(RIGHT)

	key = VGroup(
		annulus,
		stick.move_to(annulus.get_center() + RIGHT*1.8),
		little_sticks.move_to(stick.get_right() + LEFT*0.5+DOWN*0.4)
	).scale(scale).move_to(position)

	return key


def make_secret_sauce_text(include_background=False):
	secret_sauce = VGroup()

	circle = Circle(
		radius=3,
		color=GOLD_A,
		fill_opacity=0.85
	)

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

	if include_background:
		secret_sauce.add(circle)
	secret_sauce.add(paper, title, lines)
	return secret_sauce


def make_secret_sauce_encrypted(include_background=False):
	secret_sauce = VGroup()

	circle = Circle(
		radius=3,
		color=GOLD_A,
		fill_opacity=0.85
	)

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

	if include_background:
		secret_sauce.add(circle)
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



config.background_color = "#0a120c"

class DadPopsOff(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*5+UP*2.5)
		self.play(Create(dad))

		speech_bubble = make_speech_bubble([TEAL, GREEN], RIGHT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("What if we split the key into six pieces?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))

		key_text = Text("super_secret_key_1")
		self.play(Write(key_text))


		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		key_text_copy = key_text.copy()
		for i in range(0, len(key_text_copy.get_text()), 3):
			key_text_copy[i:i+3].set_color(colours[i//3])


		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5)
		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*3)
		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*1)
		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*1)
		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*3)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you).move_to(DOWN*3).scale(0.8)

		self.play(
			Transform(key_text, key_text_copy),
			Create(fam_bam)
		)


		part_of_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			part_of_key_anim.append(
				key_text[i:i+3].animate.move_to(fam_bam[i//3].get_center()+UP*1.2).scale(0.5)
			)

		self.play(*part_of_key_anim)
		self.wait(2)


		competitor = make_hooman(MAROON_D).scale(0.2).move_to(LEFT*4)
		encrypto = make_secret_sauce_encrypted().scale(0.7)
		self.play(
			Create(encrypto),
			Create(competitor)
		)

		self.play(key_text[0:0+3].animate.move_to(competitor.get_right()))

		comp_and_key = VGroup(competitor, key_text[0:0+3])
		self.play(
			comp_and_key.animate.move_to(encrypto.get_left())
		)

		self.play(Wiggle(encrypto), comp_and_key.animate.move_to(LEFT*4))
		self.wait(2)

		self.play(competitor.animate.shift(LEFT*8))


		combine_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			combine_key_anim.append(
				key_text[i:i+3].animate.move_to(LEFT*5).shift(RIGHT*i/5)
			)

		self.play(*combine_key_anim)
		self.wait(2)


		unencrypto = make_secret_sauce_text().scale(0.7)
		self.play(
			key_text.animate.move_to(encrypto.get_center())
		)
		self.play(key_text.animate.move_to(LEFT*4),
			Transform(encrypto, unencrypto)
		)
		self.wait(2)


		part_of_key_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			part_of_key_anim.append(
				key_text[i:i+3].animate.move_to(fam_bam[i//3].get_center()+UP*1.2)
			)

		self.play(*part_of_key_anim)
		self.wait(2)



config.background_color = "#000000"

class MumCranky(Scene):
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


	def construct(self):
		Text.set_default(font="Monospace")

		wall = self.make_wall()
		self.add(wall)

		poster = self.make_poster()
		self.add(poster)

		counter = self.make_counter()
		self.add(counter)


		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5+DOWN*0.37)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*3+DOWN*0.37)
		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*1+DOWN*0.37)
		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*1+DOWN*0.37)
		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*3+DOWN*0.37)
		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5+DOWN*0.37)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)


		key_text = Text("super_secret_key_1").scale(0.5)
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(key_text.get_text()), 3):
			key_text[i:i+3].set_color(colours[i//3])
			key_text[i:i+3].move_to(fam_bam[i//3].get_center()+DOWN*1.1)


		self.play(Create(mum[0]), Write(mum[1]), Write(key_text[9:9+3]))
		self.wait(2)


		for i in range(0, len(fam_bam)):
			if i != 3:
				self.play(Create(fam_bam[i][0]), Write(fam_bam[i][1]), Write(key_text[i*3:(i*3)+3]), run_time=0.5)


		combine_parts_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			combine_parts_anim.append(key_text[i:i+3].animate.move_to(UP + LEFT*1.2 + RIGHT*i/5))

		self.play(*combine_parts_anim)
		key = make_key(UP, 0.3)
		self.play(Transform(key_text, key))
		self.wait(2)



class MumCrankyP2(Scene):
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


	def construct(self):
		Text.set_default(font="Monospace")

		wall = self.make_wall()
		self.add(wall)

		poster = self.make_poster()
		self.add(poster)

		counter = self.make_counter()
		self.add(counter)


		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5+DOWN*0.37)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*3+DOWN*0.37)
		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*1+DOWN*0.37)
		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*1+DOWN*0.37)
		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*3+DOWN*0.37)
		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5+DOWN*0.37)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)


		key_text = Text("super_secret_key_1").scale(0.5)
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(key_text.get_text()), 3):
			key_text[i:i+3].set_color(colours[i//3])
			key_text[i:i+3].move_to(fam_bam[i//3].get_center()+DOWN*1.1)


		self.add(fam_bam, key_text)


		def spinny_boi(mob, alpha):
			mob.become(mob.move_to(interpolate(mob.get_center(), LEFT*5 + UP*5, alpha)).rotate(interpolate(0, 2*PI, alpha)))

		self.wait(2)
		self.play(UpdateFromAlphaFunc(key_text[0:0+3], spinny_boi))
		self.play(dad.animate.shift(DOWN*5), key_text[2*3:(2*3)+3].animate.shift(DOWN*5))
		self.play(FadeOut(brother), FadeOut(key_text[4*3:(4*3)+3]))
		self.wait(2)


		self.play(FadeOut(wall), FadeOut(poster), FadeOut(counter))



class AnyFour(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5+DOWN*0.37)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*3+DOWN*0.37)
		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*1+DOWN*0.37)
		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*1+DOWN*0.37)
		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*3+DOWN*0.37)
		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5+DOWN*0.37)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)


		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		dots = VGroup()
		for i in range(0, len(fam_bam)):
			dot_boi = Dot(color=colours[i], radius=0.2).move_to(fam_bam[i].get_center()+DOWN*1.1)
			dots.add(dot_boi)

		self.add(fam_bam, dots)

		combine_parts_anim = []
		grey_out_anim = []
		random_members = random.sample([0, 1, 2, 3, 4, 5], 4)

		random_dots = VGroup()
		for i in range(0, len(fam_bam)):
			if i in random_members:
				random_dots.add(dots[i])
				combine_parts_anim.append(dots[i].animate.move_to(UP))
			else:
				grey_out_anim.append(fam_bam[i].animate.set_color(GRAY_A))
				grey_out_anim.append(dots[i].animate.set_color(GRAY_A))

		self.play(*grey_out_anim)
		self.play(*combine_parts_anim)

		key = make_key(UP, 0.3)
		self.play(ReplacementTransform(random_dots, key))
		self.play(FadeOut(key))



config.background_color = "#faf5e8"

class Recap(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		unencrypto = make_secret_sauce_text(include_background=True).shift(RIGHT*2)
		encrypto = make_secret_sauce_encrypted(include_background=True).shift(RIGHT*2)
		key = make_key(LEFT*2, 0.6, colour=LIGHT_BROWN)

		self.play(Create(unencrypto))

		self.play(Create(key))
		self.play(key.animate.move_to(unencrypto.get_center()))
		self.play(key.animate.move_to(LEFT*2), Transform(unencrypto, encrypto))
		self.wait(2)

		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, LEFT*5+UP*3, label_colour=BLACK)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.4, LEFT*5, label_colour=BLACK)
		dad = make_hooman_with_label(GREEN, "Dad", 0.4, LEFT*5+DOWN*3, label_colour=BLACK)
		mum = make_hooman_with_label(TEAL, "Mum", 0.4, RIGHT*5+UP*3, label_colour=BLACK)
		brother = make_hooman_with_label(BLUE, "Brother", 0.4, RIGHT*5, label_colour=BLACK)
		you = make_hooman_with_label(PURPLE, "You", 0.4, RIGHT*5+DOWN*3, label_colour=BLACK)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)
		self.play(Create(fam_bam))


		baby_key = make_key(LEFT*2, 0.2, colour=LIGHT_BROWN).move_to(key.get_center())
		lil_keys = VGroup(baby_key, baby_key.copy(), baby_key.copy(), baby_key.copy(), baby_key.copy(), baby_key.copy())

		key_go_anim = []
		for i in range(len(lil_keys)):
			key_go_anim.append(lil_keys[i].animate.move_to(fam_bam[i].get_center()))
		self.play(*key_go_anim)
		self.wait(2)


		competitor = make_hooman(MAROON_D).move_to(RIGHT*8 + UP*2).scale(0.3)
		self.play(competitor.animate.move_to(brother.get_right()))
		self.play(competitor.animate.shift(RIGHT*3 + UP*2), lil_keys[4].animate.shift(RIGHT*3 + UP*2))
		self.wait(2)

		red_x = Text("X", color=RED, font_size=72)
		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))
		self.play(FadeOut(lil_keys))


		fragments = VGroup()
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(fam_bam)):
			fragments.add(Dot(radius=0.2, color=colours[i]).move_to(LEFT*3+RIGHT*i/3))
		self.play(Transform(key, fragments))


		fragments_copy = fragments.copy()
		left_or_right = [LEFT, RIGHT]
		for i in range(0, len(fam_bam)):
			self.play(fragments_copy[i].animate.move_to(fam_bam[i].get_center() + left_or_right[i//3 == 0]))
		self.wait(2)


		self.play(fragments_copy[3].animate.shift(UP*2 + RIGHT*3))

		make_key_again = []
		for i in range(0, len(fragments_copy)):
			if i != 3:
				make_key_again.append(fragments_copy[i].animate.move_to(DOWN+LEFT*3+RIGHT*i/3))
		self.play(*make_key_again)
		self.wait(2)

		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))



class Recap2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title_text = Text("Problem Recap", color=BLACK).shift(UP*3)
		self.play(Write(title_text))

		text = Text("""
Each family member gets some\n
kind of part or piece of the key.\n
But not the whole key - the piece\n
should be useless on its own.\n\n
The original key should be\n
recoverable if ANY four family\n
members bring their parts together.\n\n
But, no subset of family members\n
smaller than size four should be\n
able to reconstruct the key, or\n
even learn anything about it.
""", 
			font_size=18, color=BLACK).move_to(DOWN*0.6+LEFT*4)
		self.play(Write(text), run_time=20)
		self.wait(2)


		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.2, UP*2, label_colour=BLACK)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.2, RIGHT*2.5+UP*2, label_colour=BLACK)
		dad = make_hooman_with_label(GREEN, "Dad", 0.2, RIGHT*5+UP*2, label_colour=BLACK)
		mum = make_hooman_with_label(TEAL, "Mum", 0.2, DOWN*3, label_colour=BLACK)
		brother = make_hooman_with_label(BLUE, "Brother", 0.2, RIGHT*2.5+DOWN*3, label_colour=BLACK)
		you = make_hooman_with_label(PURPLE, "You", 0.2, RIGHT*5+DOWN*3, label_colour=BLACK)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)
		key = make_key(RIGHT*2.5, 0.5, colour=LIGHT_BROWN)

		self.play(Create(fam_bam), Create(key))
		self.wait(2)


		fragments = VGroup()
		colours = [ORANGE, GOLD, GREEN, TEAL]
		for i in range(0, len(colours)):
			fragments.add(Dot(radius=0.2, color=colours[i]).move_to(RIGHT*2+RIGHT*i/3))
		self.play(ReplacementTransform(key, fragments))
		fragments.add(fragments[0].copy(), fragments[1].copy())
		self.wait(2)


		fragments_copy = fragments.copy()
		up_or_down = [UP, DOWN]
		for i in range(0, len(fragments_copy)):
			self.play(fragments_copy[i].animate.move_to(fam_bam[i].get_center() + up_or_down[i//3 == 0]))
		self.wait(2)


		self.play(Flash(fragments_copy[0], color=ORANGE), Flash(fragments_copy[4], color=ORANGE))
		self.play(Flash(fragments_copy[1], color=GOLD), Flash(fragments_copy[5], color=GOLD))
		self.wait(2)


		self.play(fragments_copy[0].animate.move_to(DOWN+RIGHT*2+RIGHT*0/3))
		self.play(fragments_copy[1].animate.move_to(DOWN+RIGHT*2+RIGHT*1/3))
		self.play(fragments_copy[3].animate.move_to(DOWN+RIGHT*2+RIGHT*3/3))
		self.play(fragments_copy[5].animate.move_to(DOWN+RIGHT*2+RIGHT*1/3))
		self.wait(2)


		red_x = Text("X", color=RED, font_size=72)
		self.play(SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))
		self.wait(2)


		key = make_key(RIGHT*2.5 + DOWN*0.5, 0.5, colour=LIGHT_BROWN)
		self.play(FadeIn(key), FadeOut(fragments), FadeOut(fragments_copy))
		self.wait(5)


config.background_color = "#140b13"

class Shamir(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		shamir = make_hooman_with_label(LIGHT_PINK, "Shamir", 0.4, LEFT*5+UP*2.5)
		self.play(Create(shamir))

		speech_bubble = make_speech_bubble([PINK, LIGHT_PINK], RIGHT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("This is Shamir's Secret Sharing.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)

		text_1 = Text("Splits any secret into n parts called shares.", font_size=20).move_to(UP)
		self.play(Write(text_1))
		self.wait(2)

		text_2 = Text("You select a threshold, k.", font_size=20).move_to(UP*0.5)
		self.play(Write(text_2))
		self.wait(2)


		top_rect = make_speech_bubble(GREEN, DOWN, 10, 1.5)
		top_text = Text("≥ k shares reconstructs the secret.", font_size=20).move_to(top_rect.get_center())
		top = VGroup(top_rect, top_text)
		self.play(Create(top_rect), Write(top_text))
		self.wait(2)

		bot_rect = make_speech_bubble(RED, DOWN*3, 10, 1.5)
		bot_text = Text("< k shares are completely useless.", font_size=20).move_to(bot_rect.get_center())
		bot = VGroup(bot_rect, bot_text)
		self.play(Create(bot_rect), Write(bot_text))
		self.wait(2)


		self.play(
			top_rect.animate.set_width(7),
			bot_rect.animate.set_width(7)
		)

		self.play(
			top.animate.shift(LEFT*3),
			bot.animate.shift(LEFT*3)
		)

		self.wait(2)

		
		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.2, RIGHT*2+DOWN)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.2, RIGHT*4+DOWN)
		dad = make_hooman_with_label(GREEN, "Dad", 0.2, RIGHT*6+DOWN)
		mum = make_hooman_with_label(TEAL, "Mum", 0.2, RIGHT*2+DOWN*2)
		brother = make_hooman_with_label(BLUE, "Brother", 0.2, RIGHT*4+DOWN*2)
		you = make_hooman_with_label(PURPLE, "You", 0.2, RIGHT*6+DOWN*2)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)
		self.play(Create(fam_bam))

		n_is_6 = Text("n = 6", font_size=28).move_to(RIGHT*3 + DOWN*3)
		self.play(Write(n_is_6))
		self.wait(2)


		self.play(
			uncle.animate.set_color(GRAY),
			mum.animate.set_color(GRAY)
		)
		self.play(
			uncle.animate.set_color(GOLD),
			mum.animate.set_color(TEAL)
		)
		self.play(
			grandpa.animate.set_color(GRAY),
			you.animate.set_color(GRAY)
		)
		self.play(
			grandpa.animate.set_color(ORANGE),
			you.animate.set_color(PURPLE)
		)
		self.play(
			dad.animate.set_color(GRAY),
			mum.animate.set_color(GRAY)
		)


		k_is_4 = Text("k = 4", font_size=28).move_to(RIGHT*5 + DOWN*3)
		self.play(Write(k_is_4))
		self.wait(2)



config.background_color = "#000000"

class StraightLine(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-4, 8, 1],
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(DOWN*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		point = Dot(axes.coords_to_point(1, 2), color=RED)
		point_label = MathTex("(1, 2)", font_size=24).next_to(point, RIGHT, buff=0.2)

		self.play(Create(axes), Write(labels))
		self.wait(2)
		self.play(Create(point), Write(point_label))		
		self.wait(2)

		question = Text("How many straight lines can we draw through (1, 2)?", font_size=24, t2c={"(1, 2)": RED}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point, color=RED))
		self.wait(2)


		# y = ax + 2 - a
		a_start, a_end = -15, 15

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 15)/a_range * (gradient_steps-1))]


		y_x_1 = axes.plot(lambda x: x + 1, x_range=[-1, 7], color=get_line_colour(1))
		y_x_1_label = MathTex("y = x + 1", font_size=24, color=get_line_colour(1)).next_to(axes.coords_to_point(3, 4), RIGHT)
		self.play(Create(y_x_1), Write(y_x_1_label))
		self.bring_to_front(point, point_label)		
		self.wait(2)

		y_3x_m1 = axes.plot(lambda x: 3*x - 1, x_range=[-1, 3], color=get_line_colour(3))
		y_3x_m1_label = MathTex("y = 3x - 1", font_size=24, color=get_line_colour(3)).next_to(axes.coords_to_point(2, 5), RIGHT)
		self.play(Create(y_3x_m1), Write(y_3x_m1_label))
		self.bring_to_front(point, point_label)
		self.wait(2)

		y_m2x_4 = axes.plot(lambda x: -2*x + 4, x_range=[-1, 4], color=get_line_colour(-2))
		y_m2x_4_label = MathTex("y = -2x + 4", font_size=24, color=get_line_colour(-2)).next_to(axes.coords_to_point(3, -2), RIGHT)
		self.play(Create(y_m2x_4), Write(y_m2x_4_label))
		self.bring_to_front(point, point_label)
		self.wait(2)

		self.play(FadeOut(y_x_1), FadeOut(y_x_1_label),
			FadeOut(y_3x_m1), FadeOut(y_3x_m1_label),
			FadeOut(y_m2x_4), FadeOut(y_m2x_4_label)
		)
		self.wait(2)


		question_2 = MathTex("\\infty").move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)


		# This is a new thing for me - this tracks the value of a				
		a_tracker = ValueTracker(a_start)

		def get_line():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			x1 = -4
			if a != 0:
				x1 = (-4+a-2)/a

			x2 = 10
			if a != 0:
				x2 = (8+a-2)/a

			return axes.plot(
				lambda x: a * x + 2 - a,
				x_range=[max(-1, min(x1, x2)), min(10, max(x1, x2))],
				color=colour,
				stroke_width=4
			)

		# Each frame it redraws the line
		line = always_redraw(get_line)
		self.add(line)
		self.bring_to_front(point, point_label)


		def get_equation():
			a = a_tracker.get_value()
			a_str = f"{a:.2f}"
			eq = MathTex(
			    "y = ", f"{a_str}", "x + ", f"{(2 - a):.2f}",
			    color=get_line_colour(a),
			    font_size=24
			)
			eq.move_to(UP*2 + RIGHT*4)
			return eq

		equation = always_redraw(get_equation)
		self.add(equation)


		self.play(a_tracker.animate.set_value(a_end), run_time=6, rate_func=linear)
		self.wait(2)		



config.background_color = "#15131c"

class SinglePointAlgebra(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax + b").move_to(UP*2)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the line to pass through (1, 2)", font_size=28, t2c={"(1, 2)": RED}).next_to(general, DOWN)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "+", "b")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN)
		self.play(Write(sub_eq))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "=", "2").next_to(sub_eq, DOWN)
		self.play(TransformMatchingTex(sub_eq.copy(), simplified))
		self.wait(2)

		underline = Underline(simplified, color=MAROON)
		explain = Text("1 equation, 2 unknowns", font_size=20, color=MAROON).next_to(simplified, RIGHT*1.5)
		self.play(Create(underline), FadeIn(explain))
		self.wait(2)

		conclusion = Text("Infinitely many (a, b) pairs satisfy this.", font_size=28).next_to(simplified, DOWN, buff=0.5).shift(DOWN)
		self.play(Write(conclusion))
		self.wait(2)

		not_unique = Text("One point alone is not enough to define a line.", font_size=30, weight=BOLD).next_to(conclusion, DOWN, buff=0.5)
		self.play(FadeIn(not_unique))

		conc = VGroup(conclusion, not_unique)
		self.play(Circumscribe(conc, color=MAROON))
		self.wait(2)



config.background_color = "#000000"

class LineIsSoBack(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-4, 8, 1],
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(DOWN*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		point = Dot(axes.coords_to_point(1, 2), color=RED)
		point_label = MathTex("(1, 2)", font_size=24).next_to(point, RIGHT, buff=0.2)

		self.add(axes, labels, point, point_label)

		point_2 = Dot(axes.coords_to_point(2, 6), color=ORANGE)
		point_label_2 = MathTex("(2, 6)", font_size=24).next_to(point_2, RIGHT, buff=0.2)
		self.play(Create(point_2), Write(point_label_2))		
		self.wait(2)

		question = Text("How many straight lines can we draw through (1, 2) and (2, 6)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point, color=RED))
		self.play(Flash(point_2, color=ORANGE))
		self.wait(2)


		# y = ax + 2 - a
		a_start, a_end = -15, 15

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 15)/a_range * (gradient_steps-1))]


		question_2 = Text("Only 1", font_size=24).move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)


		y_4x_m2 = axes.plot(lambda x: 4*x - 2, x_range=[-1, 2.5], color=get_line_colour(4))
		y_4x_m2_label = MathTex("y = 4x - 2", font_size=24, color=get_line_colour(4)).next_to(axes.coords_to_point(1.5, 4), RIGHT)
		self.play(Create(y_4x_m2), Write(y_4x_m2_label))
		self.bring_to_front(point, point_label)		
		self.wait(2)



config.background_color = "#15131c"

class AlgebraAgain(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax + b").move_to(UP*3.5)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the line to pass through (1, 2) and (2, 6)", font_size=24, 
			t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).next_to(general, DOWN)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "+", "b", "\\quad", "(1)")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN).shift(LEFT*3)
		self.play(Write(sub_eq))
		self.wait(2)

		sub_eq_2 = MathTex("6", "=", "a", "\\cdot", "2", "+", "b", "\\quad", "(2)")
		sub_eq_2.set_color_by_tex("2", ORANGE)
		sub_eq_2.set_color_by_tex("6", ORANGE)
		sub_eq_2.next_to(point_text, DOWN).shift(RIGHT*3)
		self.play(Write(sub_eq_2))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "=", "2", "\\quad", "(1)").next_to(sub_eq, DOWN)
		simplified_2 = MathTex("2a", "+", "b", "=", "6", "\\quad", "(2)").next_to(sub_eq_2, DOWN)
		self.play(
			TransformMatchingTex(sub_eq.copy(), simplified),
			TransformMatchingTex(sub_eq_2.copy(), simplified_2)
		)
		self.wait(2)

		solve = Text("Subtract (2) - (1)", font_size=24, 
			t2c={"(1)": RED, "(2)": ORANGE})
		self.play(Write(solve))
		self.wait(2)

		big_boi = MathTex("2a", "-", "a", "+", "b", "-", "b", "=", "6", "-", "2").next_to(solve, DOWN)
		self.play(Write(big_boi))
		self.wait(2)

		big_boi_simp = MathTex("a", "=", "4").next_to(solve, DOWN)
		self.play(Transform(big_boi, big_boi_simp))
		self.wait(2)

		solve_2 = Text("Substitute a = 4 into (1)", font_size=24, 
			t2c={"(1)": RED}).next_to(big_boi_simp, DOWN).shift(DOWN*0.5)
		self.play(Write(solve_2))
		self.wait(2)

		again = MathTex("4", "+", "b", "=", "2").next_to(solve_2, DOWN)
		self.play(Write(again))
		self.wait(2)

		again_simp = MathTex("b", "=", "-2").next_to(solve_2, DOWN)
		self.play(Transform(again, again_simp))
		self.wait(2)

		final_guy = MathTex("y = 4x + -2").next_to(again_simp, DOWN).shift(DOWN*0.5)
		self.play(Write(final_guy))
		self.play(Circumscribe(final_guy, color=MAROON))
		self.wait(2)

		ahhh = Text("A polynomial of degree 1 requires 2 points to uniquely define it.", font_size=20, weight=BOLD, color=BLACK)
		rect = BackgroundRectangle(ahhh, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		self.play(FadeIn(rect), Write(ahhh))
		self.wait(2)



config.background_color = "#000000"

class ParabolaYay(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-4, 8, 1],
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(DOWN*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		point = Dot(axes.coords_to_point(1, 2), color=RED)
		point_label = MathTex("(1, 2)", font_size=24).next_to(point, RIGHT, buff=0.2)

		point_2 = Dot(axes.coords_to_point(2, 6), color=ORANGE)
		point_label_2 = MathTex("(2, 6)", font_size=24).next_to(point_2, RIGHT, buff=0.2)

		self.add(axes, labels, point, point_label, point_2, point_label_2)
		self.wait(2)

		question = Text("How many parabolas can we draw through (1, 2) and (2, 6)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point, color=RED))
		self.play(Flash(point_2, color=ORANGE))
		self.wait(2)


		# y = ((c-2)/2 + 2) x^2 - (3c-2)/2 x + c 
		a_start, a_end = -50, 60

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 50)/a_range * (gradient_steps-1))]


		y_x_1 = axes.plot(lambda x: 1.5*x*x - 0.5*x + 1, x_range=[-1, 2.3], color=get_line_colour(1))
		y_x_1_label = MathTex("y = 1.5x^{2} - 0.5x + 1", font_size=24, color=get_line_colour(1)).next_to(axes.coords_to_point(2.5, 7), RIGHT)
		self.play(Create(y_x_1), Write(y_x_1_label))
		self.bring_to_front(point, point_label, point_2, point_label_2)		
		self.wait(2)

		y_3x_m1 = axes.plot(lambda x: 6*x*x - 14*x + 10, x_range=[0.16, 2.18], color=get_line_colour(10))
		y_3x_m1_label = MathTex("y = 6x^{2} - 14x + 10", font_size=24, color=get_line_colour(10)).next_to(axes.coords_to_point(2, 5), RIGHT)
		self.play(Create(y_3x_m1), Write(y_3x_m1_label))
		self.bring_to_front(point, point_label, point_2, point_label_2)
		self.wait(2)

		y_m2x_4 = axes.plot(lambda x: -2*x*x + 10*x - 6, x_range=[0.2, 4.79], color=get_line_colour(-6))
		y_m2x_4_label = MathTex("y = -2x^{2} + 10x - 6", font_size=24, color=get_line_colour(-6)).next_to(axes.coords_to_point(4, 2), RIGHT)
		self.play(Create(y_m2x_4), Write(y_m2x_4_label))
		self.bring_to_front(point, point_label, point_2, point_label_2)
		self.wait(2)

		self.play(FadeOut(y_x_1), FadeOut(y_x_1_label),
			FadeOut(y_3x_m1), FadeOut(y_3x_m1_label),
			FadeOut(y_m2x_4), FadeOut(y_m2x_4_label)
		)
		self.wait(2)


		question_2 = MathTex("\\infty").move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)


		# This is a new thing for me - this tracks the value of a				
		a_tracker = ValueTracker(a_start)

		def get_line():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			return axes.plot(
				lambda x: ((a-2)/2 + 2)*x*x - ((3*a-2)/2)*x + a,
				x_range=[-1, 10],
				color=colour,
				stroke_width=4
			)

		# Each frame it redraws the line
		line = always_redraw(get_line)
		self.add(line)
		self.bring_to_front(point, point_label, point_2, point_label_2)


		def get_equation():
			a = a_tracker.get_value()

			eq = MathTex(
			    "y = ", f"{((a-2)/2 + 2):.2f}", "x^{2} + ", f"{(-1*(3*a-2)/2):.2f}", "x + ", f"{a:.2f}",
			    color=get_line_colour(a),
			    font_size=24
			)
			eq.move_to(UP*2 + RIGHT*4)
			return eq

		equation = always_redraw(get_equation)
		self.add(equation)


		self.play(a_tracker.animate.set_value(a_end), run_time=6, rate_func=linear)
		self.wait(2)	



config.background_color = "#15131c"

class DoublePointParabolaNoGo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax^{2} + bx + c").move_to(UP*3)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the curve to pass through (1, 2) and (2, 6)", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE}).next_to(general, DOWN, buff=1)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("2", "=", "a", "\\cdot", "1", "^{2}", "+", "b", "\\cdot", "1", "+", "c", "\\quad", "(1)")
		sub_eq.set_color_by_tex("2", RED)
		sub_eq.set_color_by_tex("1", RED)
		sub_eq.next_to(point_text, DOWN).shift(LEFT*3)
		self.play(Write(sub_eq))
		self.wait(2)

		sub_eq_2 = MathTex("6", "=", "a", "\\cdot", "2", "^{2}", "+", "b", "\\cdot", "2", "+", "c", "\\quad", "(2)")
		sub_eq_2.set_color_by_tex("2", ORANGE)
		sub_eq_2.set_color_by_tex("6", ORANGE)
		sub_eq_2.next_to(point_text, DOWN).shift(RIGHT*3)
		self.play(Write(sub_eq_2))
		self.wait(2)

		simplified = MathTex("a", "+", "b", "+", "c", "=", "2", "\\quad", "(1)").next_to(sub_eq, DOWN)
		simplified_2 = MathTex("4a", "+", "2b", "+", "c", "=", "6", "\\quad", "(2)").next_to(sub_eq_2, DOWN)
		self.play(
			TransformMatchingTex(sub_eq.copy(), simplified),
			TransformMatchingTex(sub_eq_2.copy(), simplified_2)
		)
		self.wait(2)

		underline = Underline(simplified, color=MAROON)
		underline_2 = Underline(simplified_2, color=MAROON)

		explain = Text("2 equations, 3 unknowns", font_size=20, color=MAROON).move_to(DOWN*0.5)
		self.play(Create(underline), Create(underline_2), FadeIn(explain))
		self.wait(2)

		conclusion = Text("Infinitely many solutions.", font_size=28).next_to(explain, DOWN, buff=0.5).shift(DOWN)
		self.play(Write(conclusion))
		self.wait(2)



config.background_color = "#000000"

class ParabolaIsSoBack(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-4, 8, 1],
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(DOWN*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		point = Dot(axes.coords_to_point(1, 2), color=RED)
		point_label = MathTex("(1, 2)", font_size=24).next_to(point, RIGHT, buff=0.2)

		point_2 = Dot(axes.coords_to_point(2, 6), color=ORANGE)
		point_label_2 = MathTex("(2, 6)", font_size=24).next_to(point_2, RIGHT, buff=0.2)

		self.add(axes, labels, point, point_label, point_2, point_label_2)
		self.wait(2)

		point_3 = Dot(axes.coords_to_point(3, 4), color=GOLD)
		point_label_3 = MathTex("(3, 4)", font_size=24).next_to(point_3, RIGHT, buff=0.2)
		self.play(Create(point_3), Write(point_label_3))		
		self.wait(2)

		question = Text("How many parabolas can we draw through (1, 2), (2, 6) and (3, 4)?", 
			font_size=24, t2c={"(1, 2)": RED, "(2, 6)": ORANGE, "(3, 4)": GOLD}).move_to(UP*3)
		self.play(Write(question))
		self.play(Flash(point, color=RED))
		self.play(Flash(point_2, color=ORANGE))
		self.play(Flash(point_3, color=GOLD))
		self.wait(2)


		# y = ax + 2 - a
		a_start, a_end = -50, 60

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 50)/a_range * (gradient_steps-1))]


		question_2 = Text("Only 1", font_size=24).move_to(UP*3)
		self.play(Transform(question, question_2))
		self.wait(2)


		y_4x_m2 = axes.plot(lambda x: -3*x*x + 13*x - 8, x_range=[-1, 10], color=get_line_colour(8))
		y_4x_m2_label = MathTex("y = -3x^{2} + 13x - 8", font_size=24, color=get_line_colour(8)).next_to(axes.coords_to_point(3.5, 2), RIGHT)
		self.play(Create(y_4x_m2), Write(y_4x_m2_label))
		self.bring_to_front(point, point_label, point_2, point_label_2, point_3, point_label_3)		
		self.wait(2)


		deg2 = Text("A degree-2 polynomial is uniquely defined by 3 points.", 
			font_size=20, color=BLACK, t2c={"1": MAROON, "2": MAROON, "3": MAROON})
		rect = BackgroundRectangle(deg2, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		self.play(FadeIn(rect), Write(deg2))
		self.wait(2)

		deg1 = Text("A degree-1 polynomial is uniquely defined by 2 points.", 
			font_size=20, color=BLACK, t2c={"1": MAROON, "2": MAROON, "3": MAROON})
		self.play(Transform(deg2, deg1))
		self.wait(2)

		degd = Text("A degree-d polynomial is uniquely defined by d+1 points.", font_size=20, color=BLACK)
		self.play(Transform(deg2, degd))
		self.wait(2)



config.background_color = "#000000"

class CubicWoo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-4, 8, 1],
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(DOWN*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		point = Dot(axes.coords_to_point(1, 2), color=RED)
		point_label = MathTex("(1, 2)", font_size=24).next_to(point, RIGHT, buff=0.2)

		point_2 = Dot(axes.coords_to_point(2, 6), color=ORANGE)
		point_label_2 = MathTex("(2, 6)", font_size=24).next_to(point_2, RIGHT, buff=0.2)

		point_3 = Dot(axes.coords_to_point(3, 4), color=GOLD)
		point_label_3 = MathTex("(3, 4)", font_size=24).next_to(point_3, RIGHT, buff=0.2)

		self.add(axes, labels, point, point_label, point_2, point_label_2, point_3, point_label_3)
		self.wait(2)


		a_start, a_end = -110, 170

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 110)/a_range * (gradient_steps-1))]


		# This is a new thing for me - this tracks the value of a				
		a_tracker = ValueTracker(a_start)

		def get_line():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			return axes.plot(
				lambda x: ((a-13)/11)*x*x*x - (3*(2*a-15)/11)*x*x + a*x - (6*a+32)/11 + 2,
				x_range=[-1, 10],
				color=colour,
				stroke_width=4
			)

		# Each frame it redraws the line
		line = always_redraw(get_line)
		self.add(line)
		self.bring_to_front(point, point_label, point_2, point_label_2, point_3, point_label_3)


		def get_equation():
			a = a_tracker.get_value()

			eq = MathTex(
			    "y = ", f"{((a-13)/11):.2f}", "x^{3} + ", f"{-1*(3*(2*a-15)/11):.2f}", "x^{2} + ", f"{a:.2f}", "x + ", f"{-1*(6*a+32)/11 + 2:.2f}",
			    color=get_line_colour(a),
			    font_size=24
			)
			eq.move_to(UP*2 + RIGHT*4)
			return eq

		equation = always_redraw(get_equation)
		self.add(equation)


		self.play(a_tracker.animate.set_value(a_end), run_time=6, rate_func=linear)
		self.wait(2)	


		point_4 = Dot(axes.coords_to_point(4, 2), color=GREEN)
		point_label_4 = MathTex("(4, 2)", font_size=24).next_to(point_4, RIGHT, buff=0.2)
		self.play(Create(point_4), Write(point_label_4))	
		self.play(Flash(point_4, color=GREEN))	
		self.wait(2)

		self.play(a_tracker.animate.set_value(24), run_time=1, rate_func=linear)
		self.bring_to_front(point, point_label, point_2, point_label_2, point_3, point_label_3, point_4, point_label_4)	
		self.wait(2)



config.background_color = "#ffffff"

class ShamirExplained(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Shamir's Secret Sharing", gradient=(ORANGE, GREEN, PURPLE)).move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		n_shares = make_speech_bubble([GREEN, ORANGE], UP*2 + LEFT*4, 3.5, 1)
		n_shares_text = Text("Split a secret\ninto n shares.", color=BLACK, font_size=20).move_to(n_shares.get_center())
		self.play(FadeIn(n_shares), Write(n_shares_text))

		k_shares = make_speech_bubble([PURPLE, GREEN, ORANGE], UP*2, 3.5, 1)
		k_shares_text = Text("≥ k shares can\nrecover the secret.", color=BLACK, font_size=20).move_to(k_shares.get_center())
		self.play(FadeIn(k_shares), Write(k_shares_text))

		less_k_shares = make_speech_bubble([PURPLE, GREEN], UP*2 + RIGHT*4, 3.5, 1)
		less_k_shares_text = Text("< k shares are\ncompletely useless.", color=BLACK, font_size=20).move_to(less_k_shares.get_center())
		self.play(FadeIn(less_k_shares), Write(less_k_shares_text))
		self.wait(2)

		self.play(FadeOut(n_shares), FadeOut(n_shares_text), FadeOut(k_shares), FadeOut(k_shares_text), FadeOut(less_k_shares), FadeOut(less_k_shares_text))


		poly_fact = Text("A polynomial of degree d is uniquely determined by d+1 distinct points.", color=BLACK, weight=BOLD, font_size=20).move_to(UP*2)
		self.play(Write(poly_fact))
		self.wait(2)


		line = Line(start=UP*1.5+LEFT*0.8, end=DOWN*4+LEFT*0.8)
		line.set_color_by_gradient(ORANGE, GREEN, PURPLE)
		self.play(Create(line))


		select_polynomial = Text("Choose a degree k-1 polynomial.", color=BLACK, font_size=16).move_to(LEFT*4 + UP)
		self.play(Write(select_polynomial))

		polynomial = MathTex("P(x) = a_{k-1} x^{k-1} + a_{k-2} x^{k-2} + ... + a_{1} x^{1} + a_{0}", color=BLACK, font_size=24).next_to(select_polynomial, DOWN)
		self.play(Write(polynomial))
		self.wait(2)


		axes = Axes(
			x_range=[-2, 6, 1],
			y_range=[-10, 20, 5],
			x_length=7,
			y_length=5,
			axis_config={
				"include_numbers": False, 
				"color": BLACK,
				"include_tip": False
			}
		)

		def cubic(x):
			return 0.5 * x**3 - 3 * x**2 + 2 * x + 5

		curve = axes.plot(cubic, x_range=[-1.7, 6], use_smoothing=True, color=BLACK)

		graph_group = VGroup(axes, curve)
		graph_group.to_corner(DOWN + RIGHT, buff=0.5)

		self.play(Create(axes))
		self.play(Create(curve), run_time=2)
		self.wait(2)


		secret_key = Text("Secret key (S) is the y-intercept.", color=BLACK, font_size=16).next_to(polynomial, DOWN, buff=0.5)
		self.play(Write(secret_key))

		secret_key_2 = MathTex("S = P(0) = a_{0}", color=BLACK, font_size=24).next_to(secret_key, DOWN)
		self.play(Write(secret_key_2))
		self.wait(2)

		colors = color_gradient([ORANGE, GREEN, PURPLE], 7)


		x0 = 0
		y0 = cubic(x0)
		dot = Dot(axes.c2p(x0, y0), color=colors[0], radius=0.08)
		label = Text(f"Secret = {str(int(y0))}", font_size=16, color=colors[0]).next_to(dot, UP + LEFT, buff=0.2)

		graph_group.add(dot, label)
		self.play(Create(dot), Write(label))
		self.wait(2)


		n_shares = Text("Select n distinct points.", color=BLACK, font_size=16).next_to(secret_key_2, DOWN, buff=0.5)
		self.play(Write(n_shares))

		n_points = MathTex("\\forall (x_{i}, y_{i}) \\in \\{(x_{1}, y_{1}), (x_{2}, y_{2}), ..., (x_{n}, y_{n})\\}, P(x_{i}) = y_{i}", color=BLACK, font_size=24).next_to(n_shares, DOWN)
		self.play(Write(n_points))
		self.wait(2)


		dots = VGroup()
		labels = VGroup()
		for i in range(1, 7):
			x0 = i
			y0 = cubic(x0)
			dot_2 = Dot(axes.c2p(x0, y0), color=colors[i], radius=0.08)
			label_2 = MathTex(f"({x0}, {y0})", font_size=20, color=colors[i]).next_to(dot_2, LEFT+DOWN)

			graph_group.add(dot_2, label_2)
			dots.add(dot_2)
			labels.add(label_2)
			self.play(Create(dot_2), Write(label_2))
		self.wait(2)


		recover = Text("S is recoverable if ≥ k points are known.", color=BLACK, font_size=16).next_to(n_points, DOWN, buff=0.5)
		self.play(Write(recover))
		self.wait(2)


		self.play(FadeOut(curve), FadeOut(dots), FadeOut(labels), FadeOut(dot), FadeOut(label))

		subset = [0, 3, 4, 5]
		self.play(*[FadeIn(dots[i]) for i in subset], *[FadeIn(labels[i]) for i in subset])
		self.play(Create(curve))
		self.play(FadeIn(dot), FadeIn(label))
		self.play(FadeOut(curve), *[FadeOut(dots[i]) for i in subset], *[FadeOut(labels[i]) for i in subset], FadeOut(dot), FadeOut(label))

		subset = [1, 2, 3, 4]
		self.play(*[FadeIn(dots[i]) for i in subset], *[FadeIn(labels[i]) for i in subset])
		self.play(Create(curve))
		self.play(FadeIn(dot), FadeIn(label))
		self.play(FadeOut(curve), *[FadeOut(dots[i]) for i in subset], *[FadeOut(labels[i]) for i in subset], FadeOut(dot), FadeOut(label))

		subset = [0, 1, 3, 5]
		self.play(*[FadeIn(dots[i]) for i in subset], *[FadeIn(labels[i]) for i in subset])
		self.play(Create(curve))
		self.play(FadeIn(dot), FadeIn(label))
		self.play(FadeOut(curve), *[FadeOut(dots[i]) for i in subset], *[FadeOut(labels[i]) for i in subset], FadeOut(dot), FadeOut(label))



config.background_color = "#000000"

class FamilyPolynomial(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.25, LEFT*5+DOWN*3.5)
		uncle = make_hooman_with_label(GOLD, "Uncle", 0.25, LEFT*3+DOWN*3.5)
		dad = make_hooman_with_label(GREEN, "Dad", 0.25, LEFT*1+DOWN*3.5)
		mum = make_hooman_with_label(TEAL, "Mum", 0.25, RIGHT*1+DOWN*3.5)
		brother = make_hooman_with_label(BLUE, "Brother", 0.25, RIGHT*3+DOWN*3.5)
		you = make_hooman_with_label(PURPLE, "You", 0.25, RIGHT*5+DOWN*3.5)

		fam_bam = VGroup(grandpa, uncle, dad, mum, brother, you)
		self.play(Create(fam_bam))
		self.wait(2)


		n_text = Text("n = 6").move_to(UP)
		self.play(Write(n_text))
		self.wait(2)

		k_text = Text("k = 4").next_to(n_text, DOWN)
		self.play(Write(k_text))
		self.wait(2)

		self.play(FadeOut(n_text), FadeOut(k_text))


		axes = Axes(
			x_range=[-1, 7, 1],
			y_range=[-50, 170, 10],
			y_length=6,
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).move_to(UP*0.75)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		self.play(Create(axes), Write(labels))
		self.wait(2)


		fam_cubic = axes.plot(lambda x: x*x*x - 2*x*x - 20*x + 64, x_range=[-1, 7], color=WHITE)
		fam_cubic_label = MathTex("P(x) = x^{3} - 2x^{2} - 20x + 64", font_size=36, color=WHITE).move_to(UP*3)
		self.play(Write(fam_cubic_label))
		self.play(Create(fam_cubic))
		self.wait(2)


		y_int_maths = MathTex("P(0) = 0^{3} - 2 \\cdot 0^{2} - 20 \\cdot 0 + 64", font_size=24).next_to(fam_cubic_label, DOWN)
		self.play(Write(y_int_maths))
		self.wait(2)

		y_int_maths_2 = MathTex("S = 64", font_size=24).next_to(fam_cubic_label, DOWN)
		self.play(Transform(y_int_maths, y_int_maths_2))


		y_int = Dot(axes.coords_to_point(0, 64), color=RED)
		y_int_label = MathTex("(0, 64)", font_size=24, color=RED).next_to(y_int, LEFT, buff=1)
		self.play(Create(y_int), Write(y_int_label), FadeOut(y_int_maths))
		self.wait(2)



		fam_points = [(1, 43), (2, 24), (3, 13), (4, 16), (5, 39), (6, 88)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		point_group = VGroup()
		label_group = VGroup()

		i = 0
		for point in fam_points:
			dot = Dot(axes.coords_to_point(*point), color=colours[i])

			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN
			lbl = MathTex(f"{point}", font_size=24, color=colours[i]).next_to(dot, pos, buff=0.2)

			point_group.add(dot)
			label_group.add(lbl)

			self.play(Create(dot), Write(lbl))

			i += 1
		self.wait(2)


		move_point_anim = []
		for i in range(0, len(label_group)):
			move_point_anim.append(label_group[i].animate.next_to(fam_bam[i], UP))
		self.play(*move_point_anim)
		self.wait(2)


		self.play(
			FadeOut(point_group),
			FadeOut(y_int), FadeOut(y_int_label),
			FadeOut(fam_cubic), FadeOut(fam_cubic_label)
		)


		fam_indexes = [0, 1, 2, 3, 4, 5]

		for count in range(0, 3):
			index_sample = random.sample(fam_indexes, 4)

			point_subset = VGroup()
			label_subset = VGroup()
			for i in index_sample:		

				pos = RIGHT+UP
				if i >= 4:
					pos = RIGHT+DOWN

				self.play(Create(point_group[i]), label_group[i].animate.next_to(point_group[i], pos, buff=0.2))

				point_subset.add(point_group[i])
				label_subset.add(label_group[i])

			self.wait(2)

			self.play(Create(fam_cubic))
			self.bring_to_front(point_subset)
			self.play(Write(fam_cubic_label))
			self.wait(2)

			self.play(Create(y_int))
			self.play(Write(y_int_label))
			self.wait(2)

			self.play(
				FadeOut(point_subset),
				FadeOut(y_int), FadeOut(y_int_label),
				FadeOut(fam_cubic), FadeOut(fam_cubic_label),
				*[label_group[i].animate.next_to(fam_bam[i], UP) for i in range(0, len(fam_bam))]
			)
			self.wait(2)


		index_sample = [0, 3, 4]

		point_subset = VGroup()
		label_subset = VGroup()
		for i in index_sample:		

			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN

			self.play(Create(point_group[i]), label_group[i].animate.next_to(point_group[i], pos, buff=0.2))

			point_subset.add(point_group[i])
			label_subset.add(label_group[i])

		self.wait(2)


		a_start, a_end = -170, 140

		def get_line_colour(a):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a + 170)/a_range * (gradient_steps-1))]

		
		a_tracker = ValueTracker(a_start)

		def get_cubic(a, x):
			return ((a+49)/29)*x*x*x - (2*(5*a+129)/29)*x*x + a*x + (-20*a+209)/29 + 43


		def get_line():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			return axes.plot(
				lambda x: get_cubic(a, x),
				x_range=[-0.5, 7],
				color=colour,
				stroke_width=4
			)

		line = always_redraw(get_line)
		self.add(line)
		self.bring_to_front(point_subset, label_subset)


		def get_y_int():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			y_int = Dot(axes.coords_to_point(0, get_cubic(a, 0)), color=RED)
			y_int_label = MathTex(f"(0, {get_cubic(a, 0):.2f})", font_size=24, color=RED).next_to(y_int, LEFT, buff=1)
			dot_label = VGroup(y_int, y_int_label)

			return dot_label

		y_int_group = always_redraw(get_y_int)
		self.add(y_int_group)


		def get_equation():
			a = a_tracker.get_value()

			eq = MathTex(
			    "P(x) = ", f"{((a+49)/29):.2f}", "x^{3} + ", f"{-1*(2*(5*a+129)/29):.2f}", "x^{2} + ", f"{a:.2f}", "x + ", f"{(-20*a+209)/29 + 43:.2f}",
			    color=get_line_colour(a),
			    font_size=36
			)
			eq.move_to(UP*3)
			return eq

		equation = always_redraw(get_equation)
		self.add(equation)


		self.play(a_tracker.animate.set_value(a_end), run_time=6, rate_func=linear)
		self.wait(2)	




config.background_color = "#090f1a"

class PrecisionSucks(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bro = make_hooman_with_label(BLUE, "Brother", 0.4, LEFT*5+UP*2.5)
		self.play(Create(bro))

		speech_bubble = make_speech_bubble([TEAL, BLUE], RIGHT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Let's randomly create a degree-3 polynomial!", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))


		axes = Axes(
			x_range=[-1, 3, 1],
			y_range=[-1, 4, 1],
			y_length=6,
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).scale(0.75).shift(DOWN*1.5)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		self.play(Create(axes), Write(labels))
		self.wait(2)


		round_cubic = axes.plot(lambda x: 1/3 * x*x*x - 5/7 * x*x + 2/9 * x + 2/5, x_range=[-1, 3], color=WHITE)
		round_cubic_label = MathTex("P(x) = \\frac{1}{3} x^{3} - \\frac{5}{7} x^{2} + \\frac{2}{9} x + \\frac{2}{5}", font_size=36, color=WHITE).move_to(UP*1.25 + RIGHT)
		self.play(Write(round_cubic_label))
		self.play(Create(round_cubic))

		y_int = Dot(axes.coords_to_point(0, 0.4), color=RED)
		y_int_label = MathTex("(0, \\frac{2}{5})", font_size=24, color=RED).next_to(y_int, LEFT+UP*0.5, buff=1)
		self.play(Create(y_int), Write(y_int_label))
		self.wait(2)


		speech2 = Text("How can we ensure the computer is precise enough?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)

		self.play(FadeOut(bro), FadeOut(speech_bubble), FadeOut(speech1))		


		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		fam_points = [(1/2, 943/2520), (3/4, 2053/6720), (1, 76/315), (7/5, 254/1125), (3/2, 211/840), (11/4, 51239/20160)]
		fam_labels = [
			MathTex("(\\frac{1}{2}, \\frac{943}{2520})", font_size=24, color=colours[0]),
			MathTex("(\\frac{3}{4}, \\frac{2053}{6720})", font_size=24, color=colours[1]),
			MathTex("(1, \\frac{76}{315})", font_size=24, color=colours[2]),
			MathTex("(\\frac{7}{5}, \\frac{254}{1125})", font_size=24, color=colours[3]),
			MathTex("(\\frac{3}{2}, \\frac{211}{840})", font_size=24, color=colours[4]),
			MathTex("(\\frac{11}{4}, \\frac{51239}{20160})", font_size=24, color=colours[5]),
		]		
		point_group = VGroup()
		label_group = VGroup()

		i = 0
		for point in fam_points:
			dot = Dot(axes.coords_to_point(*point), color=colours[i])
			lbl = fam_labels[i].move_to(UP*3 + LEFT*(2.5 - i)*2)

			point_group.add(dot)
			label_group.add(lbl)

			self.play(Create(dot), Write(lbl))

			i += 1
		self.wait(2)


		i = 0
		for point in fam_points:
			lbl_2 = MathTex(f"{point}", font_size=24, color=colours[i]).move_to(UP*(2.5+i%2) + LEFT*(2.5 - i)*2)
			self.play(Transform(label_group[i], lbl_2))
			i += 1

		self.wait(2)


		def whacky_rounding(x):
			ret = 0

			for i in range(0, 4):
				top = 1
				bottom = 1

				for j in range(0, 4):
					if j != i:
						top *= (x - fam_points[j][0])
						bottom *= (fam_points[i][0] - fam_points[j][0])

				ret += (top/bottom)*fam_points[i][1]

			return ret



		farked_cubic = axes.plot(
			lambda x: whacky_rounding(x), x_range=[-1, 3], color=MAROON
		)
		self.play(Create(farked_cubic))
		self.wait(2)

		y_int_2 = Dot(axes.coords_to_point(0, whacky_rounding(0)), color=MAROON)
		y_int_label_2 = MathTex(f"(0, {whacky_rounding(0)})", font_size=24, color=MAROON).next_to(y_int_2, LEFT, buff=1)
		self.play(Create(y_int_2), Write(y_int_label_2))
		self.wait(2)



config.background_color = "#0d0702"

class UseIntegers(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		polynomial = MathTex("P(x) = a_{k-1} x^{k-1} + a_{k-2} x^{k-2} + ... + a_{1} x^{1} + a_{0}")
		self.play(Write(polynomial))

		n_points = MathTex("\\forall (x_{i}, y_{i}) \\in \\{(x_{1}, y_{1}), (x_{2}, y_{2}), ..., (x_{n}, y_{n})\\}, P(x_{i}) = y_{i}").move_to(DOWN*2)
		self.play(Write(n_points))
		self.wait(2)


		integer_coefficients = MathTex("{a_{k-1}, a_{k-2}, ..., a_{1}, a_{0}} \\in \\mathbb{Z}", font_size=30).next_to(polynomial, DOWN)
		integer_shares = MathTex("{x_{1}, x_{2}, ..., x_{n}} \\in \\mathbb{Z}", font_size=30).next_to(n_points, DOWN)

		self.play(Write(integer_coefficients))
		self.wait(1)
		self.play(Write(integer_shares))
		self.wait(1)


		woo = Text("☑", color=GREEN, font_size=96).move_to(UP*2)
		self.play(SpinInFromNothing(woo))
		self.wait(2)


		self.play(FadeOut(woo))


		grandpa = make_hooman_with_label(ORANGE, "Grandpa", 0.4, RIGHT*5+UP*2.5)
		self.play(Create(grandpa))

		speech_bubble = make_speech_bubble([ORANGE, GOLD], LEFT*1.75+UP*2.5, 9, 1.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Each possible value of the key should be equally likely.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		speech2 = Text("Could some information about the secret key be leaked?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)


		self.play(FadeOut(polynomial), FadeOut(n_points), FadeOut(integer_coefficients), FadeOut(integer_shares))


		axes = Axes(
			x_range=[-1, 7, 1],
			y_range=[-50, 170, 20],
			y_length=6,
			tips=False,
			axis_config={"include_numbers": True, "font_size": 18},
		).scale(0.75).move_to(DOWN)
		labels = axes.get_axis_labels(x_label="x", y_label="y")

		self.play(Create(axes), Write(labels))
		self.wait(2)


		fam_cubic = axes.plot(lambda x: x*x*x - 2*x*x - 20*x + 64, x_range=[-1, 7], color=WHITE)
		fam_cubic_label = MathTex("P(x) = x^{3} - 2x^{2} - 20x + 64", color=WHITE, font_size=24).move_to(UP+RIGHT)
		self.play(Write(fam_cubic_label))
		self.play(Create(fam_cubic))
		self.wait(2)

		y_int = Dot(axes.coords_to_point(0, 64), color=RED)
		y_int_label = MathTex("(0, 64)", font_size=24, color=RED).next_to(y_int, LEFT, buff=1)
		self.play(Create(y_int), Write(y_int_label))
		self.wait(2)

		self.play(FadeOut(fam_cubic), FadeOut(fam_cubic_label), FadeOut(y_int), FadeOut(y_int_label))



		fam_points = [(1, 43), (2, 24), (3, 13)]
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		point_group = VGroup()
		label_group = VGroup()

		i = 0
		for point in fam_points:
			dot = Dot(axes.coords_to_point(*point), color=colours[i])

			pos = RIGHT+UP
			if i >= 4:
				pos = RIGHT+DOWN
			lbl = MathTex(f"{point}", font_size=24, color=colours[i]).next_to(dot, pos, buff=0.2)

			point_group.add(dot)
			label_group.add(lbl)

			self.play(Create(dot), Write(lbl))

			i += 1
		self.wait(2)


		a_start, a_end = -170, 140

		def get_line_colour(a, a_end=140, a_start=-170):
			a_range, gradient_steps = a_end - a_start, 100

			return color_gradient(
				[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], gradient_steps
			)[int((a - a_start)/a_range * (gradient_steps-1))]

		
		a_tracker = ValueTracker(a_start)


		def get_cubic(a, x):
			return ((a+31)/11)*x*x*x - (2*(3*a+71)/11)*x*x + a*x + (-6*a+111)/11 + 43


		def get_line():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			return axes.plot(
				lambda x: get_cubic(a, x),
				x_range=[-0.5, 7],
				color=colour,
				stroke_width=4
			)

		line = always_redraw(get_line)
		self.add(line)
		self.bring_to_front(point_group, label_group)


		def get_y_int():
			a = a_tracker.get_value()
			colour = get_line_colour(a)

			y_int = Dot(axes.coords_to_point(0, get_cubic(a, 0)), color=RED)
			y_int_label = MathTex(f"(0, {get_cubic(a, 0):.2f})", font_size=24, color=RED).next_to(y_int, LEFT, buff=1)
			dot_label = VGroup(y_int, y_int_label)

			return dot_label

		y_int_group = always_redraw(get_y_int)
		self.add(y_int_group)


		def get_equation():
			a = a_tracker.get_value()

			eq = MathTex(
			    "P(x) = ", f"{((a+31)/11):.2f}", "x^{3} + ", f"{-1*(2*(3*a+71)/11):.2f}", "x^{2} + ", f"{a:.2f}", "x + ", f"{(-6*a+111)/11 + 43:.2f}",
			    color=get_line_colour(a),
			    font_size=24
			)
			eq.move_to(UP+RIGHT)
			return eq

		equation = always_redraw(get_equation)
		self.add(equation)


		self.play(a_tracker.animate.set_value(a_end), run_time=6, rate_func=linear)
		self.wait(2)	

		self.remove(equation, line)


		a_start, a_end = -50, 50

		def get_line_2():
			a = a_tracker.get_value()

			colour = GRAY
			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and ((-6*a+111)/11 + 43).is_integer():
				colour = get_line_colour(a, a_end=a_end, a_start=a_start)

			return axes.plot(
				lambda x: get_cubic(a, x),
				x_range=[-0.5, 7],
				color=colour,
				stroke_width=4
			)


		line_2 = always_redraw(get_line_2)
		self.add(line_2)
		self.bring_to_front(point_group, label_group)


		def get_y_int_2():
			a = a_tracker.get_value()

			colour = GRAY
			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and ((-6*a+111)/11 + 43).is_integer():
				colour = RED

			y_int = Dot(axes.coords_to_point(0, get_cubic(a, 0)), color=colour)
			y_int_label = MathTex(f"(0, {get_cubic(a, 0):.2f})", font_size=24, color=colour).next_to(y_int, LEFT, buff=1)
			dot_label = VGroup(y_int, y_int_label)

			return dot_label


		y_int_group_2 = always_redraw(get_y_int_2)
		self.add(y_int_group_2)


		def get_equation_2():
			a = a_tracker.get_value()

			colour = GRAY
			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and a.is_integer() and ((-6*a+111)/11 + 43).is_integer():
				colour = get_line_colour(a, a_end=a_end, a_start=a_start)

			eq = MathTex(
			    "P(x) = ", f"{((a+31)/11):.2f}", "x^{3} + ", f"{-1*(2*(3*a+71)/11):.2f}", "x^{2} + ", f"{a:.2f}", "x + ", f"{(-6*a+111)/11 + 43:.2f}",
			    color=colour,
			    font_size=24
			)
			eq.move_to(UP+RIGHT)
			return eq


		equation_2 = always_redraw(get_equation_2)
		self.add(equation_2)

		
		a_tracker.set_value(a_start)

		step = 1
		pause_time = 0.5
		frame_time = 0.02

		a = a_start
		while a <= a_end:
			self.play(a_tracker.animate.set_value(a), run_time=frame_time, rate_func=linear)

			if ((a+31)/11).is_integer() and (-1*(2*(3*a+71)/11)).is_integer() and ((-6*a+111)/11 + 43).is_integer():
				self.wait(pause_time)

			a += step


		self.wait(2)



config.background_color = "#15131c"

class CubicAlgebra(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		general = MathTex("y = ax^{3} + bx^{2} + cx + d").move_to(UP*3)
		self.play(Write(general))
		self.wait(2)

		point_text = Text("We want the curve to pass through (1, 43), (2, 24) and (3, 13)", 
			font_size=24, t2c={"(1, 43)": ORANGE, "(2, 24)": GOLD, "(3, 13)": GREEN}).next_to(general, DOWN, buff=1)
		self.play(Write(point_text))
		self.wait(2)

		sub_eq = MathTex("43", "=", "a", "\\cdot", "1", "^{3}", "+", "b", "\\cdot", "1", "^{2}", "+", "c", "\\cdot", "1", "+", "d", "\\quad", "(1)", font_size=36)
		sub_eq.set_color_by_tex("43", ORANGE)
		sub_eq.set_color_by_tex("1", ORANGE)
		sub_eq.next_to(point_text, DOWN)
		self.play(Write(sub_eq))

		sub_eq_2 = MathTex("24", "=", "a", "\\cdot", "2", "^{3}", "+", "b", "\\cdot", "2", "^{2}", "+", "c", "\\cdot", "2", "+", "d", "\\quad", "(2)", font_size=36)
		sub_eq_2.set_color_by_tex("24", GOLD)
		sub_eq_2.set_color_by_tex("2", GOLD)
		sub_eq_2.next_to(sub_eq, DOWN)
		self.play(Write(sub_eq_2))

		sub_eq_3 = MathTex("13", "=", "a", "\\cdot", "3", "^{3}", "+", "b", "\\cdot", "3", "^{2}", "+", "c", "\\cdot", "3", "+", "d", "\\quad", "(3)", font_size=36)
		sub_eq_3.set_color_by_tex("13", GREEN)
		sub_eq_3.set_color_by_tex("3", GREEN)
		sub_eq_3.next_to(sub_eq_2, DOWN)
		self.play(Write(sub_eq_3))
		self.wait(2)

		simplified = MathTex("43", "=", "a", "+", "b", "+", "c", "+", "d", "\\quad", "(1)", font_size=36).next_to(point_text, DOWN)
		simplified_2 = MathTex("24", "=", "8", "a", "+", "4", "b", "+", "2", "c", "+", "d", "\\quad", "(2)", font_size=36).next_to(sub_eq, DOWN)
		simplified_3 = MathTex("13", "=", "27", "a", "+", "9", "b", "+", "3", "c", "+", "d", "\\quad", "(3)", font_size=36).next_to(sub_eq_2, DOWN)

		self.play(TransformMatchingTex(sub_eq, simplified))
		self.play(TransformMatchingTex(sub_eq_2, simplified_2))
		self.play(TransformMatchingTex(sub_eq_3, simplified_3))
		self.wait(2)


		solve = Text("(1) - (2) + 1/3 * (3)", font_size=24, 
			t2c={"(1)": ORANGE, "(2)": GOLD, "(3)": GREEN}).next_to(sub_eq_3, DOWN, buff=1)
		self.play(Write(solve))
		self.wait(2)

		big_boi = MathTex("a - 8a + 9a + b - 4b + 3b + c - 2c + c + d - d + \\frac{1}{3} d = 43 - 24 + \\frac{13}{3}", font_size=36).next_to(solve, DOWN)
		self.play(Write(big_boi))
		self.wait(2)

		big_boi_simp = MathTex("2a + \\frac{1}{3} d", "=", "\\frac{70}{3}", font_size=36).next_to(solve, DOWN)
		self.play(Transform(big_boi, big_boi_simp))
		self.wait(2)

		big_boi_simp_2 = MathTex("6a + d", "=", "70", font_size=36).next_to(solve, DOWN)
		self.play(Transform(big_boi, big_boi_simp_2))
		self.wait(2)

		big_boi_simp_3 = MathTex("d", "=", "70 - 6a", font_size=36).next_to(solve, DOWN)
		self.play(Transform(big_boi, big_boi_simp_3))
		self.wait(2)


		oh_no = MathTex("d", "=", "70", "-", "6", "\\cdot", "a").next_to(solve, DOWN)
		self.play(oh_no.animate.shift(DOWN))
		self.wait(2)


		for a in range(-10, 10):
			oh_no_2 = MathTex("d", "=", "70", "-", "6", "\\cdot", str(a), "=", str(70-6*a)).next_to(solve, DOWN).shift(DOWN)
			oh_no_2[6].set_color(RED)
			self.play(Transform(oh_no, oh_no_2))

		self.wait(2)