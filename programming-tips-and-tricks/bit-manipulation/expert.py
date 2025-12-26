from manim import *
import math

from bit_manipulation import BinaryNumber, BitwiseTable, BitwiseSubtraction, fade_out_scene

config.background_color = "#140010"



class SameSign(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		speech_bubble = RoundedRectangle(
			width=12, height=1.25, 
			fill_color=[LIGHT_PINK, PINK], stroke_color=[LIGHT_PINK, PINK],
			corner_radius=0.1, fill_opacity=0.3,
			stroke_width=1
		).move_to(UP*2.5)
		self.play(Create(speech_bubble))

		trick = Text("Trick #8: Check if two numbers have the same sign.", 
			font_size=24).move_to(speech_bubble.get_center())
		self.play(Write(trick))

		trick_group = VGroup(speech_bubble, trick)
		self.wait(5)


		binary = BinaryNumber(self, 8)
		binary_table = binary.binary_table.move_to(ORIGIN)
		binary.create_binary_table()


		num = 4
		binary.add_num_to_table(num, pace="fast")
		self.wait(1)

		for num in range(3, -1, -1):
			binary.replace_num_in_table(num)
		self.wait(2)

		for num in range(-1, -10, -1):
			binary.replace_num_in_table(num)
		self.wait(2)



class TwosComplement(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		number_line = NumberLine(
			x_range=[-8, 7, 1],
			length=12,
			include_numbers=True,
			include_tip=False,
			stroke_width=2,
		)
		self.play(Create(number_line))
		self.wait(2)


		bins, instructions = VGroup(), VGroup()
		right = 6
		for i in range(7, -9, -1):
			cur = i
			if i < 0:
				cur = -1*i

			num_bin = bin(cur)[2:]
			num_bin = '0'*(4-len(num_bin)) + num_bin

			if i == -1:
				instructions_1 = Text("1. Take the positive equivalent.", font_size=24).move_to(UP*3)
				self.play(Write(instructions_1))
				instructions.add(instructions_1)

			binary = Text(num_bin, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN)
			self.play(Write(binary))

			# Show two's complement
			if i < 0:
				if i == -1:
					instructions_2 = Text("2. Flip all the bits.", font_size=24).next_to(instructions_1, DOWN)
					self.play(Write(instructions_2))
					instructions.add(instructions_2)

				flip_bits = ""
				for c in num_bin:
					flip_bits += ('1' if c == '0' else '0')

				binary_2 = Text(flip_bits, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN)
				self.play(Transform(binary, binary_2))

				if i == -1:
					instructions_3 = Text("3. Add 1.", font_size=24).next_to(instructions_2, DOWN)
					self.play(Write(instructions_3))
					instructions.add(instructions_3)

				num_bin = bin(i & 0b1111)[2:]
				binary_3 = Text(num_bin, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN)
				self.play(Transform(binary, binary_3))

			right -= 0.8
			bins.add(binary)

		self.wait(2)
		self.play(FadeOut(instructions))


		# Convert to ring
		ticks, numbers = VGroup(), VGroup()
		numbers = VGroup()
		for mob in number_line.get_family():
			if isinstance(mob, Line):
				ticks.add(mob)
			if isinstance(mob, DecimalNumber):
				numbers.add(mob)


		centre, radius, total = ORIGIN, 2, 8*2
		angle_step = (2*PI)/total

		target_ticks, target_numbers, target_bins = VGroup(), VGroup(), VGroup()
		directions = []
		for i in range(total):
			up = math.sin(i*2*PI/total)
			right = math.cos(i*2*PI/total)
			direction = UP*up + RIGHT*right
			directions.append(direction)

			tick_centre = centre + radius*direction
			tick = Line(
				tick_centre,
				tick_centre + 0.2*direction
			)

			number = Text(str(int(i-total/2)), font_size=24).move_to(tick_centre + 0.4*direction)
			binary_shifted = bins[len(bins)-1-i].copy().move_to(tick_centre + direction)

			target_ticks.add(tick)
			target_numbers.add(number)
			target_bins.add(binary_shifted)


		ring = Circle(radius=radius, stroke_color=WHITE).move_to(centre)

		transform_ticks_anim, transform_numbers_anim, transform_bins_anim = [], [], []
		for i in range(total):
			transform_ticks_anim.append(Transform(ticks[i], target_ticks[i]))
			transform_numbers_anim.append(Transform(numbers[i], target_numbers[i]))
			transform_bins_anim.append(Transform(bins[i], target_bins[i]))

		self.play(
			*transform_ticks_anim,
			*transform_numbers_anim,
			*transform_bins_anim,
			Create(ring),
			run_time=2
		)

		self.wait(5)




class SameSign2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		string_1 = "01101001"
		string_2 = "00110101"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class SameSign3(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		string_1 = "11011010"
		string_2 = "10110001"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)



class SameSign4(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		bitwise_table = BitwiseTable(self, "^", TEAL)
		xor_table = bitwise_table.bitwise_table.shift(UP)
		self.play(FadeIn(xor_table))
		self.wait(2)


		string_1 = "11010111"
		string_2 = "00011010"
		bitwise_table.compare_two_binaries(string_1, string_2)
		self.wait(2)


