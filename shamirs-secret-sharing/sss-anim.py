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
