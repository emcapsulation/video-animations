from manim import *


def fade_out_scene(scene):
	scene.play(
		*[FadeOut(mob)for mob in scene.mobjects]
	)


def get_value_colour(min_val, max_val, val):
	val_range, gradient_steps = max_val-min_val, 100

	return color_gradient(
		[RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK], 
		gradient_steps
	)[int((val - min_val)/val_range * (gradient_steps-1))]


def get_bin_colour(bit):
	return WHITE if bit=="1" else GRAY



class BinaryNumber():
	def __init__(self, scene, num_bits):
		self.scene = scene
		self.num_bits = num_bits
		self.binary_table = self.make_binary_table()


	def make_binary_table(self):
		binary_table = VGroup(VGroup(), VGroup())
		for i in range(self.num_bits-1, -1, -1):
			power = Tex(f"$2^{i}$", font_size=40, color=get_value_colour(0, self.num_bits-1, i))

			if i != self.num_bits-1:
				power.move_to(binary_table[0][self.num_bits-1-i-1].get_center() + RIGHT)
			binary_table[0].add(power)

			num = Tex(f"{2**i}", font_size=40, 
				color=get_value_colour(0, self.num_bits-1, i)).move_to(binary_table[0][self.num_bits-1-i].get_center() + DOWN*0.5)	
			binary_table[1].add(num)
		return binary_table


	def create_binary_table(self):
		for j in range(0, len(self.binary_table[0])):
			self.scene.play(
				Write(self.binary_table[0][j]),
				Write(self.binary_table[1][j])
			)


	def add_num_to_table(self, num, pace="slow", num_pos=UP):
		num_text = Text(f"{num}", font_size=24).move_to(self.binary_table[0].get_center()+num_pos)
		self.scene.play(Write(num_text))

		tab_len = len(self.binary_table)

		arrow = Arrow(
			start=self.binary_table[tab_len-1][0].get_center()+DOWN*2, 
			end=self.binary_table[tab_len-1][0].get_center()+DOWN
		).move_to(self.binary_table[tab_len-1][0].get_center() + DOWN)

		if pace == "slow":
			self.scene.play(Create(arrow))
			self.scene.wait(2)

		row = VGroup()
		cur = num
		for i in range(self.num_bits-1, -1, -1):
			binary = Text("1" if 2**i <= cur else "0", 
				color=(WHITE if 2**i <= cur else GRAY), font_size=28).next_to(self.binary_table[tab_len-1][self.num_bits-1-i], DOWN)

			row.add(binary)
			if pace == "slow":
				self.scene.play(Write(binary))
				self.scene.wait(1)

			if 2**i <= cur:
				minus = Text(f"{cur} - {2**i}", font_size=24).move_to(self.binary_table[0].get_center()+num_pos)
				if pace == "slow":
					self.scene.play(Transform(num_text, minus))
					self.scene.wait(1)

				new_cur = Text(f"{cur - 2**i}", font_size=24).move_to(self.binary_table[0].get_center()+num_pos)
				if pace == "slow":
					self.scene.play(Transform(num_text, new_cur))
					self.scene.wait(1)

				cur -= (2**i)

			if pace == "slow":
				if i > 0:
					self.scene.play(arrow.animate.move_to(self.binary_table[tab_len-1][self.num_bits-1-i+1].get_center() + DOWN))
				self.scene.wait(2)

		if pace == "slow":
			self.scene.play(FadeOut(num_text), FadeOut(arrow))
		else:
			self.scene.wait(2)
			self.scene.play(ReplacementTransform(num_text, row))			
			self.scene.wait(2)

		self.binary_table.add(row)


	def remove_num_from_table(self):
		self.scene.play(FadeOut(self.binary_table[len(self.binary_table)-1]))
		self.binary_table.remove(self.binary_table[len(self.binary_table)-1])


	def shift(self, direction, k, row=2):
		num_text = Text(f"<< {k}" if direction=="left" else f">> {k}", 
			t2c={"<<": PURPLE, ">>": PURPLE},
			font_size=24).move_to(self.binary_table[0].get_center()+UP)
		self.scene.play(Write(num_text))

		for j in range(0, k):
			self.scene.play(FadeOut(self.binary_table[row][0 if direction == "left" else self.num_bits-1]))

			shift_anim = []

			if direction == "left":
				for i in range(1, self.num_bits):
					self.binary_table[row][i-1] = self.binary_table[row][i]
					shift_anim.append(self.binary_table[row][i-1].animate.next_to(self.binary_table[row-1][i-1], DOWN))
			elif direction == "right":
				for i in range(self.num_bits-1, 0, -1):
					self.binary_table[row][i] = self.binary_table[row][i-1]
					shift_anim.append(self.binary_table[row][i].animate.next_to(self.binary_table[row-1][i], DOWN))

			last_bit = self.num_bits-1 if direction == "left" else 0
			self.binary_table[row][last_bit] = Text("0", color=GRAY, font_size=28).next_to(self.binary_table[row-1][last_bit], DOWN)
			shift_anim.append(FadeIn(self.binary_table[row][last_bit]))

			self.scene.play(*shift_anim)

		self.scene.play(FadeOut(num_text))


	def flip_bit(self, k, row=2):
		new_text = "1" if self.binary_table[row][k].text == "0" else "0"
		new_text_text = Text(str(new_text), 
				color=(WHITE if new_text == "1" else GRAY), 
				font_size=28).next_to(self.binary_table[row-1][k], DOWN)
		self.scene.play(Transform(self.binary_table[row][k], new_text_text))
		self.binary_table[row][k] = new_text_text


	def perform_bitwise_operation(self, bitwise_table):
		bin_rect = Rectangle(
			width=0.75, height=1.25,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		).move_to(self.binary_table[2][0].get_center()+DOWN*0.25)		

		if bitwise_table.operator == '~':
			bin_rect = Rectangle(
				width=0.75, height=0.75,
				color=WHITE, 
				stroke_width=0,
				fill_opacity=0.2
			).move_to(self.binary_table[3][0].get_center())

		bw_rect = bitwise_table.highlight_row
		shift_anim = None
		if bitwise_table.operator == '~':
			shift_anim = bitwise_table.shift_highlight_row_not(self.binary_table[2][0].text)
		else:
			shift_anim = bitwise_table.shift_highlight_row(self.binary_table[2][0].text, 
				self.binary_table[3][0].text)
		self.scene.play(Create(bin_rect), Create(bitwise_table.highlight_row), shift_anim)


		bw_row = VGroup()
		for i in range(0, len(self.binary_table[0])):
			# Indicate the combination
			bit = "0"
			flash_colour = RED
			if bitwise_table.operator == '&' and self.binary_table[2][i].text == '1' and self.binary_table[3][i].text == '1':
				flash_colour=GREEN
				bit = "1"
			elif bitwise_table.operator == '|' and (self.binary_table[2][i].text == '1' or self.binary_table[3][i].text == '1'):
				flash_colour=GREEN
				bit = "1"
			elif bitwise_table.operator == '^' and (self.binary_table[2][i].text != self.binary_table[3][i].text):
				flash_colour=GREEN
				bit = "1"
			elif bitwise_table.operator == '~' and self.binary_table[3][i].text == '0':
				flash_colour=GREEN
				bit = "1"

			self.scene.play(Indicate(bin_rect, color=flash_colour), 
				Indicate(bw_rect, color=flash_colour))


			# Write the bit
			if bitwise_table.operator != '~':
				bit_text = Text(bit, color=(WHITE if bit=="1" else GRAY), 
					font_size=28).move_to(self.binary_table[3][i].get_center()+DOWN)
				bw_row.add(bit_text)
				self.scene.play(Write(bit_text))
			else:
				bit_text = Text(bit, color=(WHITE if bit=="1" else GRAY), 
					font_size=28).move_to(self.binary_table[3][i].get_center())
				self.scene.play(Transform(self.binary_table[3][i], bit_text))
				self.binary_table[3][i] = bit_text


			# Shift over		
			if i < len(self.binary_table[0])-1:
				move_anim = []

				if bitwise_table.operator != '~':
					move_anim.append(bitwise_table.shift_highlight_row(self.binary_table[2][i+1].text, 
						self.binary_table[3][i+1].text))
					move_anim.append(bin_rect.animate.move_to(self.binary_table[2][i+1].get_center()+DOWN*0.25))
				else:
					move_anim.append(bitwise_table.shift_highlight_row_not(self.binary_table[3][i+1].text))
					move_anim.append(bin_rect.animate.move_to(self.binary_table[3][i+1].get_center()))

				self.scene.play(*move_anim)

		self.scene.wait(2)
		self.scene.play(FadeOut(bin_rect), FadeOut(bitwise_table.highlight_row))

		self.scene.wait(2)
		self.scene.play(FadeOut(bw_row))



class BitwiseTable():
	def __init__(self, scene, operator, colour):
		self.scene = scene
		self.operator = operator
		self.colour = colour
		self.bitwise_table = self.make_bitwise_table()
		self.highlight_row = self.make_highlight_row()


	def make_bitwise_table(self):
		bitwise_table = VGroup(
			VGroup(
				Text("x", color=self.colour), 
				Text("y", color=self.colour), 
				Text("x" + self.operator + "y", color=self.colour)
			).arrange(RIGHT, buff=0.7)
		)

		if self.operator == '~':
			bitwise_table = VGroup(
				VGroup(
					Text("x", color=self.colour), 
					Text(self.operator + "x", color=self.colour)
				).arrange(RIGHT, buff=0.7)
			)

		i = 0
		for a in range(0, 2):		
			if self.operator != '~':
				for b in range(0, 2):
					row = VGroup()
					row.add(Text(f"{a}").move_to(bitwise_table[i][0].get_center() + DOWN))
					row.add(Text(f"{b}").move_to(bitwise_table[i][1].get_center() + DOWN))

					operation = a&b
					if self.operator == "|":
						operation = a|b
					elif self.operator == "^":
						operation = a^b
					row.add(Text(f"{operation}").move_to(bitwise_table[i][2].get_center() + DOWN))

					bitwise_table.add(row)
					i += 1

			else:
				row = VGroup()
				row.add(Text(f"{a}").move_to(bitwise_table[i][0].get_center() + DOWN))
				row.add(Text(f"{int(not a)}").move_to(bitwise_table[i][1].get_center() + DOWN))
				bitwise_table.add(row)
				i += 1

		return bitwise_table


	def make_highlight_row(self):
		return Rectangle(
			width=2, height=0.5,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		)


	def shift_highlight_row(self, a, b, animate=True):
		pos = self.bitwise_table[1].get_center()
		if a == '0' and b == '1':
			pos = self.bitwise_table[2].get_center()
		elif a == '1' and b == '0':
			pos = self.bitwise_table[3].get_center()
		elif a == '1' and b == '1':
			pos = self.bitwise_table[4].get_center()

		if not animate:
			return self.highlight_row.move_to(pos)
		return self.highlight_row.animate.move_to(pos)


	def shift_highlight_row_not(self, a):
		pos = self.bitwise_table[1].get_center()
		if a == '1':
			pos = self.bitwise_table[2].get_center()

		return self.highlight_row.animate.move_to(pos)


	def compare_two_binaries(self, bin_1, bin_2):
		self.scene.play(self.bitwise_table.animate.scale(0.6).shift(RIGHT*5))		

		# Add the two binary strings to the grid
		row_1 = VGroup()
		row_2 = VGroup()
		for i in range(0, len(bin_1)):
			row_1.add(Text(bin_1[i], color=get_bin_colour(bin_1[i])))
			if i > 0:
				row_1[i].move_to(row_1[i-1].get_center() + RIGHT)

			row_2.add(Text(bin_2[i], color=get_bin_colour(bin_2[i])).move_to(row_1[i].get_center() + DOWN))
		binary_table = VGroup(row_1, row_2).move_to(LEFT*2 + DOWN*0.5)

		num_1 = Text(f"{int(bin_1, 2)}").move_to(binary_table[0].get_center())
		self.scene.play(Write(num_1))
		self.scene.wait(1)
		self.scene.play(Transform(num_1, binary_table[0]))

		num_2 = Text(f"{int(bin_2, 2)}").move_to(binary_table[1].get_center())
		self.scene.play(Write(num_2))
		self.scene.wait(1)
		self.scene.play(Transform(num_2, binary_table[1]))


		# Loop through binary strings and compare
		arrow = Arrow(start=binary_table[0][0].get_center()+UP*2, 
			end=binary_table[0][0].get_center()+UP).move_to(binary_table[0][0].get_center()+UP)
		self.scene.play(Create(arrow))

		bw_rect = self.shift_highlight_row(bin_1[0], bin_2[0], animate=False)

		bin_rect = Rectangle(
			width=1, height=2,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		).move_to(binary_table[0][0].get_center()+DOWN*0.5)

		self.scene.play(Create(bin_rect), Create(bw_rect))

		bw_row = VGroup()
		for i in range(0, len(bin_1)):
			# Indicate the combination
			bit = "0"
			flash_colour = RED
			if self.operator == '&' and bin_1[i] == '1' and bin_2[i] == '1':
				flash_colour=GREEN
				bit = "1"
			elif self.operator == '|' and (bin_1[i] == '1' or bin_2[i] == '1'):
				flash_colour=GREEN
				bit = "1"
			elif self.operator == '^' and bin_1[i] != bin_2[i]:
				flash_colour=GREEN
				bit = "1"

			self.scene.play(Indicate(bin_rect, color=flash_colour), 
				Indicate(bw_rect, color=flash_colour))


			# Write the bit
			bit_text = Text(bit, color=get_bin_colour(bit)).move_to(binary_table[1][i].get_center() + DOWN*1.5)
			bw_row.add(bit_text)
			self.scene.play(Write(bit_text))


			# Shift over		
			if i < len(bin_1)-1:
				move_anim = [
					arrow.animate.move_to(binary_table[0][i+1].get_center()+UP),
					bin_rect.animate.move_to(binary_table[0][i+1].get_center()+DOWN*0.5),
					self.shift_highlight_row(bin_1[i+1], bin_2[i+1])
				]				

				self.scene.play(*move_anim)

		binary_table.add(bw_row)
		self.scene.wait(2)


	def not_binary(self, bin_1):
		self.scene.play(self.bitwise_table.animate.scale(0.6).shift(RIGHT*5))


		def get_bin_colour(bit):
			return WHITE if bit=="1" else GRAY


		# Add the two binary strings to the grid
		row_1 = VGroup()
		row_2 = VGroup()
		for i in range(0, len(bin_1)):
			row_1.add(Text(bin_1[i], color=get_bin_colour(bin_1[i])))
			if i > 0:
				row_1[i].move_to(row_1[i-1].get_center() + RIGHT)
		binary_table = VGroup(row_1).move_to(LEFT*2)

		num_1 = Text(f"{int(bin_1, 2)}").move_to(binary_table[0].get_center())
		self.scene.play(Write(num_1))
		self.scene.wait(1)
		self.scene.play(Transform(num_1, binary_table[0]))


		# Loop through binary strings and compare
		arrow = Arrow(start=binary_table[0][0].get_center()+UP*2, 
			end=binary_table[0][0].get_center()+UP).move_to(binary_table[0][0].get_center()+UP)
		self.scene.play(Create(arrow))

		bw_rect = self.highlight_row.move_to(self.bitwise_table[1].get_center())

		bin_rect = Rectangle(
			width=1, height=1.5,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		).move_to(binary_table[0][0].get_center())

		self.scene.play(Create(bin_rect), Create(bw_rect))

		bw_row = VGroup()
		for i in range(0, len(bin_1)):
			# Indicate the combination
			bit = "0"
			flash_colour = RED
			if bin_1[i] == '0':
				flash_colour=GREEN
				bit = "1"

			self.scene.play(Indicate(bin_rect, color=flash_colour), 
				Indicate(bw_rect, color=flash_colour))


			# Write the bit
			bit_text = Text(bit, color=get_bin_colour(bit)).move_to(binary_table[0][i].get_center() + DOWN*1.5)
			bw_row.add(bit_text)
			self.scene.play(Write(bit_text))


			# Shift over		
			if i < len(bin_1)-1:
				move_anim = [
					arrow.animate.move_to(binary_table[0][i+1].get_center()+UP),
					bin_rect.animate.move_to(binary_table[0][i+1].get_center()),
					self.shift_highlight_row_not(bin_1[i+1])
				]				

				self.scene.play(*move_anim)

		binary_table.add(bw_row)
		self.scene.wait(2)



class BitwiseSubtraction():
	def __init__(self, scene, num_1, num_2):
		self.scene = scene

		self.num_1 = num_1
		self.num_2 = num_2
		self.num_1_bin = bin(self.num_1)[2:]
		self.num_2_bin = bin(self.num_2)[2:].rjust(len(self.num_1_bin), '0')

		self.subtraction_table = self.make_subtraction_table()


	def make_subtraction_table(self):
		subtraction_table = VGroup()

		num_1_group = VGroup()
		for bit in self.num_1_bin:
			bit_text = Text(bit, color=get_bin_colour(bit))
			num_1_group.add(bit_text)
		subtraction_table.add(num_1_group.arrange(RIGHT))
		
		num_2_group = VGroup()
		for i in range(0, len(self.num_2_bin)):
			bit_text = Text(self.num_2_bin[i], color=get_bin_colour(self.num_2_bin[i])).move_to(subtraction_table[0][i].get_center()+DOWN)
			num_2_group.add(bit_text)
		subtraction_table.add(num_2_group)

		return subtraction_table


	def perform_subtraction(self):
		num_1_bits = self.subtraction_table[0].copy()
		line = None
		result = VGroup()

		for i in range(len(self.num_1_bin)-1, -1, -1):
			if num_1_bits[i].text == '0' and self.num_2_bin[i] == '1':
				# Trade
				j = i
				while (num_1_bits[j].text != '1'):
					j -= 1

				line = Line(start=self.subtraction_table[0][j].get_center()+LEFT*0.1, end=self.subtraction_table[0][i].get_center()+RIGHT*0.1, color=RED, stroke_width=2)
				self.scene.play(Create(line))

				carry_bit = Text('0', color=RED, font_size=20).move_to(num_1_bits[j].get_center()).shift(UP*0.75+RIGHT*0.2)
				num_1_bits[j] = carry_bit
				self.scene.play(Write(carry_bit))

				for k in range(j+1, i+1):
					carry_bit = Text('1', color=RED, font_size=20).move_to(num_1_bits[k].get_center()).shift(UP*0.75+RIGHT*0.2)
					num_1_bits[k] = carry_bit
					self.scene.play(Write(carry_bit))

			bit = str(int(num_1_bits[i].text)-int(self.num_2_bin[i]))
			bit_text = Text(bit, color=get_bin_colour(bit)).move_to(self.subtraction_table[1][i].get_center()+DOWN*1.25)
			self.scene.play(Write(bit_text))

			result.add(bit_text)

		self.subtraction_table.add(result, num_1_bits)

		if line is not None:
			self.subtraction_table.add(line)


