from manim import *

PASTEL_BLUE = "#8ab9ff"
PASTEL_TEAL = "#8afbff"

class SkewedBellCurve:
	def __init__(self, x_range, y_range, x_length, y_length, title, label_x, label_y):
		self.axes = Axes(
			x_range=[0, 10, 1],
			y_range=[0, 0.5, 0.1],
			x_length=8,
			y_length=4,
			axis_config={
				"include_tip": True,
				"tip_width": 0.1,
				"tip_height": 0.1
			}
		)

		self.labels = self.axes.get_axis_labels(
			x_label=Text(label_x).scale(0.3),
			y_label=Text(label_y).scale(0.3)
		)

		self.curve = self.axes.plot(
			self.skewed_bell,
			x_range=[0, 10],
			color=PASTEL_BLUE,
		)

		self.title = Text(title, font_size=20).move_to(self.axes.get_top())

		self.chart = VGroup(self.title, self.axes, self.curve, self.labels)

	def skewed_bell(self, x):
		x -= 4
		sigma = 1 + 0.15 * np.tanh(x)
		return np.exp(-x**2 / (2 * sigma**2)) / (
			sigma * np.sqrt(2 * np.pi)
		)

	def get_line_at_x(self, x):
		return self.axes.get_vertical_line(self.axes.c2p(x, self.skewed_bell(x)), color=YELLOW)

	def get_area_in_x_range(self, x1, x2):
		return self.axes.get_area(self.curve, x_range=[x1, x2], color=PASTEL_TEAL, opacity=0.4)

	def get_area_before_x(self, x):
		return self.get_area_in_x_range(0, x)


