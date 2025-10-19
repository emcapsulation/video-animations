from manim import *


def get_value_colour(min_val, max_val, val):
	val_range, gradient_steps = max_val-min_val, 100

	return color_gradient(
		[RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK], 
		gradient_steps
	)[int((val - min_val)/val_range * (gradient_steps-1))]



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


	def shift(self, direction, k):
		num_text = Text(f"<< {k}" if direction=="left" else f">> {k}", 
			font_size=24).move_to(self.binary_table[0].get_center()+UP)
		self.scene.play(Write(num_text))

		for j in range(0, k):
			self.scene.play(FadeOut(self.binary_table[2][0 if direction == "left" else self.num_bits-1]))

			shift_anim = []

			if direction == "left":
				for i in range(1, self.num_bits):
					self.binary_table[2][i-1] = self.binary_table[2][i]
					shift_anim.append(self.binary_table[2][i-1].animate.next_to(self.binary_table[1][i-1], DOWN))
			elif direction == "right":
				for i in range(self.num_bits-1, 0, -1):
					self.binary_table[2][i] = self.binary_table[2][i-1]
					shift_anim.append(self.binary_table[2][i].animate.next_to(self.binary_table[1][i], DOWN))

			last_bit = self.num_bits-1 if direction == "left" else 0
			self.binary_table[2][last_bit] = Text("0", color=GRAY, font_size=28).next_to(self.binary_table[1][last_bit], DOWN)
			shift_anim.append(FadeIn(self.binary_table[2][last_bit]))

			self.scene.play(*shift_anim)

		self.scene.play(FadeOut(num_text))



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

		i = 0
		for a in range(0, 2):
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

		return bitwise_table


	def make_highlight_row(self):
		return Rectangle(
			width=2, height=0.5,
			color=WHITE, 
			stroke_width=0,
			fill_opacity=0.2
		)


	def shift_highlight_row(self, a, b):
		pos = self.bitwise_table[1].get_center()
		if a == '0' and b == '1':
			pos = self.bitwise_table[2].get_center()
		elif a == '1' and b == '0':
			pos = self.bitwise_table[3].get_center()
		elif a == '1' and b == '1':
			pos = self.bitwise_table[4].get_center()

		return self.highlight_row.animate.move_to(pos)