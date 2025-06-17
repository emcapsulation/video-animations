from manim import *
import colorsys

class QuickSort:
	def __init__(self, elements):
		self.elements = elements
		self.colours = self.generate_colors(len(self.elements))
		self.scene_elements = None


	# Generates a random colour for the element
	def generate_colors(self, n):
		colors = []
		for i in range(n):
			hue = (i / n)
			rgb = colorsys.hls_to_rgb(hue, 0.5, 0.5)  
			hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
			colors.append(hex_color)

		return colors 


	# Creates the list
	def create_scene_elements(self):
		self.scene_elements = VGroup()

		for i in range(0, len(self.elements)):
			new_elem = Text(str(self.elements[i]), color=self.colours[self.elements[i]])
			self.scene_elements.add(new_elem)

		self.scene_elements.arrange(RIGHT, buff=0.5)
		return self.scene_elements


	# Sets the pivot at this index and returns an arrow
	def set_pivot(self, pivot_index):
		self.pivot_index = pivot_index
		return Arrow(start=self.scene_elements[pivot_index].get_center()+DOWN,
			end=self.scene_elements[pivot_index].get_center()).shift(DOWN*0.5)


	# Swaps two elements
	def animate_swap(self, scene, i, j):
		i_pos = self.scene_elements[i].get_center()
		j_pos = self.scene_elements[j].get_center()

		path = Line(i_pos, j_pos)
		path.points[1:3] += UP*1

		path2 = Line(j_pos, i_pos)
		path2.points[1:3] += DOWN*1

		scene.play(
			MoveAlongPath(self.scene_elements[i], path),
			MoveAlongPath(self.scene_elements[j], path2)
		)

		tmp = self.scene_elements[i]
		self.scene_elements[i] = self.scene_elements[j]
		self.scene_elements[j] = tmp


	def create_low_arrow(self, scene, index):
		self.low = index

		self.low_arrow = VGroup(
			Arrow(start=self.scene_elements[index].get_center()+DOWN,
				end=self.scene_elements[index].get_center()),
			Text("low", font_size=20, color=ORANGE)).arrange(DOWN).next_to(self.scene_elements[index], DOWN*0.5)

		scene.play(Create(self.low_arrow))
		scene.wait(2)

		return self.low_arrow


	def create_high_arrow(self, scene, index):
		self.high = index

		self.high_arrow = VGroup(
			Arrow(start=self.scene_elements[index].get_center()+DOWN,
				end=self.scene_elements[index].get_center()),
			Text("high", font_size=20, color=TEAL)).arrange(DOWN).next_to(self.scene_elements[index], DOWN*0.5)

		scene.play(Create(self.high_arrow))
		scene.wait(2)

		return self.high_arrow