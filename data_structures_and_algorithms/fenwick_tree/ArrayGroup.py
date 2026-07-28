from manim import *


class ArrayGroup:
	ARRAY_GROUP_FS = 30
	INDEX_GROUP_FS = 10

	ARRAY_BUFF = 0.3

	def __init__(self, array):
		self.array = array
		self.array_group = self.create_array_group()

	def create_array_group(self):
		ag = VGroup()

		for i in range(0, len(self.array)):
			invisible_box = Rectangle(width=0.6, height=0.6, stroke_width=0)
			arr = Text(str(self.array[i]), font_size=ArrayGroup.ARRAY_GROUP_FS)
			ind = Text(str(i), font_size=ArrayGroup.INDEX_GROUP_FS)

			elem = VGroup(invisible_box, VGroup(ind, arr).arrange(DOWN).move_to(invisible_box.get_center()))
			ag.add(elem)

		ag.arrange(RIGHT)

		left_bracket = Text("[", font_size=ArrayGroup.ARRAY_GROUP_FS)
		right_bracket = Text("]", font_size=ArrayGroup.ARRAY_GROUP_FS)

		return VGroup(left_bracket, ag, right_bracket).arrange(RIGHT)

	def get_array_group(self):
		return self.array_group[1]

	def get_i(self, i):
		return self.get_array_group()[i]

	def get_i_num(self, i):
		return self.get_i(i)[1][1]

	def get_brackets(self):
		return VGroup(self.array_group[0], self.array_group[2])

	def change_i(self, i, new_val):
		old_text = self.get_i(i)[1][1]
		old_val = self.array[i]
		new_text = Text(str(old_val+new_val), font_size=ArrayGroup.ARRAY_GROUP_FS).move_to(old_text.get_center())
		self.array[i] += new_val

		return Transform(self.get_i(i)[1][1], new_text)

