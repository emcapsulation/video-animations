from manim import *

from bit_manipulation import BinaryNumber, BitwiseTable

config.background_color = "#070d05"



class Parity(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[GREEN_B, GREEN], stroke_color=[GREEN_B, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #1: Check if a number is even or odd.", 
			font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		self.wait(5)

		bitwise_table = BitwiseTable(self, "&", GREEN)
		and_table = bitwise_table.bitwise_table.shift(UP)
		self.add(and_table)
		self.wait(2)


		self.play(and_table.animate.scale(0.6).shift(RIGHT*5))

		string_1 = "11001100"
		string_2 = "10100101"

		row_1 = VGroup()
		row_2 = VGroup()
		for i in range(0, len(string_1)):
			row_1.add(Text(string_1[i]))
			if i > 0:
				row_1[i].move_to(row_1[i-1].get_center() + RIGHT)

			row_2.add(Text(string_2[i]).move_to(row_1[i].get_center() + DOWN))
		binary_table = VGroup(row_1, row_2).move_to(LEFT*2 + DOWN*0.5)

		num_1 = Text(f"{int(string_1, 2)}").move_to(binary_table[0].get_center())
		self.play(Write(num_1))
		self.wait(1)
		self.play(Transform(num_1, binary_table[0]))

		num_2 = Text(f"{int(string_2, 2)}").move_to(binary_table[1].get_center())
		self.play(Write(num_2))
		self.wait(1)
		self.play(Transform(num_2, binary_table[1]))


		# Loop through binary strings and compare
		arrow = Arrow(start=binary_table[0][0].get_center()+UP*2, 
			end=binary_table[0][0].get_center()+UP).move_to(binary_table[0][0].get_center()+UP)
		self.play(Create(arrow))

		and_rect = bitwise_table.highlight_row.move_to(and_table[4].get_center())

		bin_rect = Rectangle(
			width=1, height=2,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		).move_to(binary_table[0][0].get_center()+DOWN*0.5)

		self.play(Create(bin_rect), Create(and_rect))

		and_row = VGroup()
		for i in range(0, len(string_1)):
			# Indicate the combination
			bit = "0"
			flash_colour = RED
			if string_1[i] == '1' and string_2[i] == '1':
				flash_colour=GREEN
				bit = "1"

			self.play(Indicate(bin_rect, color=flash_colour), 
				Indicate(and_rect, color=flash_colour))


			# Write the bit
			bit_text = Text(bit, color=flash_colour).move_to(binary_table[1][i].get_center() + DOWN)
			and_row.add(bit_text)
			self.play(Write(bit_text))


			# Shift over		
			if i < len(string_1)-1:
				move_anim = [
					arrow.animate.move_to(binary_table[0][i+1].get_center()+UP),
					bin_rect.animate.move_to(binary_table[0][i+1].get_center()+DOWN*0.5),
					bitwise_table.shift_highlight_row(string_1[i+1], string_2[i+1])
				]				

				self.play(*move_anim)

		binary_table.add(and_row)
		self.wait(2)

		self.play(
			FadeOut(and_rect), 
			FadeOut(bin_rect), 
			FadeOut(arrow), 
			FadeOut(binary_table),
			FadeOut(num_1),
			FadeOut(num_2)
		)



class Parity2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		bitwise_table = BitwiseTable(self, "&", GREEN)
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
			width=7.5, height=2,
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

		bitwise_table = BitwiseTable(self, "&", GREEN)
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


			bin_rect = Rectangle(
				width=0.75, height=1.25,
				color=WHITE, 
				stroke_width=0,
				fill_opacity=0.2
			).move_to(binary.binary_table[2][0].get_center()+DOWN*0.25)
			and_rect = bitwise_table.highlight_row.move_to(and_table[3].get_center())
			self.play(Create(bin_rect), Create(bitwise_table.highlight_row))


			and_row = VGroup()
			for i in range(0, len(binary.binary_table[0])):
				# Indicate the combination
				bit = "0"
				flash_colour = RED
				if binary_table[2][i].text == '1' and binary_table[3][i].text == '1':
					flash_colour=GREEN
					bit = "1"

				self.play(Indicate(bin_rect, color=flash_colour), 
					Indicate(and_rect, color=flash_colour))


				# Write the bit
				bit_text = Text(bit, color=(WHITE if bit=="1" else GRAY), font_size=28).next_to(binary_table[3][i].get_center(), DOWN)
				and_row.add(bit_text)
				self.play(Write(bit_text))


				# Shift over		
				if i < len(binary.binary_table[0])-1:
					move_anim = [
						bin_rect.animate.move_to(binary_table[2][i+1].get_center()+DOWN*0.25),
						bitwise_table.shift_highlight_row(binary_table[2][i+1].text, binary_table[3][i+1].text)
					]				

					self.play(*move_anim)

			self.wait(2)
			self.play(FadeOut(bin_rect), FadeOut(bitwise_table.highlight_row), FadeOut(and_row))
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
			fill_color=[GREEN_B, GREEN], stroke_color=[GREEN_B, GREEN],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #2: Multiply and divide by 2^k.", 
			font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(trick))


		shift_table = make_shift_table()
		self.add(shift_table)
		self.wait(2)


		self.play(FadeOut(speech_bubble), FadeOut(trick), shift_table.animate.shift(UP*2.5))



class Multiply2K(Scene):
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

