from manim import *

class Plant:
	def __init__(self, fill_opacity=0.8):
		self.plant = self.make_plant(fill_opacity)

	def make_plant(self, fill_opacity):
		plant = Ellipse(width=0.5, height=4, color=GREEN, fill_opacity=fill_opacity)
		plant_2 = Ellipse(width=0.5, height=1, color=GREEN, fill_opacity=fill_opacity).rotate(-PI/3).move_to(plant.get_center()+RIGHT*0.3+UP)
		pot = Sector(radius=2, start_angle=0, angle=-PI, color=DARK_BROWN, fill_opacity=1)
		full_plant = VGroup(VGroup(plant, plant_2), pot).arrange(DOWN, buff=0)
		full_plant[0].shift(RIGHT*0.2)
		return full_plant