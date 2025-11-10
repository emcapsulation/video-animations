from manim import *
from bit_manipulation import BinaryNumber, BitwiseTable


config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class BinaryExplanation(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


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


		title = Text("Binary Explanation").move_to(UP*5)
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


		# Display binary 1011101
		binary_text = Text("0", t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP)
		self.play(Write(binary_text))
		self.wait(1)

		self.play(
			Transform(binary_text, 
			Text("1", t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP))
		)
		self.wait(1)

		for i in range(0, 94):
			self.play(
				Transform(binary_text, 
					Text(format(i, 'b'), t2c={"1": get_binary_colour(1), "0": get_binary_colour(0)}).shift(UP), 
					run_time=0.005)
				)
		self.wait(2)


		def write_binary_str(binary_str):
			expand, expand2 = VGroup(VGroup(), VGroup()), VGroup(VGroup(), VGroup())
			ei = 0

			answer = 0
			for i in range(0, len(binary_str)):
				if i >= 4:
					ei = 1

				expand[ei].add(Tex(f"${binary_str[i]}\\times 2^{len(binary_str)-i-1}$", 
					font_size=28, 
					color=get_binary_colour(int(binary_str[i])))
				)

				term = int(binary_str[i]) * 2**(len(binary_str)-i-1)
				expand2[ei].add(Tex(f"${term}$", 
					font_size=36, 
					color=get_binary_colour(int(binary_str[i])))
				)

				answer += term

				if i < len(binary_str)-1:
					expand[ei].add(Tex("+", font_size=28))
					expand2[ei].add(Tex("+", font_size=36))


			def write_expand(expand, pos):
				expand[0].arrange(RIGHT)
				expand[1].arrange(RIGHT)
				expand.arrange(DOWN).move_to(pos)

				for text in expand:
					self.play(Write(text))
					self.wait(1)

			write_expand(expand, DOWN*2)
			write_expand(expand2, DOWN*3.5)

			term_text = Text(f"= {answer}").next_to(expand2, DOWN, buff=0.5)
			self.play(Write(term_text))
			self.wait(2)

			self.play(
				FadeOut(binary_text), 
				FadeOut(expand), 
				FadeOut(expand2), 
				FadeOut(term_text)
			)

		write_binary_str("1011101")


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN).scale(0.9)
		binary.create_binary_table()
		self.wait(1)

		binary.add_num_to_table(77)
		write_binary_str("1001101")	




class Parity(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		FZ = 24

		question_group = VGroup()

		question_1 = Text("Can you check if an", font_size=FZ)
		question_group.add(question_1)

		question_2 = Text("integer is even or odd", font_size=FZ, t2c={"even": GREEN, "odd": RED})
		question_group.add(question_2)

		question_3 = Text("without using mod?", font_size=FZ)
		question_group.add(question_3)

		question_group.arrange(DOWN).move_to(ORIGIN)

		self.play(FadeIn(question_group))
		self.wait(1)
		self.play(question_group.animate.shift(UP*5))
		self.wait(5)


		bitwise_table = BitwiseTable(self, "&", ORANGE)
		and_table = bitwise_table.bitwise_table.move_to(ORIGIN)
		self.play(FadeIn(and_table))
		self.wait(1)
		self.play(and_table.animate.scale(0.5).shift(DOWN*2.5))


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.scale(0.9).move_to(UP*2)
		binary.create_binary_table()


		bit_highlight = Rectangle(
			width=0.9*1, height=0.9*1.5,
			color=RED, fill_opacity=0.2,
			stroke_width=0
		).move_to(binary.binary_table[0][7].get_center() + DOWN*0.9*0.25)
		self.play(Create(bit_highlight))

		odd_brace = BraceBetweenPoints(
			binary.binary_table[0][7].get_center() + UP*0.9*0.25 + LEFT*0.9*0.5, 
			binary.binary_table[0][7].get_center() + UP*0.9*0.25 + RIGHT*0.9*0.5,
			direction=UP
		)

		odd = Text("odd", font_size=24, color=RED).move_to(binary.binary_table[0][7].get_center() + UP)
		self.play(Write(odd), Create(odd_brace))
		self.wait(1)


		new_highlight = Rectangle(
			width=0.9*7, height=0.9*1.5,
			color=GREEN, fill_opacity=0.2,
			stroke_width=0
		).move_to(binary.binary_table[0].get_center() + DOWN*0.9*0.25 + LEFT*0.9*0.5)
		self.play(Transform(bit_highlight, new_highlight))

		even_brace = BraceBetweenPoints(
			binary.binary_table[0][0].get_center() + UP*0.9*0.25 + LEFT*0.9*0.5, 
			binary.binary_table[0][6].get_center() + UP*0.9*0.25 + RIGHT*0.9*0.5,
			direction=UP
		)

		even = Text("even", font_size=24, color=GREEN).move_to(binary.binary_table[0][3].get_center() + UP)
		self.play(Write(even), Create(even_brace))
		self.wait(1)

		self.play(FadeOut(bit_highlight))
		self.wait(1)


		def play_last_bit(num):
			binary.add_num_to_table(num, pace="fast", num_pos=UP*1.5)
			self.play(Indicate(binary.binary_table[2][7], color=(RED if num&1 else GREEN)))
			binary.remove_num_from_table()

		explanation = Text("Odd values end in a 1 bit.", font_size=20, t2c={"1": RED}).move_to(bitwise_table.bitwise_table.get_center() + DOWN*2)
		self.play(Write(explanation))
		self.wait(1)

		odd_nums = [183, 79]		
		for num in odd_nums:
			play_last_bit(num)

		explanation_2 = Text("Even values end in a 0 bit.", font_size=20, t2c={"0": GREEN}).move_to(bitwise_table.bitwise_table.get_center() + DOWN*2.5)
		self.play(Write(explanation_2))
		self.wait(1)

		even_nums = [244, 92]
		for num in even_nums:
			play_last_bit(num)


		explanation_3 = Text("Take the bitwise AND of 1 with\nthe number you are checking.", font_size=FZ, t2c={"1": RED}).move_to(question_group.get_center())
		self.play(Transform(question_group, explanation_3))
		self.wait(2)

		check = [91, 74]
		for c in check:
			binary.add_num_to_table(c, pace="fast", num_pos=UP*1.5)
			binary.add_num_to_table(1, pace="fast", num_pos=UP*1.5)
			self.wait(1)

			binary.perform_bitwise_operation(bitwise_table)

			binary.remove_num_from_table()
			binary.remove_num_from_table()



class MultiplyDivide2PowK(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		def make_shift_table():
			shift_table = VGroup()
			rows = [
				["<<", "Left Shift", "Shifts all bits k steps left."],
				[">>", "Right Shift", "Shifts all bits k steps right."]
			]

			for row in rows:
				r = VGroup()
				for col in row:
					col_text = Text(col, color=(PURPLE if len(col)==2 else WHITE), font_size=16)
					r.add(col_text)
				shift_table.add(r.arrange(RIGHT, buff=0.5))
			return shift_table.arrange(DOWN).move_to(ORIGIN)


		FZ = 24

		question_group = VGroup()

		question_1 = Text("Can you multiply and divide by ", font_size=FZ, t2c={"multiply": TEAL, "divide": PINK})
		question_group.add(question_1)

		question_2 = Text("2^k without using *, / or pow?", font_size=FZ)
		question_group.add(question_2)

		question_3 = Text("(for non-negative k)", font_size=FZ)
		question_group.add(question_3)

		question_group.arrange(DOWN).move_to(ORIGIN)

		self.play(FadeIn(question_group))
		self.wait(1)
		self.play(question_group.animate.shift(UP*5))
		self.wait(5)


		shift_table = make_shift_table()
		self.add(shift_table.shift(DOWN*5))
		self.wait(2)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.scale(0.9).move_to(ORIGIN)
		binary.create_binary_table()


		def show_multiplication(num, k):
			FS = 30

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


			num_text = MathTex(f"{num}", font_size=FS).move_to(DOWN*2)
			self.play(Write(num_text))

			num_text_bin = MathTex(f"{num}", "=", f"{expand}", font_size=FS).move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text, num_text_bin))

			
			num_text_2 = MathTex(f"{num}", "=", f"{expand}", 
				"=", f"{binary_str}", font_size=FS).move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text_bin, num_text_2))
			self.wait(2)


			num_text_3 = MathTex(f"{mult} \\times", f"{num}", 
				"=", f"{mult}", "(", f"{expand}", ")", 
				"=", f"{mult} \\times", f"{binary_str}", font_size=FS).move_to(DOWN*2)
			self.play(TransformMatchingTex(num_text_2, num_text_3))
			self.wait(2)

			
			num_text_4 = MathTex("=", f"{expand_2}", font_size=FS).move_to(DOWN*3)
			self.play(Write(num_text_4))
			self.wait(2)


			# Shift
			if k < 0:
				binary.shift("right", -1*k)
			else:
				binary.shift("left", k)
			self.wait(2)


			num_text_5 = MathTex("=", f"{expand_2}", "=", f"{binary_str_2}", font_size=FS).move_to(DOWN*3)
			self.play(TransformMatchingTex(num_text_4, num_text_5))
			self.wait(2)


			num_text_6 = MathTex("=", f"{expand_2}", 
				"=", f"{binary_str_2}", 
				"=", f"{int(2**k * num)}", font_size=FS).move_to(DOWN*3)
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