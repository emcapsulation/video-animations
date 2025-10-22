from manim import *

from bit_manipulation import BinaryNumber, BitwiseTable

config.background_color = "#041200"



class Parity(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_A, GREEN], stroke_color=[GREEN_A, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #1: Check if a number is even or odd.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		self.wait(5)

		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.shift(UP)
		self.add(and_table)
		self.wait(2)


		string_1 = "11001100"
		string_2 = "10100101"
		bitwise_table.compare_two_binaries(string_1, string_2)



class Parity2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(and_table)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		binary.create_binary_table()


		num = 235
		num_text = Text(f"{num}").move_to(LEFT*1.5 + DOWN*2)
		self.play(Write(num_text))


		binary.add_num_to_table(num)


		bit_highlight = Rectangle(
			width=1, height=2,
			color=RED, fill_opacity=0.2,
			stroke_width=0
		).move_to(binary.binary_table[0][7].get_center() + DOWN*0.5)
		self.play(Create(bit_highlight))

		odd_brace = BraceBetweenPoints(
			binary.binary_table[0][7].get_center() + UP*0.25 + LEFT*0.5, 
			binary.binary_table[0][7].get_center() + UP*0.25 + RIGHT*0.5,
			direction=UP
		)

		odd = Text("odd", font_size=24, color=RED).move_to(binary.binary_table[0][7].get_center() + UP)
		self.play(Write(odd), Create(odd_brace))
		self.wait(1)


		new_highlight = Rectangle(
			width=7, height=2,
			color=GREEN, fill_opacity=0.2,
			stroke_width=0
		).move_to(binary.binary_table[0].get_center() + DOWN*0.5 + LEFT*0.5)
		self.play(Transform(bit_highlight, new_highlight))

		even_brace = BraceBetweenPoints(
			binary.binary_table[0][0].get_center() + UP*0.25 + LEFT*0.5, 
			binary.binary_table[0][6].get_center() + UP*0.25 + RIGHT*0.5,
			direction=UP
		)

		even = Text("even", font_size=24, color=GREEN).move_to(binary.binary_table[0][3].get_center() + UP)
		self.play(Write(even), Create(even_brace))
		self.wait(1)

		self.play(FadeOut(bit_highlight), FadeOut(num_text))
		self.wait(1)

		binary.remove_num_from_table()

		def play_last_bit(num):
			binary.add_num_to_table(num, pace="fast", num_pos=UP*2)
			self.play(Indicate(binary.binary_table[2][7], color=(RED if num&1 else GREEN)))
			binary.remove_num_from_table()

		explanation = Text("Odd values end in a 1 bit.", font_size=24).move_to(binary.binary_table.get_center() + DOWN*2.5)
		self.play(Write(explanation))
		self.wait(1)		

		odd_nums = [183, 79]		
		for num in odd_nums:
			play_last_bit(num)

		explanation_2 = Text("Even values end in a 0 bit.", font_size=24).move_to(binary.binary_table.get_center() + DOWN*3)
		self.play(Write(explanation_2))
		self.wait(1)		
		even_nums = [244, 92]
		for num in even_nums:
			play_last_bit(num)
		


class Parity3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(and_table)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		self.add(binary.binary_table)


		explanation = Text("Take the bitwise AND of 1 with\nthe number you are checking.", font_size=24).move_to(binary.binary_table.get_center() + DOWN*3.5)
		self.play(Write(explanation))
		self.wait(2)

		check = [201, 232]
		for c in check:
			binary.add_num_to_table(c, pace="fast")
			binary.add_num_to_table(1, pace="fast")
			self.wait(1)

			binary.perform_bitwise_operation(bitwise_table)

			binary.remove_num_from_table()
			binary.remove_num_from_table()



def make_shift_table():
	shift_table = VGroup()
	rows = [
		["<<", "Left Shift", "Shifts all bits k steps to the left."],
		[">>", "Right Shift", "Shifts all bits k steps to the right."]
	]

	for row in rows:
		r = VGroup()
		for col in row:
			col_text = Text(col, color=(PURPLE if len(col)==2 else WHITE), font_size=20)
			r.add(col_text)
		shift_table.add(r.arrange(RIGHT, buff=0.5))
	return shift_table.arrange(DOWN).move_to(ORIGIN)


class Multiply2K(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_A, GREEN], stroke_color=[GREEN_A, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #2: Multiply and divide by 2^k.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		shift_table = make_shift_table()
		self.add(shift_table)
		self.wait(2)


		self.play(FadeOut(speech_bubble), FadeOut(trick), shift_table.animate.shift(UP*2.5))



class Multiply2K2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")
		shift_table = make_shift_table()
		self.add(shift_table.shift(UP*2.5))


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()


		def show_multiplication(num, k):
			binary_str = bin(num)
			binary_str_2 = bin(int(num*(2**k)))
			mult = "2^{" + f"{k}" + "}"

			expand, expand_2 = "", ""
			power = len(binary_str)-3
			for c in range(2, len(binary_str)):
				if binary_str[c] == '1':
					expand += "2^{" + f"{power}" + "} + "
					expand_2 += "2^{" + f"{power+k}" + "} + "

				power -= 1
			expand = expand[0:-3]
			expand_2 = expand_2[0:-3]


			num_text = MathTex(f"{num}").move_to(DOWN*2)
			self.play(Write(num_text))

			num_text_bin = MathTex(f"{num}", "=", f"{expand}").move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text, num_text_bin))

			
			num_text_2 = MathTex(f"{num}", "=", f"{expand}", 
				"=", f"{binary_str}").move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text_bin, num_text_2))
			self.wait(2)


			num_text_3 = MathTex(f"{mult} \\times", f"{num}", 
				"=", f"{mult}", "(", f"{expand}", ")", 
				"=", f"{mult} \\times", f"{binary_str}").move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text_2, num_text_3))
			self.wait(2)

			
			num_text_4 = MathTex("=", f"{expand_2}").move_to(DOWN*3)
			self.play(Write(num_text_4))
			self.wait(2)


			# Shift
			if k < 0:
				binary.shift("right", -1*k)
			else:
				binary.shift("left", k)
			self.wait(2)


			num_text_5 = MathTex("=", f"{expand_2}", "=", f"{binary_str_2}").move_to(DOWN*3)
			self.play(TransformMatchingTex(num_text_4, num_text_5))
			self.wait(2)


			num_text_6 = MathTex("=", f"{expand_2}", 
				"=", f"{binary_str_2}", 
				"=", f"{int(2**k * num)}").move_to(DOWN*3)
			self.play(TransformMatchingTex(num_text_5, num_text_6))
			self.wait(2)


			self.play(FadeOut(num_text_3), FadeOut(num_text_6))


		num = 13

		binary.add_num_to_table(num)
		show_multiplication(num, 1)
		binary.remove_num_from_table()


		binary.add_num_to_table(num, pace="fast")
		show_multiplication(num, 3)
		binary.remove_num_from_table()


		num = 104
		binary.add_num_to_table(num, pace="fast")
		show_multiplication(num, -3)
		binary.remove_num_from_table()



def set_toggle_unset(mode, scene):
	binary = BinaryNumber(scene, 8)
	binary_table = binary.binary_table.move_to(ORIGIN)
	binary.create_binary_table()

	# Label bit numbers
	bit_labels = VGroup()
	for i in range(7, -1, -1):
		bit_label = Text(str(7-i), font_size=20).next_to(binary.binary_table[0][i], UP)
		scene.play(Write(bit_label))
		bit_labels.add(bit_label)
	scene.wait(2)


	k = 3
	arrow = Arrow(start=binary.binary_table[1][7-k].get_center()+DOWN*2, end=binary.binary_table[1][7-k].get_center()+DOWN)
	k_equals = Text("k = 3", font_size=20).next_to(arrow, DOWN)
	scene.play(Create(arrow))
	scene.play(Write(k_equals))
	scene.wait(2)


	binary.add_num_to_table(38, pace="fast")
	scene.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
	if mode == "set" or mode == "toggle":
		binary.flip_bit(7-k)
	scene.wait(2)

	binary.remove_num_from_table()


	binary.add_num_to_table(59, pace="fast")
	scene.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
	if mode == "toggle" or mode == "clear":
		binary.flip_bit(7-k)
	scene.wait(2)

	binary.remove_num_from_table()



class SetKthBit(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_A, GREEN], stroke_color=[GREEN_A, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #3.1: Set the kth bit from the right.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		set_toggle_unset("set", self)



class SetKthBit2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "|", GREEN)
		or_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(or_table))
		self.wait(2)


		string_1 = "10101100"
		string_2 = "01100101"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class SetKthBit3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		self.add(binary.binary_table)

		# Label bit numbers
		bit_labels = VGroup()
		for i in range(7, -1, -1):
			bit_label = Text(str(7-i), font_size=20).next_to(binary.binary_table[0][i], UP)
			self.add(bit_label)
			bit_labels.add(bit_label)
		self.wait(2)


		bitwise_table = BitwiseTable(self, "|", GREEN)
		and_table = bitwise_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(and_table)


		k=3
		check = [38, 59]
		for c in check:			
			binary.add_num_to_table(c, pace="fast")
			self.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
			self.wait(2)

			step_1 = Text("1. Shift 1 k spots to the left.", 
				font_size=24).move_to(binary.binary_table.get_center() + DOWN*3)
			self.play(Write(step_1))
			self.wait(1)

			binary.add_num_to_table(1, pace="fast")
			binary.shift("left", k, row=3)
			self.wait(2)

			step_2 = Text("2. Take the bitwise OR.", font_size=24).next_to(step_1, DOWN)
			self.play(Write(step_2))
			self.wait(1)

			binary.perform_bitwise_operation(bitwise_table)

			binary.remove_num_from_table()
			binary.remove_num_from_table()



class ToggleKthBit(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_A, GREEN], stroke_color=[GREEN_A, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #3.2: Toggle the kth bit from the right.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		set_toggle_unset("toggle", self)



class ToggleKthBit2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		string_1 = "10101100"
		string_2 = "01100101"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class ToggleKthBit3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		self.add(binary.binary_table)

		# Label bit numbers
		bit_labels = VGroup()
		for i in range(7, -1, -1):
			bit_label = Text(str(7-i), font_size=20).next_to(binary.binary_table[0][i], UP)
			self.add(bit_label)
			bit_labels.add(bit_label)
		self.wait(2)


		bitwise_table = BitwiseTable(self, "^", TEAL)
		and_table = bitwise_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(and_table)


		k=3
		check = [38, 59]
		for c in check:			
			binary.add_num_to_table(c, pace="fast")
			self.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
			self.wait(2)

			step_1 = Text("1. Shift 1 k spots to the left.", 
				font_size=24).move_to(binary.binary_table.get_center() + DOWN*3)
			self.play(Write(step_1))
			self.wait(1)

			binary.add_num_to_table(1, pace="fast")
			binary.shift("left", k, row=3)
			self.wait(2)

			step_2 = Text("2. Take the bitwise XOR.", font_size=24).next_to(step_1, DOWN)
			self.play(Write(step_2))
			self.wait(1)

			binary.perform_bitwise_operation(bitwise_table)

			binary.remove_num_from_table()
			binary.remove_num_from_table()



class ClearKthBit(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_A, GREEN], stroke_color=[GREEN_A, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #3.3: Clear the kth bit from the right.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		set_toggle_unset("clear", self)



class ClearKthBit2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "~", RED)
		not_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(not_table))
		self.wait(2)


		string_1 = "10101100"
		bitwise_table.not_binary(string_1)
		self.wait(2)



class ClearKthBit3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		self.add(binary.binary_table)

		# Label bit numbers
		bit_labels = VGroup()
		for i in range(7, -1, -1):
			bit_label = Text(str(7-i), font_size=20).next_to(binary.binary_table[0][i], UP)
			self.add(bit_label)
			bit_labels.add(bit_label)
		self.wait(2)


		not_table = BitwiseTable(self, "~", RED)
		not_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(not_table.bitwise_table)


		k=3
		c = 59		
		binary.add_num_to_table(c, pace="fast")
		self.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
		self.wait(2)

		step_1 = Text("1. Shift 1 k spots to the left.", 
			font_size=24).move_to(binary.binary_table.get_center() + DOWN*3)
		self.play(Write(step_1))
		self.wait(1)

		binary.add_num_to_table(1, pace="fast")
		binary.shift("left", k, row=3)
		self.wait(2)


		step_2 = Text("2. Apply bitwise NOT to the shifted 1.", font_size=24).next_to(step_1, DOWN)
		self.play(Write(step_2))
		self.wait(1)

		binary.perform_bitwise_operation(not_table)


		step_3 = Text("3. Take the bitwise AND.", font_size=24).next_to(step_2, DOWN)
		self.play(Write(step_3))
		self.wait(1)

		and_table = BitwiseTable(self, "&", ORANGE)
		and_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.play(ReplacementTransform(not_table.bitwise_table, and_table.bitwise_table))

		binary.perform_bitwise_operation(and_table)

		binary.remove_num_from_table()
		binary.remove_num_from_table()

		self.play(ReplacementTransform(and_table.bitwise_table, not_table.bitwise_table))



class ClearKthBit4(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(LEFT*1.5 + UP)
		self.add(binary.binary_table)

		# Label bit numbers
		bit_labels = VGroup()
		for i in range(7, -1, -1):
			bit_label = Text(str(7-i), font_size=20).next_to(binary.binary_table[0][i], UP)
			self.add(bit_label)
			bit_labels.add(bit_label)
		self.wait(2)


		not_table = BitwiseTable(self, "~", RED)
		not_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.add(not_table.bitwise_table)


		k=3
		c = 38		
		binary.add_num_to_table(c, pace="fast")
		self.play(Indicate(binary.binary_table[2][7-k], color=GREEN))
		self.wait(2)

		step_1 = Text("1. Shift 1 k spots to the left.", 
			font_size=24).move_to(binary.binary_table.get_center() + DOWN*3)
		self.play(Write(step_1))
		self.wait(1)

		binary.add_num_to_table(1, pace="fast")
		binary.shift("left", k, row=3)
		self.wait(2)


		step_2 = Text("2. Apply bitwise NOT to the shifted 1.", font_size=24).next_to(step_1, DOWN)
		self.play(Write(step_2))
		self.wait(1)

		binary.perform_bitwise_operation(not_table)


		step_3 = Text("3. Take the bitwise AND.", font_size=24).next_to(step_2, DOWN)
		self.play(Write(step_3))
		self.wait(1)

		and_table = BitwiseTable(self, "&", ORANGE)
		and_table.bitwise_table.shift(UP).scale(0.6).shift(RIGHT*5)
		self.play(ReplacementTransform(not_table.bitwise_table, and_table.bitwise_table))

		binary.perform_bitwise_operation(and_table)

		binary.remove_num_from_table()
		binary.remove_num_from_table()

		self.play(ReplacementTransform(and_table.bitwise_table, not_table.bitwise_table))