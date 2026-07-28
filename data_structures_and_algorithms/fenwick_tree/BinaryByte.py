from manim import *

from utils import generate_colours

PASTEL_RED = "#ff8a8a"
PASTEL_PINK = "#ff8adc"
PASTEL_PURPLE = "#ce8aff"
PASTEL_INDIGO = "#9a8aff"
PASTEL_BLUE = "#8ab9ff"
PASTEL_TEAL = "#8afbff"

class BinaryByte:
	def __init__(self, base_10):
		self.base_10 = base_10
		self.base_2 = f"{base_10:08b}"
		self.bit_vals = [2**k for k in range(7, -1, -1)]
		self.v_binary = self.make_binary()

	def make_binary(self):
		l_colours = generate_colours([k for k in range(7, -1, -1)], colour_scheme=[PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO, PASTEL_BLUE, PASTEL_TEAL])

		byte_group = VGroup()

		for i in range(0, len(self.bit_vals)):
			invisible_box = Rectangle(width=0.6, height=0.6, stroke_width=0)

			pow_2 = MathTex(fr"2^{{{8-i-1}}}", font_size=30, color=l_colours[i])
			ind = Text(str(self.bit_vals[i]), font_size=18, color=GRAY)
			bit = Text(self.base_2[i], font_size=30)			

			elem = VGroup(invisible_box, VGroup(pow_2, ind, bit).arrange(DOWN).move_to(invisible_box.get_center()))
			byte_group.add(elem)

		byte_group.arrange(RIGHT)

		return byte_group

	def get_bit(self, i):
		return self.v_binary[8-i-1][1]

