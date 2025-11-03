from manim import *

from bit_manipulation import BinaryNumber

config.background_color = "#15131c"


def get_value_colour(min_val, max_val, val):
	val_range, gradient_steps = max_val-min_val, 100

	return color_gradient(
		[RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK], 
		gradient_steps
	)[int((val - min_val)/val_range * (gradient_steps-1))]


def get_binary_colour(bit):
	if bit == 0:
		return RED
	else:
		return GREEN



class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("8 Epic Bit Manipulation Tricks").move_to(UP*3)
		subtitle = Text("From Beginner to Expert", 
			font_size=24,
			t2c={"Beginner": GREEN, "Expert": PINK}).move_to(UP*2)

		self.add(title)
		self.add(subtitle)



class IntroSlide(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("8 Epic Bit Manipulation Tricks").move_to(UP)
		subtitle = Text("From Beginner to Expert", 
			font_size=24,
			t2c={"Beginner": GREEN, "Expert": PINK}).next_to(title, DOWN)

		self.play(Write(title))
		self.play(Write(subtitle))
		self.wait(2)



class BinaryNumberExplanation(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Binary Explanation").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		# Count up to 349
		d1, d2, d3 = Dot(radius=0.01), Dot(radius=0.01), Dot(radius=0.01)
		digits = VGroup(d1, d2, d3).arrange(RIGHT, buff=0.5)
		

		dig1, dig2, dig3 = 0, 0, 0
		RT = 0.5
		for dig1 in range(0, 4):
			if dig3 > 0:
				RT = 0.005

			self.play(Transform(d1, 
				Text(str(dig1), color=get_value_colour(0, 9, dig1)).move_to(d1),
				run_time=RT
			))

			for dig2 in range(0, 10):
				if dig1 == 0 and dig2 > 0:
					RT = 0.01

				self.play(Transform(d2, 
					Text(str(dig2), color=get_value_colour(0, 9, dig2)).move_to(d2),
					run_time=RT
				))

				for dig3 in range(0, 10):
					self.play(Transform(d3, 
						Text(str(dig3), color=get_value_colour(0, 9, dig3)).move_to(d3),
						run_time=RT
					))							

				if dig1 == 3 and dig2 == 4 and dig3 == 9:
					break;

		self.wait(2)

		self.play(digits.animate.shift(UP))

		expand = VGroup(
			Tex("$3\\times 100$", font_size=44, color=get_value_colour(0, 9, dig1)),
			Tex("+", font_size=44),
			Tex("$4\\times 10$", font_size=44, color=get_value_colour(0, 9, dig2)),
			Tex("+", font_size=44),
			Tex("$9\\times 1$", font_size=44, color=get_value_colour(0, 9, dig3))
		).arrange(RIGHT)

		for text in expand:
			self.play(Write(text))
		self.wait(1)

		expand2 = VGroup(
			Tex("$3\\times 10^{2}$", font_size=36, color=get_value_colour(0, 9, dig1)),
			Tex("+", font_size=36),
			Tex("$4\\times 10^{1}$", font_size=36, color=get_value_colour(0, 9, dig2)),
			Tex("+", font_size=36),
			Tex("$9\\times 10^{0}$", font_size=36, color=get_value_colour(0, 9, dig3))
		).arrange(RIGHT).next_to(expand, DOWN)

		for text in expand2:
			self.play(Write(text))
		self.wait(1)

		self.play(FadeOut(digits), FadeOut(expand), FadeOut(expand2))




		# Display binary 349 = 101011101
		binary_text = Text("0", t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP)
		self.play(Write(binary_text))
		self.wait(1)

		self.play(
			Transform(binary_text, 
			Text("1", t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP))
		)
		self.wait(1)

		for i in range(0, 350):
			self.play(
				Transform(binary_text, 
					Text(format(i, 'b'), t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP), 
					run_time=0.005)
				)
		self.wait(2)

		binary_str = "101011101"
		expand = VGroup()
		expand2 = VGroup()
		answer = 0

		for i in range(0, len(binary_str)):
			expand.add(Tex(f"${binary_str[i]}\\times 2^{len(binary_str)-i-1}$", 
				font_size=28, 
				color=get_binary_colour(int(binary_str[i])))
			)

			term = int(binary_str[i]) * 2**(len(binary_str)-i-1)
			expand2.add(Tex(f"${term}$", 
				font_size=36, 
				color=get_binary_colour(int(binary_str[i])))
			)

			answer += term

			if i < len(binary_str)-1:
				expand.add(Tex("+", font_size=28))
				expand2.add(Tex("+", font_size=36))

		expand.arrange(RIGHT)
		expand2.arrange(RIGHT).next_to(expand, DOWN)

		for text in expand:
			self.play(Write(text))
		self.wait(1)

		for text in expand2:
			self.play(Write(text))
		self.wait(1)

		term_text = Text(f"= {answer}").next_to(expand2, DOWN, buff=0.5)
		self.play(Write(term_text))
		self.wait(2)

		self.play(
			FadeOut(binary_text), 
			FadeOut(expand), 
			FadeOut(expand2), 
			FadeOut(term_text)
		)



class BinaryNumberExplanation2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Binary Explanation").move_to(UP*3)
		self.add(title)
		self.wait(2)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()
		self.wait(1)

		binary.add_num_to_table(77)


		binary_str = "1001101"
		expand = VGroup()
		expand2 = VGroup()
		answer = 0

		for i in range(0, len(binary_str)):
			expand.add(Tex(f"${binary_str[i]}\\times 2^{len(binary_str)-i-1}$", 
				font_size=28, 
				color=get_binary_colour(int(binary_str[i])))
			)

			term = int(binary_str[i]) * 2**(len(binary_str)-i-1)
			expand2.add(Tex(f"${term}$", 
				font_size=36, 
				color=get_binary_colour(int(binary_str[i])))
			)

			answer += term

			if i < len(binary_str)-1:
				expand.add(Tex("+", font_size=28))
				expand2.add(Tex("+", font_size=36))

		expand.arrange(RIGHT).move_to(DOWN*2)
		expand2.arrange(RIGHT).next_to(expand, DOWN)

		for text in expand:
			self.play(Write(text))
		self.wait(1)

		for text in expand2:
			self.play(Write(text))
		self.wait(1)

		term_text = Text(f"= {answer}").next_to(expand2, DOWN, buff=0.5)
		self.play(Write(term_text))
		self.wait(2)



class DrawAndGlowLetter(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		self.play(Write(Text("Thank you for watching!").shift(UP*2)))

		letter_e = Text("e", font_size=200, color=TEAL)
		self.play(Write(letter_e))

		letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
		glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
		self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
		self.play(FadeOut(letter_e_stroke, glow_effect))

		self.wait(3)