from manim import *

from bit_manipulation import BinaryNumber, BitwiseTable, BitwiseSubtraction, fade_out_scene

config.background_color = "#140000"



class PowerOfTwo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[RED, MAROON], stroke_color=[RED, MAROON],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #6: Check if an integer is a power of 2.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)


		powers = VGroup()

		down = -1
		right = 1
		for i in range(0, 6):
			row = VGroup()

			power_of_two = Tex(f"$2^{i}$").move_to(DOWN*down+LEFT*2)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			power_of_two = Tex(f"${2**i}$").move_to(row[0].get_center()+RIGHT)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			power_of_two = Tex(f"${bin(2**i)[2:]}$").move_to(row[1].get_center()+RIGHT*right)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			powers.add(row)

			down += 0.75
			right += 0.13


		self.wait(5)
		self.play(powers.animate.scale(0.8).shift(LEFT*2.5))


		powers_2 = VGroup()

		down = -1
		right = 1
		for i in range(0, 6):
			row = VGroup()

			power_of_two = Tex(f"$2^{i}-1$").move_to(DOWN*down)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			power_of_two = Tex(f"${2**i - 1}$").move_to(row[0].get_center()+RIGHT*1.5)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			power_of_two = Tex(f"${0 if i != 0 else ''}{bin(2**i - 1)[2:]}$").move_to(row[1].get_center()+RIGHT*right)
			self.play(Write(power_of_two))
			row.add(power_of_two)

			powers_2.add(row)

			down += 0.75
			right += 0.13

		self.wait(5)

		self.play(powers_2.animate.scale(0.8).shift(RIGHT*1.5))
		self.wait(5)



class PowerOfTwo2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.shift(UP)

		string_1 = "100000"
		string_2 = "011111"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(5)

		fade_out_scene(self)


		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.shift(UP)

		string_1 = "110000"
		string_2 = "101111"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(5)



class DivisibleBy2K(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[RED, MAROON], stroke_color=[RED, MAROON],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #7: Check if an integer is divisible by 2^k.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)


		question = Text("Is 10101000 divisible by 2^3, or 8?", font_size=24)
		self.play(Write(question))
		self.wait(2)


		self.play(FadeOut(trick_group), question.animate.shift(UP*2.5))


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()


		num = 8+32+128
		binary.add_num_to_table(num, pace="fast")
		self.wait(1)


		factorisation = Tex(f"${num} = 2^{7} + 2^{5} + 2^{3}$", font_size=36).move_to(DOWN*2)
		self.play(Write(factorisation))
		self.wait(1)


		factorisation_2 = Tex("$= 2^{3}(2^{4} + 2^{2} + 2^{0})$", font_size=36).move_to(DOWN*2.5)
		self.play(Write(factorisation_2))
		self.wait(1)


		green_check = Text("☑", color=GREEN, font_size=108).move_to(UP*2.5)
		self.play(SpinInFromNothing(green_check))
		self.wait(5)


		self.play(FadeOut(green_check))
		binary.remove_num_from_table()
		self.play(FadeOut(factorisation), FadeOut(factorisation_2))


		question_2 = Text("Is 11101010 divisible by 2^2, or 4?", font_size=24).move_to(UP*2.5)
		self.play(Transform(question, question_2))
		self.wait(2)


		num = 2+8+32+64+128
		binary.add_num_to_table(num, pace="fast")
		self.wait(1)


		factorisation = Tex(f"${num} = 2^{7} + 2^{6} + 2^{5} + 2^{3} + 2^{1}$", font_size=36).move_to(DOWN*2)
		self.play(Write(factorisation))
		self.wait(1)


		factorisation_2 = Tex("$= 2^{2}(2^{5} + 2^{4} + 2^{3} + 2^{1}) + 2^{1}$", font_size=36).move_to(DOWN*2.5)
		self.play(Write(factorisation_2))
		self.wait(1)


		red_x = Text("X", color=RED, font_size=108).move_to(UP*2.5)
		self.play(SpinInFromNothing(red_x))
		self.wait(5)



class DivisibleBy2K2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()


		num = 8+16+32
		binary.add_num_to_table(num, pace="fast")
		self.wait(2)


		divisible = Text("This is divisible by 2^3.", color=GREEN, font_size=30).shift(UP*2)
		self.play(Write(divisible))
		self.wait(2)


		binary.flip_bit(5)
		divisible_2 = Text("This is not divisible by 2^3.", color=RED, font_size=30).shift(UP*2)
		self.play(Transform(divisible, divisible_2))
		self.wait(5)



class DivisibleBy2K3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		def show_code(x, k, res):
			example_question = Text(f"Is {x} divisible by {2**k}?", font_size=24).shift(UP*2.5)
			self.play(Write(example_question))


			example = Text(f"x = {x}, k = {k}", color=GRAY, font_size=24).shift(UP*2)
			self.play(Write(example))


			binary = BinaryNumber(self, 8)
			binary_table = binary.binary_table.move_to(ORIGIN+LEFT)
			binary.create_binary_table()


			num = x
			binary.add_num_to_table(num, pace="fast")
			self.wait(2)


			binary.add_num_to_table(1, pace="fast")
			self.wait(2)


			binary.shift("left", k, row=3)
			self.wait(2)


			instructions = Text("1 << k", font_size=20).next_to(binary.binary_table, UP)
			self.play(Write(instructions))
			self.wait(1)


			instructions_2 = Text("(1 << k) - 1", font_size=20).next_to(binary.binary_table, UP)
			self.play(Transform(instructions, instructions_2))
			self.wait(1)


			for i in range(8-k-1, 8):
				binary.flip_bit(i, row=3)
			self.wait(2)


			instructions_3 = Text("x & ((1 << k) - 1)", font_size=20).next_to(binary.binary_table, UP)
			self.play(Transform(instructions, instructions_3))
			self.wait(1)


			bitwise_table = BitwiseTable(self, "&", ORANGE)
			and_table = bitwise_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
			self.play(FadeIn(and_table))

			binary.perform_bitwise_operation(bitwise_table)
			self.wait(2)

			self.play(SpinInFromNothing(res))
			self.wait(5)


		show_code(168, 3, Text("☑", color=GREEN, font_size=108).move_to(UP*2.5))

		fade_out_scene(self)

		show_code(170, 3, Text("X", color=RED, font_size=108).move_to(UP*2.5))
