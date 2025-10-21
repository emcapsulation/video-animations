from manim import *

from bit_manipulation import BinaryNumber, BitwiseTable, BitwiseSubtraction, fade_out_scene

config.background_color = "#120800"



class Swap(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GOLD_D, ORANGE], stroke_color=[GOLD_D, ORANGE],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #4: Swap two variables.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)


		xor_tip = Text("Anything XORed with itself gives 0.", font_size=24).move_to(UP*2.5)
		self.play(Transform(trick_group, xor_tip))
		self.wait(2)


		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		# 210
		string_1 = "11010010"
		string_2 = "11010010"
		binary_table = bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class Swap2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		xor_tip_2 = Text("Anything XORed with 0 retains its value.", font_size=24).move_to(UP*2.5)
		self.play(Write(xor_tip_2))
		self.wait(2)


		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		# 117
		string_1 = "01110101"
		string_2 = "00000000"
		binary_table = bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class SwapTable(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		A_COLOUR = ORANGE
		B_COLOUR = PURPLE
		FZ=30
		FZ2=40


		swap_table = VGroup(
			VGroup(
				Text("Line #", font_size=FZ),
				Text("a", color=A_COLOUR, font_size=FZ),
				Text("b", color=B_COLOUR, font_size=FZ)
			).arrange(RIGHT, buff=2)
		).shift(UP*3)

		for h in swap_table[0]:
			self.play(Write(h))
		self.wait(2)


		# Row 0
		row_0 = VGroup(
			Text("0", font_size=FZ).move_to(swap_table[0][0].get_center()+DOWN),
			Tex("$a_0$", font_size=FZ2).move_to(swap_table[0][1].get_center()+DOWN),
			Tex("$b_0$", font_size=FZ2).move_to(swap_table[0][2].get_center()+DOWN)
		)
		swap_table.add(row_0)

		for h in swap_table[1]:
			self.play(Write(h))
		self.wait(2)


		# Row 1
		row_1 = VGroup(
			Text("1", font_size=FZ).move_to(swap_table[1][0].get_center()+DOWN),
			Text("a^b", font_size=FZ, t2c={"a": A_COLOUR, "b": B_COLOUR}).move_to(swap_table[1][1].get_center()+DOWN),
			Tex("$b_0$", font_size=FZ2).move_to(swap_table[1][2].get_center()+DOWN)
		)
		swap_table.add(row_1)

		for h in swap_table[2]:
			self.play(Write(h))
		self.wait(2)


		a_xor_b = Tex("$a_0 \\> ^{\\wedge} b_0$", font_size=FZ2).move_to(swap_table[1][1].get_center()+DOWN)
		self.play(Transform(swap_table[2][1], a_xor_b))
		self.wait(2)


		# Row 2
		row_2 = VGroup(
			Text("2", font_size=FZ).move_to(swap_table[2][0].get_center()+DOWN),
			Tex("$a_0 \\> ^{\\wedge} b_0$", font_size=FZ2).move_to(swap_table[2][1].get_center()+DOWN),
			Text("a^b", font_size=FZ, t2c={"a": A_COLOUR, "b": B_COLOUR}).move_to(swap_table[2][2].get_center()+DOWN)
		)
		swap_table.add(row_2)

		for h in swap_table[3]:
			self.play(Write(h))
		self.wait(2)


		a_xor_b = Tex("$a_0 \\> ^{\\wedge} b_0 \\> ^{\\wedge} b_0$", font_size=FZ2).move_to(swap_table[2][2].get_center()+DOWN)
		self.play(Transform(swap_table[3][2], a_xor_b))
		self.wait(2)


		a_xor_b = Tex("$a_0$", font_size=FZ2).move_to(swap_table[2][2].get_center()+DOWN)
		self.play(Transform(swap_table[3][2], a_xor_b))
		self.wait(2)


		# Row 3
		row_3 = VGroup(
			Text("3", font_size=FZ).move_to(swap_table[3][0].get_center()+DOWN),
			Text("a^b", font_size=FZ, t2c={"a": A_COLOUR, "b": B_COLOUR}).move_to(swap_table[3][1].get_center()+DOWN),
			Tex("$a_0$", font_size=FZ2).move_to(swap_table[3][2].get_center()+DOWN)
		)
		swap_table.add(row_3)

		for h in swap_table[4]:
			self.play(Write(h))
		self.wait(2)


		a_xor_b = Tex("$a_0 \\> ^{\\wedge} b_0 \\> ^{\\wedge} a_0$", font_size=FZ2).move_to(swap_table[3][1].get_center()+DOWN)
		self.play(Transform(swap_table[4][1], a_xor_b))
		self.wait(2)


		a_xor_b = Tex("$b_0$", font_size=FZ2).move_to(swap_table[3][1].get_center()+DOWN)
		self.play(Transform(swap_table[4][1], a_xor_b))
		self.wait(2)




class SwapLines(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		bitwise_table = BitwiseTable(self, "^", TEAL)

		string_1 = "11010010"
		string_2 = "01110101"
		bitwise_table.compare_two_binaries(string_1, string_2)
		fade_out_scene(self)


		string_3 = ""
		for i in range(0, len(string_1)):
			string_3 += str(int(string_1[i])^int(string_2[i]))
		string_1 = string_3

		bitwise_table.compare_two_binaries(string_1, string_2)
		fade_out_scene(self)


		string_3 = ""
		for i in range(0, len(string_1)):
			string_3 += str(int(string_1[i])^int(string_2[i]))
		string_2 = string_3

		bitwise_table.compare_two_binaries(string_1, string_2)
		fade_out_scene(self)




class ClearLsb(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GOLD_D, ORANGE], stroke_color=[GOLD_D, ORANGE],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #5: Clear the lowest set bit.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()


		num = 38
		binary.add_num_to_table(num, pace="fast")
		binary.flip_bit(6)
		binary.remove_num_from_table()


		num = 56
		binary.add_num_to_table(num, pace="fast")
		binary.flip_bit(4)
		binary.remove_num_from_table()


		num = 127
		binary.add_num_to_table(num, pace="fast")
		binary.flip_bit(7)
		binary.remove_num_from_table()



class ClearLsb2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		subtraction_tables = VGroup()

		def play_subtraction(num, pos):
			bw_subtraction = BitwiseSubtraction(self, num, 1)
			self.play(Create(bw_subtraction.subtraction_table.move_to(UP*2)))
			self.wait(1)

			bw_subtraction.perform_subtraction()
			self.wait(2)

			self.play(bw_subtraction.subtraction_table.animate.scale(0.5).move_to(pos))
			subtraction_tables.add(bw_subtraction.subtraction_table)


		params = [[15, DOWN*2.5+LEFT*6], [22, DOWN*2.3+LEFT*3], [108, DOWN*2.3], [88, DOWN*2.3+RIGHT*3], [48, DOWN*2.3+RIGHT*6]]
		for param in params:
			play_subtraction(*param)

		self.play(subtraction_tables.animate.move_to(ORIGIN))
		self.wait(5)


		self.play(FadeOut(subtraction_tables))


		bitwise_table = BitwiseTable(self, "&", ORANGE)

		string_1 = "01011000"
		string_2 = "01010111"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(5)

		fade_out_scene(self)