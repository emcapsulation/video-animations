from manim import *

class FloppyDisk:
	def __init__(self):
		self.floppy_disk = self.make_floppy()


	def make_floppy(self):
		disk = RoundedRectangle(
			width=1, height=1,
			corner_radius=[0, 0, 0, 0.1],
			stroke_color=GRAY,
			fill_color=GRAY,
			fill_opacity=0.85
		)

		circle = Circle(
			radius=0.1,
			stroke_color=GRAY_A,
			fill_color=GRAY_A,
			fill_opacity=0.85
		).move_to(disk.get_center())

		return VGroup(disk, circle)