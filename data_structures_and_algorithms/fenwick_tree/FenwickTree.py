from manim import *


class FenwickTree:
	def __init__(self, array):
		self.array = array
		self.bit = self.construct_bit()

		self.v_array = self.make_v_array()
		self.v_bit = self.make_v_bit()

	def construct_bit(self):
		bit = [0]*(len(self.array)+1)
		for i in range(1, len(self.array)+1):
			bit[i] += self.array[i-1]
			parent = i + self.lsb(i)
			if parent <= len(self.array):
				bit[parent] += bit[i]
		return bit

	def lsb(self, i):
		return (i & -i)

	def make_v_array(self):
		return self.make_array_group(self.array, True)

	def make_v_bit(self):
		return self.make_array_group(self.bit, True, one_indexed=True)

	def make_array_group(self, array, show_binary, one_indexed=False):
		ag = VGroup()

		offset = 1 if one_indexed else 0
		for i in range(0+offset, len(array)):
			invisible_box = Rectangle(width=0.6, height=0.6, stroke_width=0)

			arr = Text(str(array[i]), font_size=24)
			ind = Text(str(i+1-offset), font_size=16)
			v_element = VGroup(ind, arr).arrange(DOWN)

			if show_binary:
				binary = Text(str(format(i+1-offset, '04b')), font_size=12, color=GRAY)
				v_element = VGroup(ind, binary, arr).arrange(DOWN)

			elem = VGroup(invisible_box, v_element.move_to(invisible_box.get_center()))
			ag.add(elem)

		ag.arrange(RIGHT)

		left_bracket = Text("[", font_size=24)
		right_bracket = Text("]", font_size=24)

		return VGroup(left_bracket, ag, right_bracket).arrange(RIGHT)

	def get_i(self, v_a, i):
		return v_a[1][i]

	def update_i(self, a, v_a, i, delta):
		new_val = a[i] + delta
		old_elem = self.get_i(v_a, i)[1][2]
		new_elem = Text(str(new_val), font_size=24).move_to(old_elem.get_center())

		return Transform(old_elem, new_elem)

	# List of elements with range size of 2^k
	def get_l_k_bit(self, k):
		ret = []
		for i in range(1, len(self.bit)):
			if (i & -i) == 2**k:
				ret.append(i)
		return ret

	# Group of rectangles over the ranges of size 2^k
	def make_rect_ranges(self, colour, k):
		rects = VGroup()
		for j in self.get_l_k_bit(k):
			l = self.get_i(self.v_array, j-1-(2**k)+1)[1][2].get_left()+LEFT*0.25
			r = self.get_i(self.v_array, j-1)[1][2].get_right()+RIGHT*0.25
			rect = Rectangle(
				width=r[0]-l[0], height=0.5, 
				fill_color=colour, fill_opacity=0.1, 
				stroke_width=0).move_to((l+r)/2)
			rects.add(rect)
		return rects

	# Group of actual elements in the range for size 2^k
	# Source
	def make_v_ranges(self, colour, k):
		ranges = VGroup()
		for i in self.get_l_k_bit(k):
			this_range = VGroup(*[self.get_i(self.v_array, j)[1][2].copy() for j in range(i-1-(2**k)+1, i)])
			ranges.add(this_range)
		return ranges

	# Target
	def make_part(self, colour, k):
		part = VGroup()
		for i in self.get_l_k_bit(k):
			element = self.get_i(self.v_bit, i-1).copy()
			element[1][0].color = colour
			element[1][1].color = colour
			part.add(element)
		return part.shift(DOWN*(1.5-k*0.5))